# 🖐️ Gesture-controlled-Operating-System

Камер дээрх гарын хөдөлгөөнөөр компьютерийн дууны хэмжээг удирдах төсөл.
Машин сургалт (MediaPipe) ашиглан гарын 21 цэгийг баримтлан, доошлүүлэх/дээшлүүлэх,
таг мэт хийснээр унтрааж-аших боломжтой юм.

## ✨ Онцлогууд

- 📷 Вебкамерээр гарыг илрүүлэн, бүрэн скелет, **кадр бүрийн индекс дугаартай** (0–20) зурж харуулна
- 🤏 **PINCH + чирэлт** — эрхий (4) болон зангиа (8) хүрээгээ хавчсан хэвээрээ дээш/доош хөдөлгөхөд дууны хэмжээ өөрчлөгдөнө
- 👆 **TAP** — хавчлагаа хөдөлгөөнгүйгээр хурдан тайлахад дуу унтраах/асах (mute toggle)
- 📊 Дэлгэц дээр дууны хэмжээний самбар, одоогийн төлөвийг шууд харуулна
- ⚙️ Чичрэлээс хамааралгүй тогтвортой ажиллахаар (deadband + hysteresis) тооцоологдсон
- 💻 **Linux (Arch / Debian / Fedora), Windows (шууд болон WSL), macOS** дээр ажиллана

## 🖐️ Гарын дохилтууд

| Дохиолол | Хийх хөдөлгөөн | Үр дүн |
|---|---|---|
| **TAP** | Эрхий (4) болон зангиа (8) хүрээгээ хавчаад, **0.6 секундын дотор** хөдөлгөөнгүйгээр тайлах | Дуу унтраах / асаах |
| **DRAG** | Хавчлагаа хадгалсан хэвээрээ гараа **дээш/доош** хөдөлгөх | Дууны хэмжээ нэмэгдэх/хасах |

> Хавчсан ч чирэхгүй (хэт богино хугацаанд тайлавал) = TAP,
> хавчсан ч дээш/доош хөдөлгөвөл = DRAG гэж тооцогдоно.

## 💻 Шаардлага

- ОС: **Linux** (PulseAudio / PipeWire), **Windows 10/11** (шууд эсвэл WSL), **macOS**
- Python **3.10+**
- Вебкамер (default camera, index 0)
- Python номын сангууд: `opencv-python`, `mediapipe`
  - Linux/WSL дээр **нэмэлтээр `pactl`** хэрэгтэй (доорх хэсэгт суулгана)
  - Windows дээр `pycaw`, `comtypes` (суулгагдаагүй бол алдаа өгөөд зогсоно)
- Загвар файл `models/hand_landmarker.task` **төсөлд багтсан** — татаж авах шаардлагагүй

## 📖 Агуулга

