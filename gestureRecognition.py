import cv2
import numpy as np
from pynput.mouse import Button, Controller
from AppKit import NSScreen

# Colour Boundaries (for bright green)
lowerBound = np.array([30, 80, 40])
upperBound = np.array([40, 255, 255])

# Colours
blue = (255, 0, 0)
red = (0, 0, 255)
# Camera Settings
camx, camy = (320, 240)
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))


def main():
    # mouse object
    mouse = Controller()
    # screen size
    screenWidth, screenHeight = (NSScreen.mainScreen().frame().size.width, NSScreen.mainScreen().frame().size.height)
    # open camera
    cam = cv2.VideoCapture(0)
    # gesture
    pinching = False

    while cam.isOpened():
        ret, img = cam.read()
        img = cv2.resize(img,(340,220))
        img = cv2.flip(img, flipCode=1)

        # convert BGR to HSV
        imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        # create the Mask
        mask = cv2.inRange(imgHSV,lowerBound,upperBound)
        # masks
        maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
        # use masks to find finger(s)
        maskFinal = maskClose
        matches = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[1]

        if len(matches) == 2:
            if pinching:
                pinching = False
                mouse.release(Button.left)
            # blue rectangles on each finger
            x1,y1,w1,h1=cv2.boundingRect(matches[0])
            x2,y2,w2,h2=cv2.boundingRect(matches[1])
            cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),blue,2)
            cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),blue,2)
            # center of rectangles
            cx1, cy1 = coordinates(x1, y1, w1, h1)
            cx2, cy2 = coordinates(x2, y2, w2, h2)
            # midpoint between 2 fingers
            cx, cy = midpoint(cx1, cy1, cx2, cy2)
            # line connecting 2 fingers
            cv2.line(img, (cx1,cy1), (cx2,cy2), blue, 2)
            # circle at midpoint
            cv2.circle(img, (cx,cy), 2, red, 2)
            # move mouse based on circle coordinate
            moveMouse(cx, cy, screenWidth, screenHeight, camx, camy, mouse)

        elif(len(matches)==1):
            x,y,w,h=cv2.boundingRect(matches[0])
            if not pinching:
                pinching = True
                mouse.press(Button.left)
            # blue rectangle on finger
            cv2.rectangle(img,(x,y),(x+w,y+h),blue,2)
            # center of rectangle
            cx, cy = coordinates(x,y,w,h)
            # circle around center
            cv2.circle(img,(cx,cy),int((w+h)/4),red,2)
            # move mouse based on circle coordinate
            moveMouse(cx, cy, screenWidth, screenHeight, camx, camy, mouse)

        # display camera preview
        cv2.imshow("Gesture Recognition Preview", img)
        # stop program when q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def coordinates(x,y,w,h):
    return int(x+w/2), int(y+h/2)

def midpoint(x1,y1,x2,y2):
    return int((x1+x2)/2), int((y1+y2)/2)

def moveMouse(x, y, screenWidth, screenHeight, camx, camy, mouse):
    mouseLoc = (x * screenWidth / camx, y * screenHeight / camy)
    mouse.position = mouseLoc
    while mouse.position != mouseLoc:
        mouse.position = mouseLoc
        pass

if __name__ == '__main__':
    main()