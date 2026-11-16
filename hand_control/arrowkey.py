import os
import shutil
import subprocess
import sys


_KEYS = {
    "up": ("Up", "Up"),
    "down": ("Down", "Down"),
    "left": ("Left", "Left"),
    "right": ("Right", "Right"),
}


def session_type():
    """Идэвхтэй display-server / window manager-ийн төрөл.

    Linux дээр XDG_SESSION_TYPE (gdm/sddm/lightdm-ээр дамжсан) эсвэл
    WAYLAND_DISPLAY / DISPLAY-аас тогтооно:
      "x11" | "wayland" | "todorhoigui"
    """
    if not sys.platform.startswith("linux"):
        return sys.platform
    st = os.environ.get("XDG_SESSION_TYPE", "").strip().lower()
    if st in ("x11", "wayland"):
        return st
    # Session бүртгэлгүй (ssh, tty) ч environment-аас унших боломжтой
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    return "todorhoigui"


def backend():
    """Энэ session-д ажиллах сумын хэрэгсэл.

    - wayland (wlroots/Mutter/KWin/Sway...)  -> wtype
    - x11 (i3/Sway-X11/Xfce/KDE-X11...)      -> xdotool
    - session тодорхойгүй                    -> аль нь байгаа нь
    Тухайн хэрэгсэл алга бол нөгөөг нь нөхцөл болгон авна.
    """
    if not sys.platform.startswith("linux"):
        return "pyautogui"
    xdo = shutil.which("xdotool")
    wt = shutil.which("wtype")
    sess = session_type()
    if sess == "wayland":
        if wt:
            return "wtype"
        if xdo:
            return "xdotool"
        return None
    if sess == "x11":
        if xdo:
            return "xdotool"
        if wt:
            return "wtype"
        return None
    # Session тодорхойгүй: аль нь байгаа нь
    if xdo:
        return "xdotool"
    if wt:
        return "wtype"
    return None


def preflight():
    if sys.platform.startswith("linux"):
        sess = session_type()
        be = backend()
        if be is None:
            print(f"SUM tovch oldsongui (session: {sess}):")
            print("  X11:     sudo pacman -S xdotool  /  sudo apt install xdotool")
            print("  Wayland: sudo pacman -S wtype     /  sudo apt install wtype")
            return False
        # Session болон хэрэгсэл таарахгүй бол анхааруулна
        if sess == "wayland" and be == "xdotool":
            print("Anhaaruulga: WAYLAND session d baina, xdotool zovhon XWayland")
            print("  programd l ajillana. Dew: sudo pacman -S wtype (Wayland tovch)")
        elif sess == "x11" and be == "wtype":
            print("Anhaaruulga: X11 session d baina, wtype Wayland-d zoriulsan;")
            print("  X11 deer ajillahgui. Dew: sudo pacman -S xdotool")
        return True
    # Windows / macOS: pyautogui heregtei
    try:
        import pyautogui  # noqa: F401
        return True
    except ImportError:
        print("pyautogui oldsongui (sum tovch): pip install pyautogui")
        return False


def press(direction):
    if direction not in _KEYS:
        return False
    key = _KEYS[direction][0 if sys.platform.startswith("linux") else 1]
    be = backend()
    if be == "xdotool":
        subprocess.run(["xdotool", "key", "--clearmodifiers", key], check=False)
        return True
    if be == "wtype":
        subprocess.run(["wtype", "-k", key], check=False)
        return True
    if be == "pyautogui":
        try:
            import pyautogui
            pyautogui.press(key.lower() if key != "Up" else "up")
            return True
        except Exception as e:
            print(f"pyautogui aldaa: {e}")
            return False
    return False
