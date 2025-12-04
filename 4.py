import cv2, time, pyautogui
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands = 1, min_detection_confidence = 0.7)
mpDrawing = mp.solutions.drawing_utils

scrollSpeed = 600
scrollDelay = 1
camWidth, camHeight = 900, 850

def detect_gesture(landmarks, handedness):
    fingers = []
    tips = [mpHands.HandLandmarks.INDEX_FINGER_TIP, mpHands.HandLandmarks.MIDDLE_FINGER_TIP, mpHands.HandLandmarks.RING_FINGER, mpHands.HandLandmarks.PINKY_FINGER]
    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            fingers.append(1)
    tip_thumb = landmarks.landmark[mpHands.HandLandmark.THUMB_TIP]
    tip_ip = landmarks.landmark[mpHands.HandLandmark.THUMB_IP]
    if(handedness == "Right" and tip_thumb.x > tip_ip) or (handedness == "Left" and tip_ip > tip_thumb):
        fingers.append(1)
        return "scroll up" if sum(fingers) == 5 else "scroll down" if len(fingers) == 0 else "none" 
    
cap = cv2.VideoCapture(0)
cap.set(3, camWidth)
cap.set(4, camHeight)
lastScroll = p_time = 0

print("Gesture control \n open palm: scroll up \n close palm: scroll down")

while cap.isOpened():
    sucess, img = cap.read()

    if not sucess:
        print("Error try again")
        break

    img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1)
    results = hands.process(img)
    gesture, handedness = "none", "Unknown"

    if results.multi_hand_landmarks:
        for hand, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness_landmarks):
            handedness = handedness_info.classification[0].label
            gesture = detect_gesture(hand, handedness)
            mpDrawing.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)

            if(time.time() - lastScroll) > scrollDelay :
                if gesture == "scroll up": pyautogui.scroll(scrollSpeed)
                elif gesture == "scroll down": pyautogui.scroll(-scrollSpeed)
                lastScroll = time.time()

    fps = 1/(time.time()-p_time) if (time.time()-p_time) > 0 else 0
    p_time = time.time()
    cv2.putText(img, f"FPS: {int(fps)} | hand : {handedness} | Gesture : {gesture}", (10,30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    cv2.imshow("Gesture Control", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.relese()
cap.destoryAllWindows()
