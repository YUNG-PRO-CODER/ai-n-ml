import cv2


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


cap = cv2.VideoCapture(0)
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]

      
        smiles = smile_cascade.detectMultiScale(face_roi, scaleFactor=1.7, minNeighbors=22)
        eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=10)

     
        if len(smiles) > 0:
            emotion = "Happy"
            color = (0, 255, 0)
        elif len(eyes) == 0:
            emotion = "Sad"
            color = (255, 0, 0)
        else:
            emotion = "Neutral"
            color = (0, 255, 255)

      
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, emotion, (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Emotion Detection (OpenCV Only)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
