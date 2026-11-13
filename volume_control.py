import subprocess
import math
import os
import shutil
import sys
import time
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions

MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "models", "hand_landmarker.task")

WINDOW_NAME = "Volume Control (q=quit)"
WIN_W, WIN_H = 640, 480

# --- Tohirgoo ---
PINCH_DIST = 0.06   # 4+8 olon zuin olond pinch-n hamch
DRAG_MIN = 0.035    # eneээrs их niit hodelguun = uylguurt hodelguun (drag) gej tootsnoo
DRAG_STEP = 0.012   # chichrel uldeejuulah: eneээrs baga zailldagui bol hemjee uurchlugduhgui
TAP_MAX_S = 0.6     # TAP-h dryand eneээrs urt hugatsaa baihgui

# gar-iin uldegdeluud (0=wrist, 1-4 muur, 5-8 erxii, 9-12 duunii, 13-16 tsuuvii, 17-20 deluu)
HAND_BONES = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]


# --- Duu udirdah backend (platform-toos hamaarana) ---
if sys.platform == "win32":
    # --- Windows: pycaw (Windows Audio API) ---
    try:
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL
    except ImportError:
        print("pycaw suulgaagui baina:  pip install pycaw comtypes")
        sys.exit(1)

    _devices = AudioUtilities.GetSpeakers()
    _iface = _devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    _volume = _iface.QueryInterface(IAudioEndpointVolume)

    def get_volume_pct():
        return round(_volume.GetMasterVolumeLevelScalar() * 100)

    def set_volume_pct(pct):
        pct = max(0, min(100, pct))
        _volume.SetMasterVolumeLevelScalar(pct / 100.0, None)
        return pct

    def get_mute():
        return bool(_volume.GetMute())

    def toggle_mute():
        muted = not get_mute()
        _volume.SetMute(1 if muted else 0, None)
        return muted

elif sys.platform == "darwin":
    # --- macOS: osascript ---
    def get_volume_pct():
        out = subprocess.run(
            ["osascript", "-e", "output volume of (get volume settings)"],
            capture_output=True, text=True).stdout.strip()
        try:
            return int(float(out))
        except ValueError:
            return 0

    def set_volume_pct(pct):
        pct = max(0, min(100, pct))
        subprocess.run(["osascript", "-e",
                        f"set volume output volume {pct}"], check=False)
        return pct

    def get_mute():
        out = subprocess.run(
            ["osascript", "-e", "output muted of (get volume settings)"],
            capture_output=True, text=True).stdout.strip()
        return out == "true"

    def toggle_mute():
        muted = not get_mute()
        subprocess.run(["osascript", "-e",
                        f"set volume output muted {'true' if muted else 'false'}"],
                       check=False)
        return muted

else:
    # --- Linux: pactl (PulseAudio / PipeWire) ---
    def get_volume_pct():
        out = subprocess.run(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
            capture_output=True, text=True).stdout
        for token in out.split():
            if token.endswith("%"):
                return int(token[:-1])
        return 0

    def set_volume_pct(pct):
        pct = max(0, min(100, pct))
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{pct}%"],
                       check=False)
        return pct

    def get_mute():
        out = subprocess.run(
            ["pactl", "get-sink-mute", "@DEFAULT_SINK@"],
            capture_output=True, text=True).stdout
        return "yes" in out

    def toggle_mute():
        subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"],
                       check=False)
        return get_mute()


