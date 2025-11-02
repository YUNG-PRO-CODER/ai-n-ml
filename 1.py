import cv2
import numpy as np


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("Couldn't open the webcam")
    exit()

def adjust_brightness(image, value=40):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    final_hsv = cv2.merge((h, s, v))
    bright_img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return bright_img

def rotate_image(image, angle=0):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def crop_to_face(image, faces):
    if len(faces) == 0:
        return image 
    (x, y, w, h) = faces[0]
    margin = 30  
    x1 = max(x - margin, 0)
    y1 = max(y - margin, 0)
    x2 = min(x + w + margin, image.shape[1])
    y2 = min(y + h + margin, image.shape[0])
    cropped = image[y1:y2, x1:x2]
    return cropped

while True:
    ret, frame = capture.read()
    if not ret:
        print("Failed to capture the image")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(35, 35))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.putText(frame, f'People count: {len(faces)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Live Feed (Press 'e' to edit image, 'q' to quit)", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('e'): 
        print("Enhancing image...")

       
        rotated = rotate_image(frame, angle=0)

        
        bright = adjust_brightness(rotated, value=40)

        
        gray2 = cv2.cvtColor(bright, cv2.COLOR_BGR2GRAY)
        faces2 = face_cascade.detectMultiScale(gray2, scaleFactor=1.1, minNeighbors=5, minSize=(35, 35))
        cropped = crop_to_face(bright, faces2)

      
        cv2.imshow("Edited Image", cropped)
        cv2.imwrite("enhanced_image.jpg", cropped)
        print("✅ Image saved as 'enhanced_image.jpg'")

    elif key == ord('q'):  
        break

capture.release()
cv2.destroyAllWindows()