- [🐧 Linux](#-linux)
  - [Arch Linux / Manjaro / CachyOS](#arch-linux--manjaro--cachyos)
  - [Debian / Ubuntu](#debian--ubuntu)
  - [Fedora](#fedora)
- [🍎 macOS](#-macos)
- [🪟 Windows](#-windows)
  - [Шууд суулгаж ажиллуулах](#шууд-суулгаж-ажиллуулах-powershell)
  - [WSL дээр (Windows Subsystem for Linux)](#wsl-дээр-windows-subsystem-for-linux)
- [⚙️ Тохиргоо](#-тохиргоо)
- [📁 Төслийн бүтэц](#-төслийн-бүтэц)
- [🛠️ Ажилладаг зарчим](#-ажилладаг-зарчим)
- [🔧 Асуудал шийдвэрлэх](#-асуудал-шийдвэрлэх)

## 🚀 Ажиллуулах заавар

> Бүх платформ дээр **эхлээд** кодыг татаж авна:
> ```bash
> git clone https://github.com/Zaprilli/Gesture-controlled-Operating-System.git
> cd Gesture-controlled-Operating-System
> ```

### 🐧 Linux

```bash
# 1. Virtual environment үүсгэнэ (зөвлөмж)
python3 -m venv .venv
source .venv/bin/activate

# 2. Номын сангуудыг суулгана
pip install -r requirements.txt

# 3. `pactl` суулгана (дууны хэмжээг удирдахад шаардлагатай) — тухайн дистрибуциас:
```

#### Arch Linux / Manjaro / CachyOS

```bash
sudo pacman -S libpulse          # pactl -г олгодог
# PipeWire ашиглаж байвал (ихэнх шинэ системд):
sudo pacman -S pipewire-pulse
```

Хянах: `pactl --version` ажиллавал болно. Дуугүй систем дээр `pipewire-pulse`
суулгасны дараа `systemctl --user restart pipewire-pulse` гүйцэтгэнэ үү.

#### Debian / Ubuntu

```bash
sudo apt install pulseaudio-utils    # pactl
```

#### Fedora

```bash
sudo dnf install pulseaudio-utils    # pactl
```

#### Хэрэгжүүлнэ

```bash
python volume_control.py
```

Дэлгэцэнд камерын зураг, гарын скелет (индекс дугаартай) болон дууны хэмжээний
самбар харагдана. Гарахын тулд терминалд `q` дарна уу.

> 💡 **KDE / GNOME (Wayland)** дээр ийм warning гарч болно —
> `Could not find the Qt platform plugin "wayland"`.
> Цонх **гарч л байвал асуудалгүй** (OpenCV `xcb` руу буцаад унадаг).
> Урьдчилан дарахын хүсвэл:
> ```bash
> QT_QPA_PLATFORM=xcb python volume_control.py
> ```

### 🍎 macOS

```bash
# 1. Virtual environment үүсгэнэ (зөвлөмж)
python3 -m venv .venv
source .venv/bin/activate

# 2. Номын сангуудыг суулгана
pip install -r requirements.txt

# 3. Хэрэгжүүлнэ
python volume_control.py
```

> 🍎 macOS дээр анх удаа ажиллуулахад **камерын зөвшөөрөл** асуух тул
> `System Settings → Privacy & Security → Camera`-аас зөвшөөрнө үү.
> Дууны хэмжээ `osascript`-аар (Core Audio) удирдагдана.

### 🪟 Windows

Windows дээр **хоёр зам** байна:

| Зам | Хэзээ сонгох вэ |
|---|---|
| **Шууд суулгах** | Энгийн — камерын зөв асуудалгүй, нэг л орчин шаардлагагүй (**зөвлөмж**) |
| **WSL** | Linux-ийн орчин (bash, pip, скриптүүд) хэрэгтэй бол |

#### Шууд суулгаж ажиллуулах (PowerShell)

```powershell
# 1. Кодоо татаж авна
git clone https://github.com/Zaprilli/Gesture-controlled-Operating-System.git
cd Gesture-controlled-Operating-System

# 2. Virtual environment үүсгэнэ (зөвлөмж)
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Номын сангуудыг суулгана (pycaw, comtypes автоматаар сууна)
pip install -r requirements.txt

# 4. Хэрэгжүүлнэ
python volume_control.py
```

> ⚠️ PowerShell дээр `Activate.ps1` алдаа гарвал (execution policy):
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
> командийг эхлээд гүйцэтгэнэ үү.

#### WSL дээр (Windows Subsystem for Linux)

WSL нь анхдагчаа **камерыг хардаггүй** — камерыг Windows-оос WSL рүү дамжуулах
(passthrough) хэрэгтэй. Дууны хувьд **WSLg** (Windows 11) PulseAudio-ийг дэмждэг.

**1. WSL суулгах** (Windows PowerShell дээр):

```powershell
wsl --install -d Ubuntu
wsl --update
```

Дараа `wsl --shutdown` гэж бичээд WSL-ийг дахин нээнэ үү.

**2. Камерыг WSL рүү дамжуулах** (`usbipd-win` ашиглах):

```powershell
winget install --id dorssel.usbipd-win   # нэг удаа суулгана
usbipd list                               # камерын BUSID-ийг олно ("Integrated Webcam" гэх мэт)
usbipd bind --busid <BUSID>              # нэг удаа (админ шаардлагатай)
usbipd attach --wsl --busid <BUSID>      # WSL рүү холбоно
```

WSL дээр шалгах:

```bash
ls /dev/video*        # /dev/video0 гарч ирвэл боллоо
```

> ⚠️ Компьютер **sleep-ээс буцаад** ирвэл камерыг дахин холбох хэрэгтэй:
> Windows PowerShell дээр дахин `usbipd attach --wsl --busid <BUSID>`.

**3. WSL дээр суулгаж ажиллуулах** (Ubuntu жишээ):

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip pulseaudio-utils v4l-utils

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python volume_control.py
```

> 🪟 **WSLg** (Windows 11) дээр OpenCV-ийн цонх автоматаар гарна.
> Windows 10 дээр WSLg байхгүй тул X-сэрвэр (VcXsrv / X410) суулгах шаардлагатай.
>
> 📷 Камер нэгэн зэрэг **нэг л** процесст хамаарна — Windows Teams/Zoom
> зэргээр ашиглаж байвал WSL-д нээгдэхгүй. Эхлээгээ хаана уу.

## ⚙️ Тохиргоо

`volume_control.py` эхэнд дараах хувьсагчдыг өөрчилж болно:

| Хувьсагч | Утга | Тайлбар |
|---|---|---|
| `PINCH_DIST` | `0.06` | Эрхий болон зангиа хүрээ хэдий дээр ойрчихвол хавчлага гэж үзэх вэ |
| `DRAG_MIN` | `0.035` | Үүнээс бага хөдөлгөөн = чичрэл гэж тооцохгүй (**deadband**) |
| `DRAG_STEP` | `0.012` | Дууны хэмжээ солигдох алхам (**hysteresis** — чичрэлээс flip хийхгүй) |
| `TAP_MAX_S` | `0.6` | TAP гэж үзэх хамгийн их хугацаа (секунд) |
| `WIN_W`, `WIN_H` | `640`, `480` | Камерийн авалт болон цонхны хэмжээ |

## 📁 Төслийн бүтэц

```
.
├── volume_control.py            # Гол программын код (Linux/Windows/macOS/WSL)
├── requirements.txt             # Шаардлагатай Python номын сангууд
├── models/
│   └── hand_landmarker.task     # MediaPipe гар илрүүлэх загвар (git-д багтсан)
├── README.md                    # Энэ файл
└── .gitignore
```

## 🛠️ Ажилладаг зарчим

1. `OpenCV` вебкамераас 640×480 кадрыг авна
2. `MediaPipe Hand Landmarker` загвар гарын 21 цэгийг баримтлана
3. Эрхий хүрээ (4) + зангиа хүрээ (8)-ийн зайг тооцно
   - Зай нь `PINCH_DIST`-ээс бага байвал **хавчлага (pinch)** эхэлсэн гэж үзнэ
   - Хавчлага эхлэх байрлалаас `DRAG_MIN`-ээс ихээр холдсон бол = **DRAG**
   - Хавчлага `TAP_MAX_S`-ээс бага хугацаанд, хөдөлгөөнгүй тайлагдвал = **TAP**
4. Үр дүнгээ тухайн платформын дууны API-рүү шууд хүргэнэ:
   - **Linux / WSL** → `pactl` (PulseAudio / PipeWire)
   - **Windows** → `pycaw` (Windows Audio Core API)
   - **macOS** → `osascript` (Core Audio)

### Чичрэлээс хамгаалах (deadband + hysteresis)

Гарыг удаан барихад жижиг чичрэлээс болж хэмжээс гажихгүйн тулд хоёр шүүлтүүр ашиглана:

- **Deadband** (`DRAG_MIN`) — эхлэх байрлалаас үүнээс бага холдоогүй бол *нягтхан* гэж үзэж тооцохгүй
- **Hysteresis** (`DRAG_STEP`) — сүүлд хэрэглэсэн утгаас үүнээс бага зөрөөгөөр байвал дахин тохируулахгүй

Мөн тооцоог **хуримтлалгүйгээр** (`disp = эхлэх_y − одоогийн_y`) хийдэг тул хугацаа
өнгөрөх тусам гажилт цуглардаггүй.

## 🔧 Асуудал шийдвэрлэх

### 🐧 Linux

#### `Camera not found`

1. Камер ашиглаж буй өөр процесс байгаа эсэхийг шалгаа уу — **нэгэн зэрэг нэг л
   процесс камер эзэмших боломжтой**:
   ```bash
   fuser -v /dev/video0
   ```
   Хэрэв процесс гарч ирвэл түүнийг `q` дарж зогсооно уу.

2. Камерын эрх шалгаа уу:
   ```bash
   ls -l /dev/video*
   getfacl -p /dev/video0
   ```
   - Групп нь `video` байх ёстой. Өөрийгөө нэмэх:
     ```bash
     sudo usermod -aG video $USER
     ```
     Дараа **сессиондаа дахин нэвтэрнэ** үү (logout/login эсвэл шинээр ачаална).
   - `getfacl`-д `user:<та>:rw-` байвал аль хэдийн эрхтэй.

3. Камерын бодит чадварыг харах (зарим нь 60 FPS дэмжихгүй):
   ```bash
   v4l2-ctl -d /dev/video0 --all
   ```

#### `pactl: command not found`

`pactl` суулгагдаагүй байна — тухайн дистрибуциас суулгана уу:

| Дистрибуци | Команд |
|---|---|
| Arch / Manjaro / CachyOS | `sudo pacman -S libpulse` |
| Debian / Ubuntu | `sudo apt install pulseaudio-utils` |
| Fedora | `sudo dnf install pulseaudio-utils` |

#### Дууны хэмжээ өөрчлөгдөхгүй

- Зөв **sink** сонгогдсон эсэх: `pactl get-sink-volume @DEFAULT_SINK@`
- PipeWire ашиглаж байвал `pipewire-pulse` суулгасан эсэхийг шалгаа уу
  (`sudo pacman -S pipewire-pulse`), дараа нь:
  ```bash
  systemctl --user restart pipewire-pulse
  ```

#### `Could not find the Qt platform plugin "wayland"`

Цонх **гарч байвал энэ зүгээр warning** — асуудалгүй. Цонх гарахгүй бол:

```bash
sudo pacman -S qt6-wayland    # KDE/Qt6 дээр (хэрэв шаардлагатай бол)
QT_QPA_PLATFORM=xcb python volume_control.py
```

`xcb` (XWayland) ашиглах нь илүү найдвартай — OpenCV-гийн багцанд **зөвхөн `xcb`
plugin** агуулагддаг.

#### `ModuleNotFoundError: No module named 'cv2'`

Эхлээд virtual environment-ийг идэвхжүүлсэн эсэхийг шалгаа уу:

```bash
source .venv/bin/activate      # эсвэл: source .venv/bin/activate.fish
pip install -r requirements.txt
```

VS Code дээр ажиллавал `Ctrl+Shift+P` → **Python: Select Interpreter** →
`.venv/bin/python` (эсвэл таны venv-ийн python) -ийг сонгоно уу.

### 🪟 Windows / WSL

#### WSL дээр `/dev/video*` гарахгүй байна

Камер WSL рүү дамжуулагдаагүй байна:

1. `usbipd-win` суулгагдсан эсэх: Windows PowerShell дээр `usbipd --version`
2. Камер **attached** эсэхийг шалгах:
   ```powershell
   usbipd list        # State нь "Attached" байх ёстой
   ```
3. Дахин холбох:
   ```powershell
   wsl --update
   wsl --shutdown     # дараа WSL-ийг дахин нээ
   usbipd attach --wsl --busid <BUSID>
   ```
4. WSL дээр `lsusb` дээр камерын нэр гарч байна уу, `ls /dev/video*` шалгана уу.
5. Хэрэв `Attached` байгаа ч `/dev/video*` байхгүй бол **WSL-ийн kernel шинэчлэх**
   шаардлагатай: Windows дээр `wsl --update`, дараа `wsl --shutdown`.
6. Камер **Windows-аар нээгдсэн** байж магадгүй (Teams/Zoom/бусад) — тэдгээрийг хаана уу.

#### WSL дээр `pactl` ажиллахгүй байна

```bash
sudo apt install pulseaudio-utils
pactl info          # "Server String: ... pulse/native" гарвал WSLg аудио идэвхтэй
```

Windows 10 дээр WSLg байхгүй тул **WSL-ийг Windows 11 рүү шилжүүл** эсвэл
програмыг Windows-д шууд суулгаарай (доорх "Шууд суулгаж ажиллуулах" хэсэг).

#### Windows дээр `pycaw` алдаа өгч байна

```powershell
pip install pycaw comtypes
python volume_control.py
```

`requirements.txt`-ээс суулгаж байсан бол `pycaw` автоматаар суух ёстой.

#### Цонх (OpenCV window) гарахгүй байна

- **Windows шууд:** `python volume_control.py` ажиллуулахдаа **ана/терминал**
  цонхны дотор байгаа эсэхийг шалгана уу (Python-ийн IDLE цонх дээр `q` дарах
  боломжгүй — терминал ашиглана).
- **WSL (Windows 10):** WSLg байхгүй — VcXsrv суулгаад `export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0`.

### 🍎 macOS

#### Камерын зөвшөөрөл асуугдаж байна / камерыг харахгүй байна

`System Settings → Privacy & Security → Camera`-аас терминалд (Terminal / iTerm /
VS Code) **зөвшөөрөл** өгнө үү. Дараа терминалыг бүрэн хаад дахин нээнэ.

#### Дууны хэмжээ өөрчлөгдөхгүй байна

`osascript` System Events-д хандах эрх шаардаж магадгүй —
`System Settings → Privacy & Security → Automation`-аас шалгана уу.
Турших: `osascript -e "set volume output volume 50"`.

## 📜 Лиценз

Энэхүү төсөлд лиценз нэмээгүй байна. Ашиглахдаа зохиогчийн эрхийг хүндлэнэ үү.
