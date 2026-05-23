import cv2
import numpy as np
import mediapipe as mp
import pyautogui as pyag
import time
from utils import eye_aspect_ratio
from utils import mouth_aspect_ratio
# ================== SETTINGS ==================
BLINK_THRESHOLD = 0.20
BLINK_TIME = 0.25

SMOOTHING = 5
SCROLL_SENSITIVITY = 30

SCREEN_W, SCREEN_H = pyag.size()

# ================== MEDIAPIPE ==================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# ================== LANDMARK INDEX ==================
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
NOSE_TIP = 1
MOUTH = [13, 14, 78, 308]
# ================== VARIABLES ==================
prev_x, prev_y = 0, 0

left_blink_start = None
right_blink_start = None
left_triggered = False
right_triggered = False

scroll_mode = False
scroll_anchor = None

ANCHOR_POINT = None
BOX_W, BOX_H = 80, 50
MOVE_SPEED = 20

# ================= CALIBRATION =================
calibrated = False
calibration_start = time.time()
CALIBRATION_TIME = 2  # seconds

# ================= BOX =================
ANCHOR_POINT = None
BOX_W, BOX_H = 80, 50

# ================= ACCELERATION =================
BASE_SPEED = 10
MAX_SPEED = 40

# ================= DRAG =================
dragging = False
drag_start_time = None
DRAG_THRESHOLD = 0.8  # seconds
# ================== CAMERA ==================
cap = cv2.VideoCapture(0)

# ================== MAIN LOOP ==================
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        face_landmarks = result.multi_face_landmarks[0]

        h, w, _ = frame.shape

        # Convert landmarks
        landmarks = np.array([
            (int(lm.x * w), int(lm.y * h))
            for lm in face_landmarks.landmark
        ])

        # ================== EYES ==================
        leftEye = landmarks[LEFT_EYE]
        rightEye = landmarks[RIGHT_EYE]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        mouth = landmarks[MOUTH]
        mar = mouth_aspect_ratio(mouth)
        # ================== BLINK DETECTION ==================

        # ================= DRAG =================
        # ================== SCROLL MODE (PRIORITY) ==================

        BOTH_EYES_CLOSED = leftEAR < BLINK_THRESHOLD and rightEAR < BLINK_THRESHOLD

        if BOTH_EYES_CLOSED:
            if scroll_anchor is None:
                scroll_anchor = nose
                scroll_mode = True

            cv2.putText(frame, "SCROLL MODE", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            dy = nose[1] - scroll_anchor[1]

            if abs(dy) > 10:
                pyag.scroll(-int(dy * 2))

        else:
            scroll_mode = False
            scroll_anchor = None

            # ================== LEFT CLICK ==================
            if leftEAR < BLINK_THRESHOLD and rightEAR > BLINK_THRESHOLD:
                if left_blink_start is None:
                    left_blink_start = time.time()
                elif time.time() - left_blink_start > BLINK_TIME:
                    if not left_triggered:
                        pyag.click(button='left')
                        left_triggered = True
            else:
                left_blink_start = None
                left_triggered = False

            # ================== RIGHT CLICK ==================
            if rightEAR < BLINK_THRESHOLD and leftEAR > BLINK_THRESHOLD:
                if right_blink_start is None:
                    right_blink_start = time.time()
                elif time.time() - right_blink_start > BLINK_TIME:
                    if not right_triggered:
                        pyag.click(button='right')
                        right_triggered = True
            else:
                right_blink_start = None
                right_triggered = False

        # ================== NOSE (CURSOR CONTROL) ==================
        # ================== BOX CONTROL ==================

        nose = landmarks[NOSE_TIP]
        # ================= CALIBRATION =================
        if not calibrated:
            cv2.putText(frame, "CALIBRATING... LOOK CENTER", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            if time.time() - calibration_start > CALIBRATION_TIME:
                ANCHOR_POINT = nose
                calibrated = True

            cv2.imshow("AI Mouse", frame)
            continue

        if ANCHOR_POINT is None:
            ANCHOR_POINT = nose

        x, y = ANCHOR_POINT
        nx, ny = nose

        dx = nx - x
        dy = ny - y

        # Draw box
        cv2.rectangle(frame, (x - BOX_W, y - BOX_H),
                      (x + BOX_W, y + BOX_H), (0, 255, 0), 2)

        cv2.line(frame, ANCHOR_POINT, nose, (255, 0, 0), 2)

        # Reset anchor with mouth open (optional)
        if mar > 0.6:
            ANCHOR_POINT = nose
        # ================= ACCELERATION =================
        distance_x = abs(dx)
        distance_y = abs(dy)

        speed_x = min(BASE_SPEED + distance_x // 5, MAX_SPEED)
        speed_y = min(BASE_SPEED + distance_y // 5, MAX_SPEED)

        # ================= MOVEMENT =================
        if dx > BOX_W:
            pyag.moveRel(speed_x, 0)
        elif dx < -BOX_W:
            pyag.moveRel(-speed_x, 0)

        if dy > BOX_H:
            pyag.moveRel(0, speed_y)
        elif dy < -BOX_H:
            pyag.moveRel(0, -speed_y)

        # ================== SCROLL MODE ==================

        # Activate scroll mode if both eyes closed (intentional gesture)
        if leftEAR < BLINK_THRESHOLD and rightEAR < BLINK_THRESHOLD:
            if not scroll_mode:
                scroll_mode = True
                scroll_anchor = nose
        else:
            scroll_mode = False

        if scroll_mode:
            cv2.putText(frame, "SCROLL MODE", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            dy = nose[1] - scroll_anchor[1]

            if abs(dy) > 15:
                pyag.scroll(-int(dy * SCROLL_SENSITIVITY / 100))

        # ================== DRAW ==================
        for (x1, y1) in leftEye:
            cv2.circle(frame, (x1, y1), 2, (0, 255, 0), -1)

        for (x1, y1) in rightEye:
            cv2.circle(frame, (x1, y1), 2, (0, 255, 0), -1)

        cv2.circle(frame, tuple(nose), 4, (255, 0, 0), -1)

    cv2.imshow("AI Mouse", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()