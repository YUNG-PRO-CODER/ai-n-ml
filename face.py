import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("Couldn't open the webcam")
    exit()

while True:
    ret, frame = capture.read()


    if not ret:
        print("Failed to capture the image")
        break

    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray_scale, scaleFactor = 1.1, minNeighbors=5, minSize = (35,35))

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame, f'people count {len(faces)}', (10,30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("capturing image ",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()