import cv2
import numpy as np
import mediapipe as mp

# ================= MEDIAPIPE =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

# ================= SETTINGS =================
BOX_W, BOX_H = 80, 50
ANCHOR_POINT = None

font = cv2.FONT_HERSHEY_SIMPLEX

# ================= FUNCTION =================
def get_direction(nose, anchor, w, h):
    nx, ny = nose
    x, y = anchor

    if nx > x + w:
        return "RIGHT"
    elif nx < x - w:
        return "LEFT"
    elif ny > y + h:
        return "DOWN"
    elif ny < y - h:
        return "UP"
    else:
        return "CENTER"

# ================= MAIN LOOP =================
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

        nose = landmarks[1]

        if ANCHOR_POINT is None:
            ANCHOR_POINT = nose

        x, y = ANCHOR_POINT
        nx, ny = nose

        # Draw control box
        cv2.rectangle(frame, (x - BOX_W, y - BOX_H),
                      (x + BOX_W, y + BOX_H), (0, 255, 0), 2)

        cv2.line(frame, ANCHOR_POINT, nose, (255, 0, 0), 2)

        # Get direction
        direction = get_direction(nose, ANCHOR_POINT, BOX_W, BOX_H)

        cv2.putText(frame, direction, (50, 100),
                    font, 1, (0, 0, 255), 2)

        # Reset anchor with key press (optional)
        if cv2.waitKey(1) == ord('r'):
            ANCHOR_POINT = nose

    cv2.imshow("Direction Detection (MediaPipe)", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()