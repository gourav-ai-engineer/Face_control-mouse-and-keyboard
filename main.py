import cv2
import mediapipe as mp
import numpy as np
import subprocess
import time
from utils import eye_aspect_ratio

# ================= SETTINGS =================
BLINK_THRESHOLD = 0.20
LONG_BLINK_TIME = 2.5   # seconds (use 2.5 instead of 5 for usability)
BOX_W = 80

# ================= MEDIAPIPE =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

# ================= LANDMARKS =================
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
NOSE_TIP = 1

# ================= VARIABLES =================
mode = "menu"   # menu / mouse / keyboard
process = None

blink_start = None

ANCHOR_POINT = None

font = cv2.FONT_HERSHEY_SIMPLEX


# ================= PROCESS CONTROL =================
def start_process(script):
    return subprocess.Popen(["python", script])

def stop_process(proc):
    if proc:
        proc.terminate()


# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        face_landmarks = result.multi_face_landmarks[0]

        h, w, _ = frame.shape
        landmarks = np.array([(int(lm.x*w), int(lm.y*h)) for lm in face_landmarks.landmark])

        leftEye = landmarks[LEFT_EYE]
        rightEye = landmarks[RIGHT_EYE]
        nose = landmarks[NOSE_TIP]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        if ANCHOR_POINT is None:
            ANCHOR_POINT = nose

        dx = nose[0] - ANCHOR_POINT[0]

        # ================= MENU =================
        if mode == "menu":

            cv2.putText(frame, "LOOK LEFT = MOUSE", (50,200), font, 0.8, (0,255,0), 2)
            cv2.putText(frame, "LOOK RIGHT = KEYBOARD", (50,250), font, 0.8, (0,255,0), 2)

            if dx < -BOX_W:
                mode = "mouse"
                process = start_process("mouse.py")
                ANCHOR_POINT = nose
                time.sleep(1)

            elif dx > BOX_W:
                mode = "keyboard"
                process = start_process("keyboard.py")
                ANCHOR_POINT = nose
                time.sleep(1)

        # ================= INSIDE MODE =================
        else:
            cv2.putText(frame, f"MODE: {mode.upper()}", (50,50),
                        font, 1, (0,0,255), 2)

            # BOTH EYES CLOSED → long blink detection
            if leftEAR < BLINK_THRESHOLD and rightEAR < BLINK_THRESHOLD:

                if blink_start is None:
                    blink_start = time.time()

                elif time.time() - blink_start > LONG_BLINK_TIME:
                    stop_process(process)
                    process = None
                    mode = "menu"
                    ANCHOR_POINT = nose
                    blink_start = None
                    time.sleep(1)

            else:
                blink_start = None

    cv2.imshow("MAIN CONTROL", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()