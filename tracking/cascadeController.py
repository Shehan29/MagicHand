from tracking.rotations import rotate_image, rotate_point, rotationValues
import pyautogui as control
import cv2

videoCapture = cv2.VideoCapture(0)
trackMovement = False

faceCascade = cv2.CascadeClassifier('haarcascades/face.xml')
handCascade = cv2.CascadeClassifier('haarcascades/hand.xml')

settings = {
    'scaleFactor': 1.1,
    'minNeighbors': 3,
    'minSize': (50, 50)
}

def track(frame, cascade, colour) :
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected = []

    for angle in rotationValues:
        rotatedImage = rotate_image(gray, angle)
        detected = cascade.detectMultiScale(rotatedImage, **settings)
        if len(detected):
            detected = [rotate_point(detected[-1], gray, -angle)]
            break

    for (x, y, w, h) in detected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), colour, thickness=2)

        pos = control.center((x,y,w,h))
        # currentPos = control.position()
        control.moveTo(pos)
        return

def main():
    while(videoCapture.isOpened()):
        ret, frame = videoCapture.read()
        frame = cv2.flip(frame, flipCode=1)

        track(frame, faceCascade, ((0, 255, 0)))

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    videoCapture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()