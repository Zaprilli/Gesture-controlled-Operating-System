import importlib.util
import math
import os
import shutil
import sys
import time

# --- Nomyn sanuud: ali negiig bish bol shaardlagiin taylan deer garna ---
_IMPORT_ERR = {}

try:
    import cv2
except ImportError:
    cv2 = None
    _IMPORT_ERR["cv2"] = "pip install opencv-python"

try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core.base_options import BaseOptions
except ImportError:
    mp = None
    vision = None
    BaseOptions = None
    _IMPORT_ERR["mediapipe"] = "pip install mediapipe"

MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "models", "hand_landmarker.task")

WINDOW_NAME = "Hand Control (q=quit, space=pause)"
WIN_W, WIN_H = 640, 480

ARM_HOLD_S = 1.2
LOCK_MAX_DIST = 0.15
LOCK_TIMEOUT_S = 2.0

PINCH_DIST = 0.06
DRAG_MIN = 0.035
DRAG_STEP = 0.012
TAP_MAX_S = 0.6

ARROW_HOLD_S = 0.35
ARROW_COOLDOWN_S = 1.0
ARROW_DEAD = 0.08
ARROW_STEP_PX = 60

HAND_BONES = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def fingers_up_count(lm):
    def up(tip, pip):
        return lm[tip].y < lm[pip].y
    n = 0
    for tip, pip in ((8, 6), (12, 10), (16, 14), (20, 18)):
        if up(tip, pip):
            n += 1
    return n


def classify_arrow(dx, dy):
    if abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def print_requirements():
    """Ажиллуулахад шаардлагатай бүх зүйлийг шалгаж, дэлгэрэнгүй хэвлэнэ.

    Зөвхөн ҮНДСЭН шаардлага (Python, номын сан, загвар, камера) дутуу бол
    False буцаана; нэмэлт хэрэгсэл (pactl, brightnessctl, xdotool...) дутуу
    бол зөвхөн анхааруулж, аль үйлдэл ажиллахгүйг хэлнэ.
    """
    sep = "=" * 62
    print(sep)
    print("  AJILLUULAHD SHAARDLAGATAI ZUIILSUUD (Requirements)")
    print(sep)
    fatal = []

    # 1) Python хувилбар
    ver = ".".join(map(str, sys.version_info[:3]))
    if sys.version_info >= (3, 10):
        print(f"  [OK]    Python 3.10+              : {ver}")
    else:
        print(f"  [ALDAA] Python 3.10+              : {ver} (shineer suulgana)")
        fatal.append("Python 3.10+ байх ёстой")

    # 2) Python номын сангууд
    for mod, pip_cmd in (("cv2", "pip install opencv-python"),
                         ("mediapipe", "pip install mediapipe")):
        if mod in _IMPORT_ERR:
            print(f"  [ALDAA] {mod:<25} : suugaagui -> {pip_cmd}")
            fatal.append(pip_cmd)
        else:
            mv = getattr(sys.modules.get(mod), "__version__", "suusan")
            print(f"  [OK]    {mod:<25} : {mv}")

    # 3) MediaPipe загвар
    if os.path.isfile(MODEL):
        print("  [OK]    ZAGVAR (hand_landmarker)  : models/hand_landmarker.task")
    else:
        print(f"  [ALDAA] ZAGVAR (hand_landmarker)  : olddoggui -> {MODEL}")
        fatal.append("models/hand_landmarker.task файл байх ёстой")

    # 4) Вебкамер
    if cv2 is None:
        print("  [ -- ]  KAMERA (index 0)          : cv2 baihgui tul shalgahgui")
    else:
        _cap = cv2.VideoCapture(0)
        if _cap.isOpened():
            print("  [OK]    KAMERA (index 0)          : oldloo")
        else:
            print("  [ALDAA] KAMERA (index 0)          : oldohgui baina")
            fatal.append("Вебкамер холбогдсон байх ёстой (index 0) — "
                         "бусад процесст эзэмшүүлээгүй байх")
        _cap.release()

    # 5) ОС-ийн нэмэлт хэрэгсэл: аль үйлдэл ажиллах вэ
    print("  --- OS-iin nemelt herelse: alii uildel ajillana ---")
    if sys.platform.startswith("linux"):
        p = shutil.which("pactl")
        if p:
            print(f"  [OK]    pactl (DUU)               : {p}")
        else:
            print("  [TAANI]  pactl (DUU)               : suugaagui")
            print("          -> VOLUME MODE ajillahgui!")
            print("             Arch: sudo pacman -S libpulse")
            print("             Debian/Ubuntu: sudo apt install pulseaudio-utils")
        b = shutil.which("brightnessctl")
        if b:
            print(f"  [OK]    brightnessctl (GEREL)     : {b}")
        else:
            print("  [TAANI]  brightnessctl (GEREL)     : suugaagui")
            print("          -> BRIGHTNESS MODE ajillahgui!")
            print("             Arch: sudo pacman -S brightnessctl")
            print("             Debian/Ubuntu: sudo apt install brightnessctl")
            print("             (zonov buh baiheel dahiad ajillana)")
        x = shutil.which("xdotool") or shutil.which("wtype")
        if x:
            print(f"  [OK]    xdotool/wtype (SUM)       : {x}")
        else:
            print("  [TAANI]  xdotool/wtype (SUM)       : suugaagui")
            print("          -> ARROW MODE ajillahgui!")
            print("             X11:     sudo pacman -S xdotool")
            print("             Wayland: sudo pacman -S wtype")
    elif sys.platform == "win32":
        has_pycaw = (importlib.util.find_spec("pycaw") is not None
                     and importlib.util.find_spec("comtypes") is not None)
        if has_pycaw:
            print("  [OK]    pycaw/comtypes (DUU)      : суусан")
        else:
            print("  [TAANI]  pycaw/comtypes (DUU)      : suugaagui")
            print("          -> VOLUME MODE ajillahgui!")
            print("             pip install pycaw comtypes")
        if importlib.util.find_spec("pyautogui") is not None:
            print("  [OK]    pyautogui (SUM)           : суусан")
        else:
            print("  [TAANI]  pyautogui (SUM)           : suugaagui")
            print("          -> ARROW MODE ajillahgui!")
            print("             pip install pyautogui")
        print("  [TAANI]  GEREL                     : zovhon Linux d ajillana")
    else:  # macOS
        if shutil.which("osascript"):
            print("  [OK]    osascript (DUU)           : /usr/bin/osascript")
        else:
            print("  [TAANI]  osascript (DUU)           : oldoggui (macOS baih yostoi)")
            print("          -> VOLUME MODE ajillahgui!")
        if importlib.util.find_spec("pyautogui") is not None:
            print("  [OK]    pyautogui (SUM)           : суусан")
        else:
            print("  [TAANI]  pyautogui (SUM)           : suugaagui")
            print("          -> ARROW MODE ajillahgui!  pip install pyautogui")
        print("  [TAANI]  GEREL                     : zovhon Linux d ajillana")

    print(sep)
    if fatal:
        print("  DUTUU SHAARDLAMA:")
        for f in fatal:
            print(f"    - {f}")
        print(sep)
        return False
    print("  Bund buh UNDSEN shaardlaga hangagsan - ajillulj bolno!")
    print(sep)
    return True


