AI Virtual Mouse & Keyboard using Eye Tracking 👁️🖱️⌨️

An advanced computer vision-based Human-Computer Interaction system that allows users to control the mouse, keyboard, and navigation using eye blinks, head movement, nose tracking, and voice commands.
Built using Python, OpenCV, MediaPipe, PyAutoGUI, and Speech Recognition.

🚀 Features
🖱️ AI Virtual Mouse
Control mouse cursor using head/nose movement
Left click using left eye blink
Right click using right eye blink
Scroll mode using both eyes closed
Dynamic cursor acceleration
Mouth gesture for recalibration
⌨️ AI Virtual Keyboard
On-screen keyboard controlled using head movement
Blink to select letters
Audio feedback for key selection
Supports:
Alphabets
Space
Backspace
👁️ Eye Blink Detection
Real-time blink detection using Eye Aspect Ratio (EAR)
MediaPipe facial landmark tracking
🧭 Head Direction Detection
Detects:
Left
Right
Up
Down
Center
🎤 Voice Control
Voice commands for:
Mouse movement
Left click
Right click
🎯 Main Control System
Central controller to switch between:
Mouse mode
Keyboard mode
Long blink to return to main menu
📂 Project Structure
├── main.py
├── mouse.py
├── keyboard.py
├── direction.py
├── eye blinking detection.py
├── eye detection.py
├── voice.py
├── utils.py
├── sound.wav
├── left.wav
├── right.wav
🛠️ Technologies Used
Python
OpenCV
MediaPipe
NumPy
PyAutoGUI
SciPy
SpeechRecognition
Pyglet
⚙️ Installation
1️⃣ Clone Repository
git clone <your-repository-link>
cd <project-folder>
2️⃣ Install Dependencies
pip install opencv-python mediapipe numpy pyautogui scipy SpeechRecognition pyglet pyaudio
▶️ Running the Project
Start Main Controller
python main.py

The system will open the webcam and display:

Look Left → Open Mouse Control
Look Right → Open Keyboard Control
🎮 Controls
🖱️ Mouse Controls
Action	Gesture
Move Cursor	Move Head/Nose
Left Click	Left Eye Blink
Right Click	Right Eye Blink
Scroll	Close Both Eyes
Recalibrate	Open Mouth
⌨️ Keyboard Controls
Action	Gesture
Select Left Keyboard	Look Left
Select Right Keyboard	Look Right
Select Letter	Blink
Return to Menu	Automatic after selection
🧠 How It Works

The project uses MediaPipe Face Mesh to detect facial landmarks in real time.
Important landmarks:

Eyes
Nose
Mouth

These landmarks are processed to calculate:

Eye Aspect Ratio (EAR)
Mouth Aspect Ratio (MAR)
Head movement direction

The system maps these gestures to:

Mouse movement
Clicking
Keyboard input
Scrolling
Voice actions
📌 Core Files
main.py

Main controller for switching modes between mouse and keyboard.

mouse.py

Implements AI virtual mouse using head tracking and eye blinks.

keyboard.py

Implements blink-based virtual keyboard.

direction.py

Head direction detection system.

eye blinking detection.py

Eye blink detection using EAR calculation.

eye detection.py

Eye landmark visualization using MediaPipe.

voice.py

Voice-controlled mouse operations.

utils.py

Utility functions for EAR, MAR, and direction calculations.

🔥 Future Improvements
AI-powered gesture recognition
Deep learning-based eye tracking
Multi-language virtual keyboard
Accessibility mode for disabled users
Wireless mobile integration
Real-time calibration optimization
📷 Applications
Accessibility systems
Hands-free computer interaction
Assistive technology
Smart interaction systems
AI-based HCI research
Gaming & automation
🤝 Contribution

Contributions are welcome.

fork → clone → improve → pull request
📄 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Developed by Gourav Kumar 🚀