def preflight():
    """Ажиллахад шаардлагатай зүйлс байгаа эсэхийг шалгана."""
    if sys.platform == "darwin" and shutil.which("osascript") is None:
        print("osascript oldsongui (macOS baih yostoi)")
        return False
    if sys.platform.startswith("linux") and shutil.which("pactl") is None:
        print("pactl oldsongui: PulseAudio/ PipeWire suulgana uu")
        print("  Debian/Ubuntu:  sudo apt install pulseaudio-utils")
        return False
    return True


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def main():
    if not preflight():
        return

    opts = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL),
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    landmarker = vision.HandLandmarker.create_from_options(opts)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not found")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIN_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WIN_H)

    volume = get_volume_pct()
    muted = get_mute()
    prev_pinching = False
    prev_y = None
    pinch_t0 = 0.0        # pinch эхэлсэн цаг
    pinch_y0 = None       # pinch эхэлсэн байрлал
    pinch_vol0 = volume   # pinch эхэлсэн дууны хэмжээс
    dragging = False      # drag (хэмжээс өөрчлөлт) идэвхтэй эсэх
    drag_ref = 0.0        # хамгийн сүүлд хэрэглэсэн зай (hysteresis)
    print(f"Start volume: {volume}%  mute={muted}")
    print("TAP (4+8, хөдөлгөөнгүй) = duu nemeh/hasah | DRAG (4+8 дээш/доош) = hemjee | q=quit")

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = landmarker.detect(mp_image)

        if result.hand_landmarks:
            lm = result.hand_landmarks[0]
            h, w = frame.shape[:2]
            pts = [(int(p.x * w), int(p.y * h)) for p in lm]
            thumb, index = lm[4], lm[8]

            for a, b in HAND_BONES:
                cv2.line(frame, pts[a], pts[b], (255, 255, 0), 2)
            for i, (x, y) in enumerate(pts):
                cv2.circle(frame, (x, y), 6, (0, 255, 0), -1)
                cv2.putText(frame, str(i), (x + 8, y - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # 4 (bugee) + 8 (erxii) = pinch
            pinch = dist(thumb, index) < 0.06
            mid_y = (thumb.y + index.y) / 2
            now = time.time()

            if pinch and not prev_pinching:
                # pinch эхэллээ
                pinch_t0 = now
                pinch_y0 = mid_y
                pinch_vol0 = volume
                drag_ref = 0.0
                dragging = False
            elif pinch and prev_pinching:
                # ХУРИМТЛАЛГҮЙ: эхлэх байрлалаас хэр зэрэг холдсонаар шууд тооцно.
                # Ингэхээр хугацаа өнгөрөх тусам гажилт хуримтлагдахгүй.
                disp = pinch_y0 - mid_y          # (+ = дээш хөдөлсөн)
                if abs(disp) > DRAG_MIN:         # deadband: чичрэлээс доош = үл тооцно
                    dragging = True
                    # Hysteresis: сүүлд хэрэглэсэнээс DRAG_STEP-эр холдоогүй бол
                    # дахин тохируулахгүй -> чичрэлээс flip хийхгүй.
                    if abs(disp - drag_ref) >= DRAG_STEP:
                        drag_ref = disp
                        target = pinch_vol0 + int(disp * 300)
                        if target != volume:
                            volume = set_volume_pct(target)
                            if muted:
                                muted = toggle_mute()
            elif not pinch and prev_pinching:
                # pinch тайрах -> TAP эсэхийг шийднэ
                held = now - pinch_t0
                if (not dragging) and held < TAP_MAX_S:
                    # ХӨДӨЛГӨӨНГҮЙ, ХУРГАН = TAP -> duu nemeh/hasah
                    muted = toggle_mute()
                    print(f"MUTE -> {muted}")

            prev_pinching = pinch
            prev_y = mid_y

            if muted:
                label = "MUTE  [TAP 4+8]"
                col = (0, 0, 255)
            else:
                label = f"Vol {volume}%"
                col = (0, 255, 0)
            if pinch:
                label += " [DRAG]" if dragging else " [PINCH]"
            cv2.putText(frame, label, (16, 32), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, col if pinch else (255, 255, 255), 2)

            bar_x, bar_top, bar_bot = w - 30, 16, h - 16
            cv2.rectangle(frame, (bar_x, bar_top), (bar_x + 14, bar_bot),
                          (80, 80, 80), 2)
            fill_h = int((bar_bot - bar_top) * (0 if muted else volume) / 100)
            cv2.rectangle(frame, (bar_x, bar_bot - fill_h), (bar_x + 14, bar_bot),
                          (0, 0, 200) if muted else (0, 200, 0), -1)

        cv2.imshow(WINDOW_NAME, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()


if __name__ == "__main__":
    main()
