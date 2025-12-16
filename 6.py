import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

filter_mode = "normal"
last_capture_time = 0

def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

def apply_filter(img, mode):
    if mode == "gray":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif mode == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
        return cv2.transform(img, kernel)
    elif mode == "negative":
        return cv2.bitwise_not(img)
    elif mode == "blur":
        return cv2.GaussianBlur(img, (21, 21), 0)
    return img

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        lm = hand.landmark

        thumb = lm[4]
        index = lm[8]
        middle = lm[12]
        ring = lm[16]
        pinky = lm[20]

        d_thumb_index = distance(thumb, index)
        d_thumb_middle = distance(thumb, middle)
        d_thumb_ring = distance(thumb, ring)
        d_thumb_pinky = distance(thumb, pinky)

        if d_thumb_index < 0.04 and time.time() - last_capture_time > 1:
            filename = f"photo_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print("📸 Photo Captured")
            last_capture_time = time.time()

        elif d_thumb_middle < 0.04:
            filter_mode = "gray"
        elif d_thumb_ring < 0.04:
            filter_mode = "sepia"
        elif d_thumb_pinky < 0.04:
            filter_mode = "negative"
        elif all(distance(thumb, f) > 0.1 for f in [index, middle, ring, pinky]):
            filter_mode = "blur"
        else:
            filter_mode = "normal"

    filtered = apply_filter(frame, filter_mode)

    if filter_mode == "gray":
        filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)

    cv2.putText(filtered, f"Filter: {filter_mode.upper()}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.imshow("Gesture Camera", filtered)

    if cv2.waitKey(1) & 0xFF == 'q':
        break

cap.release()
cv2.destroyAllWindows()
