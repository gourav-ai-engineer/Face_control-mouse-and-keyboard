import numpy as np
from scipy.spatial import distance


# 👁️ Eye Aspect Ratio (works for MediaPipe 6 points)
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C) if C != 0 else 0
    return ear


# 👄 Mouth Aspect Ratio (MediaPipe version - 4 points)
def mouth_aspect_ratio(mouth):
    # mouth = [top, bottom, left, right]

    top = mouth[0]
    bottom = mouth[1]
    left = mouth[2]
    right = mouth[3]

    # vertical distance
    A = distance.euclidean(top, bottom)

    # horizontal distance
    B = distance.euclidean(left, right)

    mar = A / B if B != 0 else 0
    return mar


# 🧭 Direction detection (same as before)
def direction(nose_point, anchor_point, w, h, multiple=1):
    nx, ny = nose_point
    x, y = anchor_point

    if nx > x + multiple * w:
        return 'right'
    elif nx < x - multiple * w:
        return 'left'

    if ny > y + multiple * h:
        return 'down'
    elif ny < y - multiple * h:
        return 'up'

    return 'none'