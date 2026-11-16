# 🖐️ Gesture-controlled-Operating-System

Камер дээрх гарын хөдөлгөөнөөр компьютерийг удирдах төсөл.
MediaPipe Hand Landmarker ашиглан гарын **21 цэгийг** (0–20) баримтлан:

- **дууны хэмжээ** — чимхэлт + чирэлт (DRAG)
- **дуу таглах / асаах** (mute) — хурдан чимхэлт (TAP)
- **дэлгэцийн гэрэл** — чирэлтээр тохируулах
- **сумын товч** (↑ ↓ ← →) — индекс хуруугаар хөдөлгөнө

Программ **эхлэхэдээ шаардлагатай бүх зүйлийг шалгаж хэвлэнэ** (Python хувилбар,
номын сан, загвар, камер, ОС-ийн хэрэгсэл) — алийг нь суулгаагүй байвал тухайн
үйлдэл ажиллахгүйгээр нь яг тодорхой зааж өгнө.

## 📖 Агуулга

- [✨ Онцлогууд](#-онцлогууд)
- [🖐️ Гарын дохилтууд](#-гарын-дохилтууд)
- [💻 Шаардлага](#-шаардлага)
- [🚀 Ажиллуулах заавар](#-ажиллуулах-заавар)
  - [🪟 Windows](#-windows)
  - [🪟 WSL (Windows Subsystem for Linux)](#-wsl-windows-subsystem-for-linux)
  - [🐧 Linux](#-linux)
  - [📦 Oracle VM VirtualBox дээр Linux](#-oracle-vm-virtualbox-дээр-linux)
  - [🍎 macOS](#-macos)
  - [▶️ Эхлэлтийн тайлан](#-эхлэлтийн-тайлан)
- [⚙️ Тохиргоо](#-тохиргоо)
- [📁 Төслийн бүтэц](#-төслийн-бүтэц)
- [🛠️ Ажилладаг зарчим](#-ажилладаг-зарчим)
- [🔧 Асуудал шийдвэрлэх](#-асуудал-шийдвэрлэх)
- [📜 Лиценз](#-лиценз)

## ✨ Онцлогууд

- 📷 Вебкамерээр гарыг илрүүлэн, бүрэн скелет **индекс дугаартай** (0–20) зурж харуулна
- 🖐️ **Гар LOCK** — анх илрүүлсэн гар л удирдлагаа; 2 гар нэвтрэхэд сонгосон гар
  ногоон, 2-р гар **саарал** өнгөөр харагдана
- ☝️ **1 хуруу = VOLUME**, ✌️ **2 хуруу = BRIGHTNESS**, 🤟 **3 хуруу эсвэл
  чимхэлт = ARROW** — горим 1.2с барьж байж идэвхижинэ
- 🤏 **TAP** — чимхээд хурдан тайлахад дуу тагдана; **DRAG** — чимхсэн хэвээр
  чирэхэд дуу/гэрэл өөрчлөгдөнө
- ⏸️ `space` = түр зогсоох/үргэлжлүүлэх, `q` = гарах
- 🖥️ **Windows 10/11** (шууд), **WSL**, **Linux** (Arch/Debian/Fedora болон
  **Oracle VM VirtualBox** дээрх гост), **macOS**
- 📋 Аливаа **шинэ горимд орохын өмнө** доорх шаардлагын тайланг хэвлэж,
  дутуу зүйлийг суулгах командтай нь хамт харуулна

## 🖐️ Гарын дохилтууд

> **Хурууны нэршил:** `4` = эрхий, `8` = зангиа (индекс), `12` = дунд,
> `16` = чинээ, `20` = чигчий. Хурууг «дээш» гэвэл үзүүр нь үндсэн үе (PIP)-ээс
> дээш байхыг хэлнэ.

### 1️⃣ Горим солих (1.2 секунд барих)

| Хуруу (дээш) | Горим | Дараагийн үйлдэл |
|---|---|---|
| **1 хуруу** | **VOLUME** | TAP = mute, DRAG = дуу |
| **2 хуруу** | **BRIGHTNESS** | DRAG = гэрэл |
| **3 хуруу** | **ARROW** | индексийн үзүүр хөдөлгөх = сум |
| **эрхий+зангиа чимхэлт** (4+8) барих | **ARROW** | горимгүй/ARROW үед барихад |

- Хурууны **тоо** чухал: ямар ч 1/2/3 хуруу (зөвхөн чигчийгээ дээшлүүлэх гэх мэт)
  байж болно
- Чимхсэн байхад хурууны тоог тооцохгүй (чимхэлт = ARROW-ийн дохио)
- **Горим автоматаар гарахгүй** — өөр горимд орохын тулд шинэ дохиогаа дахин
  бариарай. 3 горим **харилцан орлуулна** (нэгэн зэрэг 2 горим ажиллахгүй)
- Атгасан гар / 0 хуруу = ямар ч горимд орохгүй (зориулалтын командгүй)

### 2️⃣ VOLUME MODE (1 хуруу)

| Дохиолол | Хийх хөдөлгөөн | Үр дүн |
|---|---|---|
| **TAP** | Эрхий+зангиа чимхээд **0.6с-аас хурдан**, чирэлтгүйгээр тайлах | Дуу тагдана / асана (mute toggle) |
| **DRAG** | Чимхсэн хэвээр гараа **дээш/доош** чирэх | Дуу нэмэгдэнэ / хасагдана |

- Чирсэн бол тайлахад **mute болохгүй** (зөвхөн DRAG)
- Дуу тагтай байхад чирвэл **таг цуцлагдана**
- **Горимгүй үед чимхэлт + чирэлт = юу ч өөрчлөхгүй**

### 3️⃣ BRIGHTNESS MODE (2 хуруу)

| Дохиолол | Хийх хөдөлгөөн | Үр дүн |
|---|---|---|
| **DRAG** | Чимхсэн хэвээр гараа **дээш/доош** чирэх | Дэлгэцийн гэрэл нэмэгдэнэ / хасагдана |

- Зөвхөн **зоосв нотбук** дээр ажиллана:
  - 🐧 Linux → **`brightnessctl`**
  - 🍎 macOS → **дотоод дэлгээрийн гэрэл** (суулгах шаардлагагүй, Apple-ийн
    `DisplayServices`/`CoreDisplay` API; зөвхөн MacBook/iMac-ийн **дотоод**
    дэлгээрийг дэмжинэ — гадаад monitor биш)
  - 🪟 Windows / виртуал машинд гэрлийн тохиргоо байхгүй тул уг горим идэвхгүй
    байна
- Гэрлийн доод хязгаар **1%**

### 4️⃣ ARROW KEY MODE (3 хуруу эсвэл чимхэлт)

| Дохиолол | Хийх хөдөлгөөн | Үр дүн |
|---|---|---|
| **Сум** | **Зангиа хурууны үзүүр** (8) анхдагч байрлалаасаа 0.08-аас холдоод, чигээ (↑↓←→) **0.35с** тогтмол барьвал | Нэг сумын товч дарна (cooldown 1.0с) |

- Чигээ өөрчлөхөд хугацаа дахин тоологдоно; буцаж байрлалдаа ирвэл зогсоно
- Дарсны дараа анхдагч байрлал **шинэчлэгдэнэ** (дараагийн хөдөлгөөн шинээрээс
  эхэлнэ)
- Товчийг **фокустай цонх руу** илгээнэ — сум ашиглахдаа зорилготой
  програмаа идэвхтэй болгоорой

### 5️⃣ Хяналт, хамгаалалт

| Дохиолол | Үр дүн |
|---|---|
| **`space`** | Түр зогсоох / үргэлжлүүлэх (`PAUSED` гэж заана) |
| **`q`** | Программ зогсоно |
| **Гар LOCK** | Анх илрүүлсэн гар (бугуй, цэг 0)-аар lock; дараагийн гаруудаас 0.15 зайд ойрхон нь сонгогдоно; гар **2.0с** алга болбол lock цуцлагдана |
| **Сонгогдоогүй гар** | Саарал өнгөөр зурагдана (үйлдэл хийхгүй) |

> ⚠️ `space`/`q` нь **OpenCV цонх фокустай байхад** л орно. ARROW ашиглахдаа
> бусад програм руу шилжсэн бол сум товч ажиллана, харин `space`/`q`-г
> буцааж цонхоо сонголгон дарна уу.

## 💻 Шаардлага

### Үндсэн (бүх платформ дээр ижил)

| Зүйл | Юунд хэрэгтэй | Шалгах / суулгах |
|---|---|---|
| **Python 3.10+** | гол хэл | `python3 --version` |
| **opencv-python, mediapipe** | камер + гар таних загвар | `pip install -r hand_control/requirements.txt` |
| **`models/hand_landmarker.task`** | гар таних загвар | Төсөлд **багтсан**, татаж авах шаардлагагүй |
| **Вебкамер (index 0)** | нүд | Linux: `ls /dev/video*`; Windows: Camera privacy шалгах |

### ОС-ийн нэмэлт хэрэгсэл (алийг нь суулгаагүй бол тухайн үйлдэл ажиллахгүй)

| Үйлдэл | 🐧 Linux | 🪟 Windows | 🍎 macOS |
|---|---|---|---|
| **Дуу (VOLUME)** | `pactl` — Arch: `sudo pacman -S libpulse` / Debian: `sudo apt install pulseaudio-utils` | `pycaw` + `comtypes` (pip-ээр сууна) | `osascript` (системд байрлай) |
| **Гэрэл (BRIGHTNESS)** | `brightnessctl` — `sudo pacman -S brightnessctl` / `sudo apt install brightnessctl` (**зоосв нотбук**) | ❌ ажиллахгүй | ✅ дотоод дэлгээрийн гэрэл (суулгах шаардлагагүй) |
| **Сум (ARROW)** | `xdotool` (X11) / `wtype` (Wayland) — **session-аас автоматаар сонгодог** | `pyautogui` (pip-ээр сууна) | `pyautogui` (pip-ээр сууна) |
| **Камер** | `/dev/video*` + `video` групп эрх | Camera privacy → Desktop apps | System Settings → Camera зөвшөөрөл |

- **WSL** нэмэлтээр: камерыг Windows-оос дамжуулах (`usbipd-win`), дуу/цонх = WSLg
- **Oracle VM VirtualBox** нэмэлтээр: **Extension Pack** (камер дамжуулалт),
  гост дээрх камерын эрх; виртуал машинд **гэрлийн бүрэлдэхүүн байдаггүй** тул
  BRIGHTNESS MODE ажиллахгүй (хэвийн үзэгдэл)

## 🚀 Ажиллуулах заавар

### 0. Код татаж авах (бүх платформ)

```bash
git clone https://github.com/Zaprilli/Gesture-controlled-Operating-System.git
cd Gesture-controlled-Operating-System
```

---

### 🪟 Windows

**Шаардлага:** Windows 10/11, Python 3.10+ ([python.org](https://www.python.org/downloads/) суулгахдаа *Add to PATH*),
вебкамер.

```powershell
# 1. Virtual environment үүсгэнэ
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Номын сангууд (pycaw, comtypes, pyautogui Windows дээр автоматаар сууна)
pip install -r hand_control\requirements.txt

# 3. Ажиллуулна
python hand_control\main.py
```

> ⚠️ PowerShell дээр `Activate.ps1` алдаа гарвал (execution policy):
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
> командийг эхлээд гүйцэтгэнэ үү.

> 📷 **Анх удаа** камер ашиглахыг Windows асуух болно —
> `Settings → Privacy & Security → Camera → Desktop apps`-ийг **zөвхөрүүлнэ үү**.

> ❌ **Гэрэл (BRIGHTNESS)** Windows дээр ажиллахгүй — энэ нь хэвийн (дэмжих
> платформ: Linux / macOS).

---

### 🪟 WSL (Windows Subsystem for Linux)

WSL нь анхдагчаа **камерыг хардаггүй** — камерыг Windows-оос WSL рүү
дамжуулах (passthrough) хэрэгтэй. **WSLg** (Windows 11) цонх + дууг дэмждэг.

**1. WSL суулгах** (PowerShell, админ бус болно):

```powershell
wsl --install -d Ubuntu
wsl --update
wsl --shutdown     # дараа WSL-ийг дахин нээнэ
```

**2. Камерыг WSL рүү дамжуулах** (`usbipd-win`):

```powershell
winget install --id dorssel.usbipd-win   # нэг удаа
usbipd list                               # камерын BUSID олно ("Integrated Webcam" гэх мэт)
usbipd bind --busid <BUSID>              # нэг удаа (админ шаардлагатай)
usbipd attach --wsl --busid <BUSID>      # WSL рүү холбоно
```

WSL дээр шалгах:

```bash
ls /dev/video*        # /dev/video0 гарч ирвэл боллоо
```

**3. Суулгаж ажиллуулах** (Ubuntu жишээ):

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip \
     pulseaudio-utils brightnessctl xdotool wtype

python3 -m venv .venv
source .venv/bin/activate
pip install -r hand_control/requirements.txt

python3 hand_control/main.py
```

> 🪟 **WSLg** (Windows 11) дээр OpenCV-ийн цонх автоматаар гарна. Windows 10
> дээр WSLg байхгүй — X-сэрвэр (VcXsrv / X410) суулгах шаардлагатай.
>
> 📷 Камер нэгэн зэрэг **нэг л** процесст хамаарна — Teams/Zoom ашиглаж
> байвал WSL-д нээгдэхгүй. Computer sleep-ээс буцаад ирвэл `usbipd attach`-ийг
> дахин гүйцэтгэнэ үү.
>
> 🔊 Дуу: `pactl info` → `Server String: ... pulse/native` гарвал WSLg аудио
> идэвхтэй. Windows 10 дээр байхгүй тул Windows руу шилжинэ үү.

---

### 🐧 Linux

```bash
# 1. Номын сангууд
python3 -m venv .venv
source .venv/bin/activate
pip install -r hand_control/requirements.txt

# 2. Дуу (VOLUME) — тухайн дистрибуциас:
```

| Дистрибуци | Команд |
|---|---|
| Arch / Manjaro / CachyOS | `sudo pacman -S libpulse` (PipeWire: `pipewire-pulse`) |
| Debian / Ubuntu | `sudo apt install pulseaudio-utils` |
| Fedora | `sudo dnf install pulseaudio-utils` |

```bash
# 3. Гэрэл + сум (зоосв нотбук; сум = X11 буюу Wayland-аас хамаарна)
sudo pacman -S brightnessctl xdotool wtype     # Arch
sudo apt install brightnessctl xdotool wtype   # Debian/Ubuntu

# 4. Камерын эрх (нэг удаа; дараа сессиондоо дахин нэвтрэх)
sudo usermod -aG video $USER

# 5. Ажиллуулна
python3 hand_control/main.py
```

> 💡 **KDE / GNOME (Wayland)** дээр ийм warning гарч болно —
> `Could not find the Qt platform plugin "wayland"`. Цонх **гарч л байвал
> асуудалгүй**. Урьдчилан дарахыг хүсвэл:
> ```bash
> QT_QPA_PLATFORM=xcb python3 hand_control/main.py
> ```

---

### 📦 Oracle VM VirtualBox дээр Linux

Нэмэлтээрээ: **Oracle VM VirtualBox** + **Extension Pack** (камер дамжуулалт
зөвхөн Extension Pack-аас хамаарна).

**1. VirtualBox + Extension Pack суулгах**

1. [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)-оос
   VirtualBox болон **VirtualBox Extension Pack** (All platforms) татаж авна
2. Extension Pack-ийг суулгах: VirtualBox → `File → Extensions → Install`
   (эсвэл `sudo VBoxManage extpack install VirtualBox_Extension_Pack*.vbox-extpack`)
3. Ubuntu / Arch / бусад Linux ISO татаж аваад **гост машин үүсгэнэ**
   (Memory ≥ 4GB, 2+ CPU зөвлөмж)

**2. Камерыг гост руу дамжуулах**

1. Гост **ажиллаж байх** үед менюгээс: **Devices → Webcam → Integrated Camera**
   (санаа зовохгүйгээр идэвхжүүлнэ — гост дээр `/dev/video0` гарна)
2. Эсвэл урьдчилан USB filter үүсгэх:
   `Settings → USB → Add New Filter → Integrated Camera`
3. Хэрэв **Webcam цэс байхгүй** бол: Extension Pack суугаагүй, эсвэл
   VirtualBox хувилбар Extension Pack-ийн хувилбартайгаа таарахгүй байна

**3. Гост дээр шалгах**

```bash
ls /dev/video*                                  # /dev/video0 гарвал боллоо
groups | grep video || sudo usermod -aG video $USER   # эрх (дараа нэвтрэлт)
pactl --version                                  # дуу (VM audio → PulseAudio/PipeWire)
brightnessctl -m 2>/dev/null || echo "no backlight (VM — BRIGHTNESS ажиллахгүй)"
```

**4. Суулгаж ажиллуулах** (гост дээр, дээрх Linux зааврын дагуу)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r hand_control/requirements.txt
python3 hand_control/main.py
```

> ⚠️ **Виртуал машинд гэрэл тохируулах бүрэлдэхүүн байдаггүй** (`/sys/class/backlight`
> байхгүй) — BRIGHTNESS MODE ажиллахгүй, программ эхлэлтээрээ мэдэгдэл хэвлэнэ.
> Бусад горим (VOLUME / ARROW) хэвээр ажиллана. Энэ нь алдаа биш юм.
>
> 💡 Зөвлөмж: гост дээр **X11 сесс** сонговол `xdotool` шууд ажиллана;
> Wayland бол `wtype` суулгана уу.

---

### 🍎 macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r hand_control/requirements.txt
python3 hand_control/main.py
```

- Анх удаа **камерын зөвшөөрөл** асуух болно —
  `System Settings → Privacy & Security → Camera` (терминалд) өгнө үү
- Дуу = `osascript`, сум = `pyautogui`, **гэрэл = дотоод дэлгээрийн гэрэл**
  (суулгах шаардлагагүй; зөвхөн MacBook/iMac-ийн дотоод дэлгээрийг дэмжинэ)

---

### ▶️ Эхлэлтийн тайлан

Программ **эхлэхэдээ** доорх шалгалтыг гүйцэтгэж, хэвлэнэ:

```text
==============================================================
  AJILLUULAHD SHAARDLAGATAI ZUIILSUUD (Requirements)
==============================================================
  [OK]    Python 3.10+              : 3.14.10
  [OK]    cv2                       : 5.0.0
  [OK]    mediapipe                 : 1.2.0
  [OK]    ZAGVAR (hand_landmarker)  : models/hand_landmarker.task
  [OK]    KAMERA (index 0)          : oldloo
  --- OS-iin nemelt herelse: alii uildel ajillana ---
  [OK]    pactl (DUU)               : /usr/bin/pactl
  [OK]    brightnessctl (GEREL)     : /usr/bin/brightnessctl
  [OK]    SUM (wayland)             : /usr/bin/wtype
==============================================================
  Bund buh UNDSEN shaardlaga hangagsan - ajillulj bolno!
==============================================================
Start: vol=45% mute=False bright=79%
1 horuu = VOLUME | 2 horuu = BRIGHTNESS | 3 horuu / erxii+zungia pinch = ARROW
TAP/DRAG = hemjee | zangiin ur (8) hudulg = sum | space=pause | q=quit
```

Тэмдэглэгээ:

| Тэмдэг | Утга |
|---|---|
| `[OK]` | Бэлэн байна |
| `[ALDAA]` | **Үндсэн** шаардлага дутуу (Python / номын сан / загвар / камер) → программ зогсоно, доор юу дутуугаа гаргана |
| `[TAANI]` | **Нэмэлт** хэрэгсэл дутуу → программ ажилласаар байна, зөвхөн тухайн үйлдэл (дуу/гэрэл/сум) идэвхгүй болно + суулгах команд |
| `[ -- ]` | Шалгах боломжгүй (жнь: cv2 суугаагүй) |

Дутуу зүйлтэй жишээ:

```text
  [TAANI]  pactl (DUU)               : suugaagui
          -> VOLUME MODE ajillahgui!
             Arch: sudo pacman -S libpulse
             Debian/Ubuntu: sudo apt install pulseaudio-utils
```

## ⚙️ Тохиргоо

`hand_control/main.py`-ийн эхэнд дараах хувьсагчдыг өөрчилж болно:

| Хувьсагч | Утга | Тайлбар |
|---|---|---|
| `ARM_HOLD_S` | `1.2` | Хурууг ийм секундээр тогтмол барихад горимд орно |
| `LOCK_MAX_DIST` | `0.15` | 2-р гарыг сонгохдоо анхны гарын байрлалаас энэ зайд ойр байх ёстой |
| `LOCK_TIMEOUT_S` | `2.0` | Гар алга болсон энэ хугацаанд lock хэвээрээ (дараа цуцлана) |
| `PINCH_DIST` | `0.06` | Чимхэлтийн босго (4+8-ийн зай) |
| `DRAG_MIN` | `0.035` | Эхлэлээс үүнээс бага хөдөлгөөн = чичрэл гэж тооцохгүй (**deadband**) |
| `DRAG_STEP` | `0.012` | Хэмжээ солигдох доод зөрөө (**hysteresis** — чичрэлээс flip хийхгүй) |
| `TAP_MAX_S` | `0.6` | TAP-ын дээш хугацаа: үүнээс хурдан тайлахад mute |
| `ARROW_DEAD` | `0.08` | Сум эхлэх босго: индексийн үзүүр үүнээс бага холдохгүй бол юу ч хийхгүй |
| `ARROW_HOLD_S` | `0.35` | Чигээ (↑↓←→) ийм секунд тогтвол нэг сум дарна |
| `ARROW_COOLDOWN_S` | `1.0` | Хоёр сумын товчийн хоорондох доод хугацаа |
| `WIN_W`, `WIN_H` | `640`, `480` | Камерын авалт болон цонхны хэмжээ |

## 📁 Төслийн бүтэц

```text
.
├── hand_control/                 # 👈 гол програм (god_mode)
│   ├── main.py                   #    гол цикл, жестийн логик, шаардлагын хяналт
│   ├── volume_control.py         #    дуу: pactl (Linux) / pycaw (Windows) / osascript (macOS)
│   ├── brightness_control.py     #    гэрэл: brightnessctl (Linux) / дотоод дэлгээрийн гэрэл (macOS)
│   ├── arrowkey.py               #    сум: session-аас xdotool (X11)/wtype (Wayland) / pyautogui
│   └── requirements.txt          #    шаардлагатай Python номын сангууд
├── models/
│   └── hand_landmarker.task      # MediaPipe гар таних загвар (git-д багтсан)
├── README.md                     # энэ файл
└── .gitignore
```

Ажиллуулах заавар **төслийн үндсэн хавтасаас** (`Gesture-controlled-Operating-System`):

```bash
python3 hand_control/main.py
```

## 🛠️ Ажилладаг зарчим

1. **Камер** → 640×480 кадр → толин тусгал (`flip`) → MediaPipe-ийг оруулна
2. **Hand Landmarker** загвар гарын 21 цэгийг баримтлана; бүрэн скелет
   дугаартайгаар зурагдана — **сонгосон гар** ногоон/усан, бусад **саарал**
3. **Гар LOCK** — анх илрүүлсэн гарын бугуйгаар lock; цэг 0-ийн байрлалаар
   ойрхныг сонгож, сонгогдоогүй гарыг үл тооцно
4. **Хуруу тоолох** → 1/2/3 хуруу (эсвэл чимхэлт) + `ARM_HOLD_S` барих → горим
   солигдоно; горимд орсон дохио нэг удаа хэвлэгдэнэ
5. **Чимхэлт (4+8)** → зөвхөн VOLUME / BRIGHTNESS горимд:
   - эхлэл → байрлал + цаг хадгална (энэ үед **юу ч өөрчлөхгүй**)
   - `DRAG_MIN`-ээс холдвол **DRAG** (хуримтлалгүй: `disp = эхлэл_y − одоогийн_y`)
   - тайлахад: `TAP_MAX_S`-аас хурдан + чирээгүй бол = **mute** (зөвхөн VOLUME)
6. **ARROW** → индексийн үзүүрийн хөдөлгөөнийг `ARROW_DEAD` → `ARROW_HOLD_S`
   → `ARROW_COOLDOWN_S` шүүлтээр дамжуулж товчлуур дарна
7. **Үр дүнгээ** тухайн платформын API-рүү шууд хүргэнэ:
   - Linux → `pactl` / `brightnessctl` / `xdotool`·`wtype` (session-аас өөрөө сонгоно)
   - Windows → `pycaw` / `pyautogui`
   - macOS → `osascript` / дотоод дэлгээрийн гэрэл (`DisplayServices`) / `pyautogui`

### Чичрэлээс хамгаалах (deadband + hysteresis)

- **Deadband** (`DRAG_MIN`) — эхлэлээс үүнээс бага холдоогүй бол *нягтхан* гэж
  үзэж тооцохгүй
- **Hysteresis** (`DRAG_STEP`) — сүүлд хэрэглэсэнээс үүнээс бага зөрөөгөөр
  байвал дахин тохируулахгүй → чичрэлээс дуу «ховхрох»гүй

## 🔧 Асуудал шийдвэрлэх

### Бүх платформ

#### `[ALDAA] KAMERA (index 0): oldohgui baina`

Камерыг бусад процесс эзэмшиж байна — **нэгэн зэрэг нэг л процесс** камер
ашиглана:

- **Linux:** `fuser -v /dev/video0` → гарсан процессыг `q`/`Ctrl+C`-ээр хаана уу
- **Windows:** Task Manager → ашиглаж буй Teams/Zoom/браузерын вебкамер хэсгийг хаана уу
- **WSL:** `usbipd list` → `State` нь `Attached` байх ёстой (дээрх WSL хэсэг)
- **VirtualBox:** `Devices → Webcam → Integrated Camera` идэвхтэй эсэх шалгах

#### `ModuleNotFoundError: No module named 'cv2'` (эсвэл mediapipe)

Virtual environment идэвхжээгүй байна:

```bash
source .venv/bin/activate        # Linux / macOS / WSL
.\.venv\Scripts\Activate.ps1     # Windows
pip install -r hand_control/requirements.txt
```

#### `ZAGVAR ... olddoggui: .../hand_landmarker.task`

Төсөл **бүрэн** татагдаагүй байна — `models/hand_landmarker.task` файл байх
ёстой (`ls models/`). Дахин татаж авна уу.

#### `space` / `q` ажиллахгүй байна

OpenCV цонх **фокустай** байх ёстой — цонхоо дараад дахин дарна уу.
(ARROW MODE-д бусад руу шилжсэн бол сум хэвээр ажиллана, `space`/`q` зөвхөн
цонхоо буцааж сонголгон дарахад орно.)

### 🐧 Linux

#### `pactl oldsongui` / дуу өөрчлөгдөхгүй байна

| Дистрибуци | Команд |
|---|---|
| Arch / Manjaro / CachyOS | `sudo pacman -S libpulse` (PipeWire: `sudo pacman -S pipewire-pulse`) |
| Debian / Ubuntu | `sudo apt install pulseaudio-utils` |
| Fedora | `sudo dnf install pulseaudio-utils` |

PipeWire дээр дуугүй бол: `systemctl --user restart pipewire-pulse`.
Зөв sink сонгогдсон эсэх: `pactl get-sink-volume @DEFAULT_SINK@`.

#### `brightnessctl oldsongui` / гэрэл өөрчлөгдөхгүй

```bash
brightnessctl -m        # утга гарвал болно (жишээ: intel_backlight,...,79%,...)
```

- Зөвхөн **зоосв нотбук** дээр ажиллана — **desktop** компьютерт backlight
  байхгүй бол BRIGHTNESS MODE идэвхгүй байна (мэдэгдэл хэвлэгдэнэ)
- Эрх дутуу бол: `sudo usermod -aG video $USER` (дараа сессиондоо дахин нэвтрэх)
- **Virtual Machine** дээр backlight байдаггүй → хэвийн үзэгдэл

#### Сум (ARROW) ажиллахгүй байна

Программ **ийм дарааллаар өөрөө сонгодог**: `XDG_SESSION_TYPE` (эсвэл
`WAYLAND_DISPLAY`/`DISPLAY`) → **Wayland бол `wtype`**, **X11 бол `xdotool`**
(аль нь нь суусан байна). Эхлэлтийн тайлан дээр ямар session илрүүлсэн, аль
хэрэгсэл сонгогдсоныг `SUM (wayland)` / `SUM (x11)` мөрөөр харна уу.

```bash
echo $XDG_SESSION_TYPE     # x11 | wayland
xdotool --version           # X11 дээр
wtype --version             # Wayland дээр
```

- Аль нь ч байхгүй бол: `sudo pacman -S xdotool wtype` /
  `sudo apt install xdotool wtype` (эсвэл **session-д таарах нэгийг** нь суулга)
- Session-тай **тохирохгүй** хэрэгсэл суусан бол (`wtype` байхад X11 гэх мэт)
  программ анхааруулга хэвлэнэ — тэгэхээр суулгахаа зөв сонгоно уу
- **Сум нь фокустай цонх руу явна** — зорилготой программыа идэвхтэй болгоно уу

#### `Could not find the Qt platform plugin "wayland"`

Зөвхөн **warning** — цонх гарч байвал асуудалгүй. Гарахгүй бол:

```bash
QT_QPA_PLATFORM=xcb python3 hand_control/main.py
```

### 🪟 WSL

#### WSL дээр `/dev/video*` байхгүй байна

1. `usbipd --version` суугаагүй бол: `winget install --id dorssel.usbipd-win`
2. `usbipd list` → State нь **Attached** эсэх шалгах
3. Дахин холбох: `wsl --update` → `wsl --shutdown` → `usbipd attach --wsl --busid <BUSID>`
4. Камер **Windows-аар** (Teams/Zoom) нээгдсэн байж магадгүй — тэдгээрийг хаана уу
5. Хэвээрээ байхгүй бол WSL-ийн **kernel шинэчлэх**: Windows-аас `wsl --update`

#### WSL дээр `pactl` ажиллахгүй байна

```bash
sudo apt install pulseaudio-utils
pactl info     # "Server String: ... pulse/native" гарвал WSLg аудио идэвхтэй
```

Windows 10 дээр WSLg байхгүй → Windows-д шууд суулгана уу, эсвэл Windows 11 рүү
шилжүүлнэ үү.

### 🪟 Windows

#### `pycaw` / `pyautogui` талаарх мэдэгдэл гарч байна

```powershell
pip install -r hand_control\requirements.txt
```

Программ эхлэлтээрээ аль модулийг суулгахаа хэвлэж өгнө — тухайн командыг
гүйцэтгээд дахин ажиллуулна уу.

#### Камер олдохгүй байна (зохих зөвшөөрөл)

`Settings → Privacy & Security → Camera → Let desktop apps access your camera`
→ **ON**.

### 🍎 macOS

- **Камерын зөвшөөрөл:** `System Settings → Privacy & Security → Camera`-аас
  терминал (Terminal / iTerm / VS Code) -д өгнө үү, дараа терминалыг дахин нээнэ
- **Дуу:** `osascript -e "set volume output volume 50"` ажиллаж байгаа эсэхийг
  шалгана уу (Automation зөвшөөрөл шаардаж магадгүй)
- **Гэрэл:** эхлэлтийн тайлан дээр `[OK] GEREL (dotood deleger)` гарвал бэлэн.
  `[TAANI]` гарвал macOS шинэчлэлт private API-г хаасан, эсвэл **гадаад
  monitor** (гадаад дэлгээрийг macOS энэ аргаар тохируулахгүй) байна — энэ
  тохиолдолд BRIGHTNESS MODE идэвхгүй, бусад горим хэвээр ажиллана

## 📜 Лиценз

Энэхүү төсөлд лиценз нэмээгүй байна. Ашиглахдаа зохиогчийн эрхийг хүндлэнэ үү.
