import cv2
import numpy as np
import mediapipe as mp
import time
import pyglet
from utils import eye_aspect_ratio

# ================= SOUNDS =================
sound = pyglet.media.load("sound.wav", streaming=False)
left_sound = pyglet.media.load("left.wav", streaming=False)
right_sound = pyglet.media.load("right.wav", streaming=False)

# ================= MEDIAPIPE =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

# ================= SETTINGS =================
BLINK_THRESHOLD = 0.20
BLINK_TIME = 0.3
BOX_W = 80

MOVE_DELAY = 0.5
last_move_time = 0

# ================= LANDMARKS =================
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
NOSE_TIP = 1

# ================= KEYBOARD =================
keys_set_1 = {i: k for i, k in enumerate(
    ["Q","W","E","R","T","A","S","D","F","G","Z","X","C","V","<"]
)}
keys_set_2 = {i: k for i, k in enumerate(
    ["Y","U","I","O","P","H","J","K","L","_","B","N","M",".","<"]
)}

keyboard = np.zeros((600, 1000, 3), np.uint8)
board = np.ones((300, 1400), np.uint8) * 255

font = cv2.FONT_HERSHEY_SIMPLEX

# ================= VARIABLES =================
frames = 0
letter_index = 0
blink_start = None
blink_triggered = False

LETTER_DELAY = 20
HOLD_TIME = 0.5
BLINK_TIME = 0.3
 # seconds before blink allowed
key_hover_start = time.time()
last_letter_index = -1
text = ""
keyboard_selected = "left"
select_menu = True
ANCHOR_POINT = None

# ================= DRAW =================
def draw_letters(i, text_key, light):
    x = (i % 5) * 200
    y = (i // 5) * 200

    color = (255,255,255) if light else (50,50,50)
    text_color = (0,0,0) if light else (255,255,255)

    cv2.rectangle(keyboard, (x,y), (x+200,y+200), color, -1)
    cv2.putText(keyboard, text_key, (x+60,y+120), font, 2, text_color, 3)

def draw_menu():
    keyboard[:] = (30,30,30)
    cv2.putText(keyboard, "LEFT", (100,300), font, 2, (255,255,255), 3)
    cv2.putText(keyboard, "RIGHT", (600,300), font, 2, (255,255,255), 3)
    cv2.putText(frame, f"Hold: {current_time - key_hover_start:.2f}",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
# ================= MAIN =================
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    keyboard[:] = (26,26,26)

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

        if ANCHOR_POINT is None:
            ANCHOR_POINT = nose

        dx = nose[0] - ANCHOR_POINT[0]
        current_time = time.time()

        # ================= MENU =================
        if select_menu:
            draw_menu()

            if current_time - last_move_time > MOVE_DELAY:

                if dx > BOX_W:
                    keyboard_selected = "right"
                    right_sound.play()
                    select_menu = False
                    last_move_time = current_time
                    ANCHOR_POINT = nose

                elif dx < -BOX_W:
                    keyboard_selected = "left"
                    left_sound.play()
                    select_menu = False
                    last_move_time = current_time
                    ANCHOR_POINT = nose

        # ================= KEYBOARD =================
        else:
            keys = keys_set_1 if keyboard_selected == "left" else keys_set_2

            frames += 1
            LETTER_DELAY = 20  # increase this

            if frames >= LETTER_DELAY:
                letter_index = (letter_index + 1) % 15
                frames = 0

            # Reset hover timer ONLY when letter changes
            if letter_index != last_letter_index:
                key_hover_start = time.time()
                last_letter_index = letter_index  # reset hover timer

            for i in range(15):
                draw_letters(i, keys[i], i == letter_index)

            # ================= BLINK =================
            # ================= BLINK =================
            current_time = time.time()

            # Allow blink only after staying on key
            if current_time - key_hover_start > HOLD_TIME:

                if leftEAR < BLINK_THRESHOLD:

                    if blink_start is None:
                        blink_start = current_time

                    elif current_time - blink_start > BLINK_TIME:

                        if not blink_triggered:
                            key = keys[letter_index]

                            if key == "<":
                                text = text[:-1]
                            elif key == "_":
                                text += " "
                            else:
                                text += key

                            sound.play()

                            blink_triggered = True
                            select_menu = True
                            ANCHOR_POINT = nose

                else:
                    blink_start = None
                    blink_triggered = False

        cv2.putText(board, text, (50,150), font, 2, 0, 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("Keyboard", keyboard)
    cv2.imshow("Board", board)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()