import shutil
import subprocess
import sys


def _run(args):
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=2)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def preflight():
    if not sys.platform.startswith("linux"):
        print("GEREL tohiruulah ni zovhon Linux (brightnessctl) d ajillana.")
        return False
    if shutil.which("brightnessctl") is None:
        print("brightnessctl oldsongui:")
        print("  Arch:   sudo pacman -S brightnessctl")
        print("  Debian: sudo apt install brightnessctl")
        print("  (zonov buh baiheel dahiad ajillana)")
        return False
    return True


def get_brightness_pct():
    if shutil.which("brightnessctl") is None:
        return None
    out = _run(["brightnessctl", "-m"])
    if not out:
        return None
    for token in out.split(","):
        token = token.strip()
        if token.endswith("%"):
            try:
                return int(token[:-1])
            except ValueError:
                continue
    out = _run(["brightnessctl", "get"])
    mx = _run(["brightnessctl", "max"])
    try:
        return int(int(out) * 100 / int(mx))
    except (ValueError, ZeroDivisionError):
        return None


def set_brightness_pct(pct):
    pct = max(1, min(100, int(pct)))
    if shutil.which("brightnessctl") is None:
        return None
    _run(["brightnessctl", "set", f"{pct}%"])
    return get_brightness_pct()


def apply_delta(delta_steps, step=5):
    cur = get_brightness_pct()
    if cur is None:
        return None
    return set_brightness_pct(cur + delta_steps * step)