def main():
    if not print_requirements():
        print(">> Shaardlagaanii dutugaar duusav.")
        return

    import arrowkey
    import brightness_control
    import volume_control

    ok_vol = volume_control.preflight()
    ok_bri = brightness_control.preflight()
    ok_arr = arrowkey.preflight()
    if not (ok_vol or ok_bri or ok_arr):
        print("Ali modul ch ajillahguyi baina.")
        return

    opts = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL),
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        min_hand_presence_confidence=0.5)
    landmarker = vision.HandLandmarker.create_from_options(opts)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not found")
        landmarker.close()
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIN_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WIN_H)

    volume = volume_control.get_volume_pct() if ok_vol else 0
    muted = volume_control.get_mute() if ok_vol else False
    bright = brightness_control.get_brightness_pct() if ok_bri else -1

    lock_pos = None
    lock_t = 0.0
    chosen_i = None

    mode = None
    arm_t0 = None
    arm2_t0 = None
    arm3_t0 = None
    pinch_arm_t0 = None

    prev_pinching = False
    pinch_t0 = 0.0
    pinch_y0 = None
    pinch_val0 = 0
    dragging = False
    drag_ref = 0.0

    arrow_ref = None
    arrow_dir = None
    arrow_t0 = None
    arrow_last = 0.0

    paused = False
    status = ""

    print(f"Start: vol={volume}% mute={muted} bright={bright}%")
    print("1 horuu = VOLUME | 2 horuu = BRIGHTNESS | 3 horuu / erxii+zungia pinch = ARROW")
    print("TAP/DRAG = hemjee | zangiin ur (8) hudulg = sum | space=pause | q=quit")

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = landmarker.detect(mp_image)
        h, w = frame.shape[:2]
        hands = result.hand_landmarks
        now = time.time()

        chosen_i = None
        if hands:
            if lock_pos is None:
                chosen_i = 0
            else:
                best_i, best_d = None, None
                for i, hd in enumerate(hands):
                    d = math.hypot(hd[0].x - lock_pos[0], hd[0].y - lock_pos[1])
                    if best_d is None or d < best_d:
                        best_i, best_d = i, d
                if best_d <= LOCK_MAX_DIST:
                    chosen_i = best_i
            if chosen_i is not None:
                lock_pos = (hands[chosen_i][0].x, hands[chosen_i][0].y)
                lock_t = now

        if lock_pos is not None and now - lock_t > LOCK_TIMEOUT_S:
            lock_pos = None
            prev_pinching = False
            dragging = False
            arrow_ref = None
            arrow_dir = None
            arrow_t0 = None

        if not paused:
            for i, hd in enumerate(hands):
                sel = (i == chosen_i)
                pts = [(int(p.x * w), int(p.y * h)) for p in hd]
                for a, b in HAND_BONES:
                    cv2.line(frame, pts[a], pts[b],
                             (255, 255, 0) if sel else (70, 70, 70),
                             2 if sel else 1)
                for j, (x, y) in enumerate(pts):
                    cv2.circle(frame, (x, y), 6 if sel else 4,
                               (0, 255, 0) if sel else (110, 110, 110), -1)
                    cv2.putText(frame, str(j), (x + 8, y - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255) if sel else (150, 150, 150), 1)

        if chosen_i is not None and not paused:
            lm = hands[chosen_i]
            nf = fingers_up_count(lm)
            thumb_a, index_a = lm[4], lm[8]
            pinch_hold = dist(thumb_a, index_a) < PINCH_DIST

            if pinch_hold and mode not in ("volume", "brightness"):
                arm_t0 = None
                arm2_t0 = None
                arm3_t0 = None
                if pinch_arm_t0 is None:
                    pinch_arm_t0 = now
                elif mode != "arrow" and now - pinch_arm_t0 >= ARM_HOLD_S:
                    mode = "arrow"
                    pinch_arm_t0 = None
                    prev_pinching = False
                    dragging = False
                    idx = lm[8]
                    arrow_ref = (idx.x, idx.y)
                    arrow_dir = None
                    arrow_t0 = None
                    arrow_last = now
                    status = "ARROW baina -> indeks horuu = up/down/left/right"
                    print(status)
            elif not pinch_hold:
                pinch_arm_t0 = None

            if pinch_hold:
                pass
            elif nf == 1:
                arm2_t0 = None
                arm3_t0 = None
                pinch_arm_t0 = None
                if arm_t0 is None:
                    arm_t0 = now
                elif mode != "volume" and now - arm_t0 >= ARM_HOLD_S:
                    mode = "volume"
                    arm_t0 = None
                    prev_pinching = False
                    dragging = False
                    arrow_ref = None
                    arrow_dir = None
                    arrow_t0 = None
                    status = "VOLUME baina -> PINCH (4+8) = TAP mute / DRAG = hemjee"
                    print(status)
            elif nf == 2:
                arm_t0 = None
                arm3_t0 = None
                pinch_arm_t0 = None
                if arm2_t0 is None:
                    arm2_t0 = now
                elif mode != "brightness" and now - arm2_t0 >= ARM_HOLD_S:
                    mode = "brightness"
                    arm2_t0 = None
                    prev_pinching = False
                    dragging = False
                    arrow_ref = None
                    arrow_dir = None
                    arrow_t0 = None
                    if bright < 0:
                        status = "brightness oldsongui (Linux + brightnessctl)"
                    else:
                        status = "BRIGHTNESS baina -> PINCH+DRAG = gerald"
                    print(status)
            elif nf == 3:
                arm_t0 = None
                arm2_t0 = None
                pinch_arm_t0 = None
                if arm3_t0 is None:
                    arm3_t0 = now
                elif mode != "arrow" and now - arm3_t0 >= ARM_HOLD_S:
                    mode = "arrow"
                    arm3_t0 = None
                    prev_pinching = False
                    dragging = False
                    idx = lm[8]
                    arrow_ref = (idx.x, idx.y)
                    arrow_dir = None
                    arrow_t0 = None
                    arrow_last = now
                    status = "ARROW baina -> indeks horuu = up/down/left/right"
                    print(status)
            else:
                arm_t0 = None
                arm2_t0 = None
                arm3_t0 = None

            if mode == "arrow":
                idx = lm[8]
                if arrow_ref is None:
                    arrow_ref = (idx.x, idx.y)
                dx = idx.x - arrow_ref[0]
                dy = idx.y - arrow_ref[1]
                if abs(dx) < ARROW_DEAD and abs(dy) < ARROW_DEAD:
                    arrow_dir = None
                    arrow_t0 = None
                else:
                    d = classify_arrow(dx * w, dy * h)
                    if d != arrow_dir:
                        arrow_dir = d
                        arrow_t0 = now
                    elif (arrow_t0 is not None
                          and now - arrow_t0 >= ARROW_HOLD_S
                          and now - arrow_last >= ARROW_COOLDOWN_S):
                        if arrowkey.press(d):
                            arrow_last = now
                            status = f"ARROW {d.upper()}"
                            print(status)
                        arrow_ref = (idx.x, idx.y)
                        arrow_dir = None
                        arrow_t0 = None

            if (mode == "volume" and ok_vol) or (mode == "brightness" and ok_bri):
                thumb, index = lm[4], lm[8]
                pinch = dist(thumb, index) < PINCH_DIST
                mid_y = (thumb.y + index.y) / 2

                if pinch and not prev_pinching:
                    pinch_t0 = now
                    pinch_y0 = mid_y
                    if mode == "volume":
                        pinch_val0 = volume
                    else:
                        pinch_val0 = bright if bright >= 0 else 0
                    drag_ref = 0.0
                    dragging = False
                elif pinch and prev_pinching:
                    disp = pinch_y0 - mid_y
                    if abs(disp) > DRAG_MIN:
                        dragging = True
                        if abs(disp - drag_ref) >= DRAG_STEP:
                            drag_ref = disp
                            target = pinch_val0 + int(disp * 300)
                            if mode == "volume":
                                volume = volume_control.set_volume_pct(target)
                                if muted:
                                    muted = volume_control.toggle_mute()
                                status = f"Vol {volume}%"
                            else:
                                nb = brightness_control.set_brightness_pct(target)
                                if nb is not None:
                                    bright = nb
                                status = f"Bright {bright}%"
                elif not pinch and prev_pinching:
                    held = now - pinch_t0
                    if mode == "volume" and (not dragging) and held < TAP_MAX_S:
                        muted = volume_control.toggle_mute()
                        status = f"MUTE -> {muted}"
                        print(status)

                prev_pinching = pinch

            if mode == "volume" and not prev_pinching:
                label = "MUTE  [TAP 4+8]" if muted else f"Vol {volume}%"
                cv2.putText(frame, label, (16, 32), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255) if muted else (0, 255, 0), 2)
                bar_x, bar_top, bar_bot = w - 30, 16, h - 16
                cv2.rectangle(frame, (bar_x, bar_top), (bar_x + 14, bar_bot),
                              (80, 80, 80), 2)
                fill_h = int((bar_bot - bar_top) * (0 if muted else volume) / 100)
                cv2.rectangle(frame, (bar_x, bar_bot - fill_h), (bar_x + 14, bar_bot),
                              (0, 0, 200) if muted else (0, 200, 0), -1)
            elif mode == "brightness" and not prev_pinching:
                label = f"Bright {bright}%"
                cv2.putText(frame, label, (16, 32), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 255), 2)
                bar_x, bar_top, bar_bot = w - 30, 16, h - 16
                cv2.rectangle(frame, (bar_x, bar_top), (bar_x + 14, bar_bot),
                              (80, 80, 80), 2)
                val = 0 if bright < 0 else bright
                fill_h = int((bar_bot - bar_top) * val / 100)
                cv2.rectangle(frame, (bar_x, bar_bot - fill_h), (bar_x + 14, bar_bot),
                              (200, 200, 0), -1)
            elif mode == "arrow":
                arrow_txt = arrow_dir.upper() if arrow_dir else ""
                cv2.putText(frame, f"ARROW {arrow_txt}", (16, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2)

        mode_txt = mode.upper() if mode else "NONE"
        lock_txt = "LOCK" if lock_pos is not None else "FREE"
        pause_txt = " PAUSED" if paused else ""
        cv2.putText(frame, f"MODE: {mode_txt}  [{lock_txt}]{pause_txt}",
                    (16, h - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (255, 255, 255), 2)
        if status and mode:
            cv2.putText(frame, status[:60], (16, 64),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow(WINDOW_NAME, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord(" "):
            paused = not paused

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()


if __name__ == "__main__":
    main()
