import cv2
import numpy as np
import mediapipe as mp

# ================= MEDIAPIPE =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

# ================= LANDMARK INDEX =================
# Left eye points (MediaPipe)
LEFT_EYE_H = [33, 133]      # horizontal
LEFT_EYE_V = [159, 145]     # vertical

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

        # ================= LEFT EYE =================
        left_point = landmarks[LEFT_EYE_H[0]]
        right_point = landmarks[LEFT_EYE_H[1]]

        top_point = landmarks[LEFT_EYE_V[0]]
        bottom_point = landmarks[LEFT_EYE_V[1]]

        # Draw horizontal line
        cv2.line(frame, tuple(left_point), tuple(right_point), (0, 255, 0), 2)

        # Draw vertical line
        cv2.line(frame, tuple(top_point), tuple(bottom_point), (0, 255, 0), 2)

        # Optional: draw points
        cv2.circle(frame, tuple(left_point), 3, (0, 0, 255), -1)
        cv2.circle(frame, tuple(right_point), 3, (0, 0, 255), -1)
        cv2.circle(frame, tuple(top_point), 3, (255, 0, 0), -1)
        cv2.circle(frame, tuple(bottom_point), 3, (255, 0, 0), -1)

    cv2.imshow("Eye Detection (MediaPipe)", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()