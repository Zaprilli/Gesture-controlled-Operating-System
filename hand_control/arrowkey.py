import shutil
import subprocess
import sys


_KEYS = {
    "up": ("Up", "Up"),
    "down": ("Down", "Down"),
    "left": ("Left", "Left"),
    "right": ("Right", "Right"),
}


def preflight():
    if sys.platform.startswith("linux"):
        if shutil.which("xdotool") or shutil.which("wtype"):
            return True
        print("xdotool/wtype oldsongui (sum tovch):")
        print("  X11:     sudo pacman -S xdotool  /  sudo apt install xdotool")
        print("  Wayland: sudo pacman -S wtype")
        return False
    # Windows / macOS: pyautogui heregtei
    try:
        import pyautogui  # noqa: F401
        return True
    except ImportError:
        print("pyautogui oldsongui (sum tovch): pip install pyautogui")
        return False


def _backend():
    if sys.platform.startswith("linux"):
        if shutil.which("xdotool"):
            return "xdotool"
        if shutil.which("wtype"):
            return "wtype"
        return None
    return "pyautogui"


def press(direction):
    if direction not in _KEYS:
        return False
    key = _KEYS[direction][0 if sys.platform.startswith("linux") else 1]
    be = _backend()
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
