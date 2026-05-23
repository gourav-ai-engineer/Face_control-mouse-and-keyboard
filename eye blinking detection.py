import cv2
import numpy as np
import mediapipe as mp
from utils import eye_aspect_ratio

# ================= MEDIAPIPE =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

# ================= SETTINGS =================
BLINK_THRESHOLD = 0.20

# ================= LANDMARK INDEX =================
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

font = cv2.FONT_HERSHEY_SIMPLEX

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

        # ================= EYES =================
        leftEye = landmarks[LEFT_EYE]
        rightEye = landmarks[RIGHT_EYE]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        # ================= DRAW =================
        for (x, y) in leftEye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        for (x, y) in rightEye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # ================= BLINK DETECTION =================
        if ear < BLINK_THRESHOLD:
            cv2.putText(frame, "BLINKING", (50, 100),
                        font, 1, (0, 0, 255), 2)

        # Show EAR value (debug)
        cv2.putText(frame, f"EAR: {ear:.2f}", (50, 150),
                    font, 0.7, (255, 0, 0), 2)

    cv2.imshow("Blink Detection (MediaPipe)", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()