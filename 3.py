import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol, _ = volume.GetVolumeRange()

while True:
    ret, img = cap.read()
    if not ret:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLm, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            x1, y1 = int(handLm.landmark[4].x * w), int(handLm.landmark[4].y * h)
            x2, y2 = int(handLm.landmark[8].x * w), int(handLm.landmark[8].y * h)

            length = hypot(x2 - x1, y2 - y1)

            vol = np.interp(length, [20, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            vol_percent = int(np.interp(vol, [minVol, maxVol], [0, 100]))

            bright = int(np.interp(length, [20, 200], [10, 100]))
            sbc.set_brightness(bright)

            cv2.putText(img, f"Volume: {vol_percent}%", (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.putText(img, f"Brightness: {bright}%", (10, 80),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
