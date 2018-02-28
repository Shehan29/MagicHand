import pyautogui as control

import cv2

videoCapture = cv2.VideoCapture(0)
handCascade = cv2.CascadeClassifier('./hand.xml')
palmCascade = cv2.CascadeClassifier('./palm.xml')
fistCascade = cv2.CascadeClassifier('./fist.xml')

def track(cascade, colour) :
    objects = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), colour, 2)
        control.moveTo(x,y)
        return

while(True):
    ret, frame = videoCapture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    track(handCascade, ((0, 255, 0)))
    #track(palmCascade, ((255, 0, 0)))
    #track(fistCascade, ((0, 0, 255)))

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


