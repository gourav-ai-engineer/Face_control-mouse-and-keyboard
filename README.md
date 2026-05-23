# 👁️ AI Virtual Mouse & Keyboard using Eye Tracking

A real-time **AI-powered Human Computer Interaction (HCI)** system that enables users to control their computer using **eye blinks, head movement, nose tracking, and voice commands**.

Built using **Python, OpenCV, MediaPipe, PyAutoGUI, and Speech Recognition**, this project provides a complete hands-free interaction experience with:

- 🖱️ Virtual Mouse  
- ⌨️ Virtual Keyboard  
- 👁️ Eye Blink Detection  
- 🧭 Head Direction Detection  
- 🎤 Voice Commands  

---

# 📌 Features

## 🖱️ AI Virtual Mouse

- Cursor movement using head/nose tracking
- Left click using left eye blink
- Right click using right eye blink
- Scroll mode using both eyes
- Dynamic cursor acceleration
- Automatic calibration system

---

## ⌨️ AI Virtual Keyboard

- On-screen keyboard controlled using head movement
- Blink to select keys
- Audio feedback while selecting
- Space and backspace support
- Menu-based keyboard selection

---

## 👁️ Eye Blink Detection

- Real-time blink detection
- Uses Eye Aspect Ratio (EAR)
- MediaPipe facial landmarks

---

## 🧭 Direction Detection

Detects:
- Left
- Right
- Up
- Down
- Center

---

## 🎤 Voice Controlled Mouse

Supports voice commands like:
- Move up
- Move down
- Move left
- Move right
- Left click
- Right click

---

# 🧠 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Programming |
| OpenCV | Computer Vision |
| MediaPipe | Face Mesh Tracking |
| NumPy | Numerical Operations |
| PyAutoGUI | Mouse & Keyboard Automation |
| SciPy | EAR/MAR Calculations |
| SpeechRecognition | Voice Commands |
| Pyglet | Audio Feedback |

---

# 📂 Project Structure

```bash
AI-Virtual-Mouse-Keyboard/
│
├── main.py
├── mouse.py
├── keyboard.py
├── direction.py
├── eye blinking detection.py
├── eye detection.py
├── voice.py
├── utils.py
│
├── sound.wav
├── left.wav
├── right.wav
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Virtual-Mouse-Keyboard.git

cd AI-Virtual-Mouse-Keyboard
```

---

## 2️⃣ Create Virtual Environment (Optional)

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install opencv-python mediapipe numpy pyautogui scipy SpeechRecognition pyglet pyaudio
```

---

# ▶️ Running the Project

## Start Main Controller

```bash
python main.py
```

The system will activate your webcam and show the control menu.

---

# 🎮 Controls

## 🖱️ Mouse Controls

| Gesture | Action |
|---|---|
| Move Head | Move Cursor |
| Left Eye Blink | Left Click |
| Right Eye Blink | Right Click |
| Both Eyes Closed | Scroll Mode |
| Open Mouth | Recalibrate Cursor |

---

## ⌨️ Keyboard Controls

| Gesture | Action |
|---|---|
| Look Left | Select Left Keyboard |
| Look Right | Select Right Keyboard |
| Blink | Select Key |
| Long Blink | Return to Main Menu |

---

# 🧠 How It Works

The project uses **MediaPipe Face Mesh** to track facial landmarks in real-time.

### Important tracked landmarks:
- Eyes
- Nose
- Mouth

### The system calculates:
- **Eye Aspect Ratio (EAR)** → Blink Detection
- **Mouth Aspect Ratio (MAR)** → Recalibration
- **Head Movement Direction** → Cursor/Keyboard Navigation

These gestures are mapped to:
- Mouse movement
- Clicking
- Scrolling
- Keyboard typing
- Voice interactions

---

# 📄 Core Modules

## `main.py`
Main controller for switching between mouse and keyboard modes.

## `mouse.py`
Implements:
- Cursor control
- Eye blink clicking
- Scroll mode
- Cursor acceleration

## `keyboard.py`
Implements:
- Virtual keyboard
- Blink-based key selection
- Audio feedback

## `direction.py`
Head movement and direction tracking system.

## `eye blinking detection.py`
Real-time blink detection using EAR calculations.

## `eye detection.py`
Visualizes eye landmarks using MediaPipe Face Mesh.

## `voice.py`
Voice command based mouse control system.

## `utils.py`
Contains utility functions:
- Eye Aspect Ratio
- Mouth Aspect Ratio
- Direction Detection

---

# 🔥 Future Improvements

- Deep Learning based gaze tracking
- Customizable gestures
- Multi-language keyboard
- Accessibility enhancements
- Mobile integration
- Real-time AI calibration
- Gesture-based shortcuts

---

# 🎯 Applications

- Accessibility Systems
- Assistive Technology
- AI Human Computer Interaction
- Smart Automation
- Hands-Free Computing
- Research Projects
- Gaming Interfaces

---

# 📸 Screenshots

> Add your screenshots here

```bash
screenshots/
```

---

# 🤝 Contributing

Contributions are welcome.

## Steps:
1. Fork the repository
2. Create a new branch
3. Make improvements
4. Commit changes
5. Create Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Gourav Kumar

AI & Computer Vision Enthusiast 🚀

---

# ⭐ Support

If you like this project:

- ⭐ Star the repository
- 🍴 Fork the project
- 📢 Share with others
