import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    cv2.imshow('picture', frame)
    if cv2.waitKey(20) & 0XFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

""""
img_path = 'content/images/neymar/neymar.jpeg'
img = cv2.imread(img_path)
img = cv2.imread(img_path)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

boxes = detector.detectMultiScale(img)

for box in boxes:
    x1, y1, width, height = box
    x2, y2 = x1 + width, y1 + height
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow('fitiavana', img)
cv2.waitKey(0)
"""
