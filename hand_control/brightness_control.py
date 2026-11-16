import shutil
import subprocess
import sys

# Платформыг ЗӨВХӨН ачааллагдах үед тогтооно: бүх branch (darwin/else) үүгээр
# шийдвэрлэгдэх тул available()/preflight() ч адил байх ёстой.
_PLATFORM = sys.platform


def _run(args):
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=2)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


if _PLATFORM == "darwin":
    # --- macOS: DOTOOD delegeriin gerel (nemelt suulgahgui) ---
    # Private framework-uudiig runtime-aar neene (symbol baihgui bol aldaa bish):
    #   1) DisplayServices - Apple Silicon + Intel (gol herelse)
    #   2) CoreDisplay     - Intel Mac (noots)
    import ctypes

    _mac = {"disp": None, "get": None, "set": None}

    def _mac_init():
        if _mac["get"] is not None:
            return True
        if _mac["disp"] is not None:
            return False  # urd n amjiltdgu bolson (davtan shalgahgui)

        # Gol delegeriin ID (CGMainDisplayID)
        disp = None
        for path in ("/System/Library/Frameworks/ApplicationServices.framework"
                     "/ApplicationServices",
                     "/System/Library/Frameworks/CoreGraphics.framework"
                     "/CoreGraphics"):
            try:
                lib = ctypes.CDLL(path)
                lib.CGMainDisplayID.restype = ctypes.c_uint32
                disp = int(lib.CGMainDisplayID())
                break
            except (OSError, AttributeError):
                continue
        if disp is None:
            _mac["disp"] = 0
            return False

        # 1) DisplayServices (private framework - shinen delgeeruud)
        try:
            ds = ctypes.CDLL(
                "/System/Library/PrivateFrameworks/"
                "DisplayServices.framework/DisplayServices")
            _get = ds.DisplayServicesGetBrightness
            _get.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_float)]
            _get.restype = ctypes.c_int
            _set = ds.DisplayServicesSetBrightness
            _set.argtypes = [ctypes.c_uint32, ctypes.c_float]
            _set.restype = ctypes.c_int

            def get():
                out = ctypes.c_float()
                if _get(disp, ctypes.byref(out)) != 0:
                    raise OSError("DisplayServicesGetBrightness")
                return float(out.value)

            def set_(v):
                if _set(disp, float(v)) != 0:
                    raise OSError("DisplayServicesSetBrightness")

            _mac.update(disp=disp, get=get, set=set_)
            return True
        except (OSError, AttributeError):
            pass

        # 2) CoreDisplay (Intel Mac-d gol ni; Apple Silicon d ajillahgui)
        try:
            cd = ctypes.CDLL(
                "/System/Library/Frameworks/CoreDisplay.framework/CoreDisplay")
            _get = cd.CoreDisplay_Display_GetUserBrightness
            _get.argtypes = [ctypes.c_uint32]
            _get.restype = ctypes.c_double
            _set = cd.CoreDisplay_Display_SetUserBrightness
            _set.argtypes = [ctypes.c_uint32, ctypes.c_double]
            _set.restype = None

            def get():
                return float(_get(disp))

            def set_(v):
                _set(disp, float(v))

            _mac.update(disp=disp, get=get, set=set_)
            return True
        except (OSError, AttributeError):
            pass

        _mac["disp"] = disp  # ID baina, gehdee framework/symbol oldooggui
        return False

    def get_brightness_pct():
        if not _mac_init():
            return None
        try:
            v = _mac["get"]()
        except (OSError, AttributeError, ValueError):
            return None
        if not 0.0 <= v <= 1.0:
            return None
        return max(0, min(100, round(v * 100)))

    def set_brightness_pct(pct):
        pct = max(1, min(100, int(pct)))
        if not _mac_init():
            return None
        try:
            _mac["set"](pct / 100.0)
        except (OSError, AttributeError, ValueError):
            return None
        return get_brightness_pct()

else:
    # --- Linux (brightnessctl); Windows deer gerel demjigdehgui ---
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


def available():
    """Gerel tohiruulah bolomjtoi eseh (medeelel helbelergui)."""
    if _PLATFORM.startswith("linux"):
        return shutil.which("brightnessctl") is not None
    if _PLATFORM == "darwin":
        return _mac_init()
    return False


def preflight():
    if available():
        return True
    if _PLATFORM.startswith("linux"):
        print("brightnessctl oldsongui:")
        print("  Arch:   sudo pacman -S brightnessctl")
        print("  Debian: sudo apt install brightnessctl")
        print("  (zonov buh baiheel dahiad ajillana)")
    elif _PLATFORM == "darwin":
        print("macOS-iin GEREL oldsongui:")
        print("  Zovhon DOTOOD deleger (MacBook/iMac) l demjigdene.")
        print("  Gadnaad monitor-iig macOS-uulaa demjihgui; macOS")
        print("  shinechlegdelereer private API haagdval ajillahgui.")
    else:
        print("GEREL: zovhon Linux (brightnessctl) / macOS (dotood deleger)")
        print("       d ajillana.")
    return False


def apply_delta(delta_steps, step=5):
    cur = get_brightness_pct()
    if cur is None:
        return None
    return set_brightness_pct(cur + delta_steps * step)
