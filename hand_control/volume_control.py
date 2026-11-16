import math
import shutil
import subprocess
import sys


if sys.platform == "win32":
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
        pct = max(0, min(100, int(pct)))
        _volume.SetMasterVolumeLevelScalar(pct / 100.0, None)
        return pct

    def get_mute():
        return bool(_volume.GetMute())

    def toggle_mute():
        muted = not get_mute()
        _volume.SetMute(1 if muted else 0, None)
        return muted

elif sys.platform == "darwin":
    def get_volume_pct():
        out = subprocess.run(
            ["osascript", "-e", "output volume of (get volume settings)"],
            capture_output=True, text=True).stdout.strip()
        try:
            return int(float(out))
        except ValueError:
            return 0

    def set_volume_pct(pct):
        pct = max(0, min(100, int(pct)))
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
    def get_volume_pct():
        out = subprocess.run(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
            capture_output=True, text=True).stdout
        for token in out.split():
            if token.endswith("%"):
                return int(token[:-1])
        return 0

    def set_volume_pct(pct):
        pct = max(0, min(100, int(pct)))
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
    if sys.platform == "darwin" and shutil.which("osascript") is None:
        print("osascript oldsongui (macOS baih yostoi)")
        return False
    if sys.platform.startswith("linux") and shutil.which("pactl") is None:
        print("pactl oldsongui: PulseAudio/PipeWire suulgana uu")
        print("  Arch:     sudo pacman -S libpulse")
        print("  Debian:   sudo apt install pulseaudio-utils")
        return False
    return True


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)
