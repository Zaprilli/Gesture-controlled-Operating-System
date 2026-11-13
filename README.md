# 🖐️ Gesture-controlled-Operating-System

Камер дээрх гарын хөдөлгөөнөөр компьютерийн дууны хэмжээг удирдах төсөл.
Машин сургалт (MediaPipe) ашиглан гарын 21 цэгийг баримтлан, доошлүүлэх/дээшлүүлэх,
таг мэт хийснээр унтрааж-аших боломжтой юм.

## ✨ Онцлогууд

- 📷 Вебкамерээр гарыг илрүүлэн, бүрэн скелетийг дэлгэц дээр зурж харуулна
- 🤏 **PINCH + чирэлт** — хуруу болон эрхий хүрээ хавчсан хэвээрээ дээш/доош хөдөлгөхөд дууны хэмжээ өөрчлөгдөнө
- 👆 **TAP** — хурууны хавчлагаа хурдан тайлахад дуу унтраах/асах (mute toggle)
- 📊 Дэлгэц дээр дууны хэмжээний самбар, одоогийн төлөвийг шууд харуулна
- ⚙️ Тохиргоонууд код доторх тодорхой хувьсагчдаар хялбархан өөрчлөгдөнө
- 💻 **Linux, Windows, macOS** бүх платформ дээр ажиллана

## 🖐️ Гарын дохилтууд

| Дохиолол | Хийх хөдөлгөөн | Үр дүн |
|---|---|---|
| **TAP** | Эрхий (4) болон зангиа (8) хүрээгээ хавчаад, **0.6 секундын дотор** хөдөлгөөнгүйгээр тайлах | Дуу унтраах / асаах |
| **DRAG** | Хавчлагаа хадгалсан хэвээрээ гараа **дээш/доош** хөдөлгөх | Дууны хэмжээ нэмэгдэх/хасах |

> Хавчсан ч чирэхгүй (хэт богино хугацаанд тайлавал) = TAP,
> хавчсан ч дээш/доош хөдөлгөвөл = DRAG гэж тооцогдоно.

## 💻 Шаардлага

- ОС: **Linux** (PulseAudio/`pactl` эсвэл PipeWire), **Windows 10/11**, **macOS**
- Python 3.10+
- Вебкамер (default camera, index 0)
- Python-ийн номын сангууд: `opencv-python`, `mediapipe`
  - Windows дээр нэмэлтээр `pycaw`, `comtypes` (`requirements.txt`-д автоматаар сууна)

## 🚀 Ажиллуулах заавар

### Linux (Ubuntu/Debian)

```bash
# 1. Кодоо татаж авна
git clone https://github.com/Zaprilli/Gesture-controlled-Operating-System.git
cd Gesture-controlled-Operating-System

# 2. Virtual environment үүсгэнэ (зөвлөмж)
python3 -m venv .venv
source .venv/bin/activate

# 3. Шаардлагатай номын сангуудыг суулгана
pip install -r requirements.txt

# 4. (Хэрэв pactl байхгүй бол) PulseAudio-ийн хэрэгслүүдийг суулгана
sudo apt install pulseaudio-utils

# 5. Хэрэгжүүлнэ
python volume_control.py
```

### Windows (PowerShell)

```powershell
# 1. Кодоо татаж авна
git clone https://github.com/Zaprilli/Gesture-controlled-Operating-System.git
cd Gesture-controlled-Operating-System

# 2. Virtual environment үүсгэнэ (зөвлөмж)
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Шаардлагатай номын сангуудыг суулгана
pip install -r requirements.txt

# 4. Хэрэгжүүлнэ
python volume_control.py
```

> ⚠️ PowerShell дээр `Activate.ps1` алдаа гарвал (execution policy):
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
> командийг эхлээд гүйцэтгэнэ үү.

### macOS

```bash
# 1. Кодоо татаж авна
git clone https://github.com/Zaprilli/Gesture-controlled-Operating-System.git
cd Gesture-controlled-Operating-System

# 2. Virtual environment үүсгэнэ (зөвлөмж)
python3 -m venv .venv
source .venv/bin/activate

# 3. Шаардлагатай номын сангуудыг суулгана
pip install -r requirements.txt

# 4. Хэрэгжүүлнэ
python volume_control.py
```

> 🍎 macOS дээр анх удаа ажиллуулахад **камерын зөвшөөрөл** асуух тул
> `System Settings → Privacy & Security → Camera`-аас зөвшөөрнө үү.
> Дууны хэмжээ `osascript`-аар удирдагдана.

Дэлгэцэнд камерын зураг гарч ирэх бөгөөд гарын скелет, дууны хэмжээний самбар
дээр нь харагдана. Гаргахын тулд терминалд `q` дарна уу.

## ⚙️ Тохиргоо

`volume_control.py` эхэнд дараах хувьсагчдыг өөрчилж болно:

| Хувьсагч | Утга | Тайлбар |
|---|---|---|
| `PINCH_DIST` | `0.06` | Эрхий болон зангиа хүрээ хэдий дээр ойрчихвол хавчлага гэж үзэх вэ |
| `DRAG_MIN` | `0.035` | Үүнээс бага хөдөлгөөн = чичрэл гэж тооцохгүй (deadband) |
| `DRAG_STEP` | `0.012` | Дууны хэмжээ солигдох алхмын хэмжээ (чичрэлээс flip хийхгүйн тулд) |
| `TAP_MAX_S` | `0.6` | TAP гэж үзэх хамгийн их хугацаа ( секунд ) |

## 📁 Төслийн бүтэц

```
.
├── volume_control.py            # Гол программын код (Linux/Windows/macOS)
├── requirements.txt             # Шаардлагатай Python номын сангууд
├── models/
│   └── hand_landmarker.task     # MediaPipe гар илрүүлэх загвар
├── README.md                    # Энэ файл
└── .gitignore
```

## 🛠️ Ажилладаг зарчим

1. `OpenCV` вебкамераас кадрыг авна
2. `MediaPipe Hand Landmarker` загвар гарын 21 цэгийг баримтлана
3. Эрхий хүрээ (4) + зангиа хүрээ (8)-ийн зайг тооцно
   - Зай нь бага байвал **хавчлага (pinch)** эхэлсэн гэж үзнэ
   - Хавчлага доторх гараа дээш/доош хөдөлгөсөн бол = **DRAG**
   - Хавчлага хурдан тайлагдаж, хөдөлгөөнгүй байсан бол = **TAP**
4. Үр дүнгээ тухайн платформын дууны API-рүү шууд хүргэнэ:
   - **Linux** → `pactl` (PulseAudio/ PipeWire)
   - **Windows** → `pycaw` (Windows Audio Core API)
   - **macOS** → `osascript` (Core Audio)

## 📜 Лиценз

Энэхүү төсөлд лиценз нэмээгүй байна. Ашиглахдаа зохиогчийн эрхийг хүндлэнэ үү.
