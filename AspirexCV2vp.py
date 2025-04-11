import cv2
import numpy as np
import os
from AspirexCV2module import handDetector

# Load overlay images
overlayList = []
folderPath = r"C:\Program Files\Python312\Myprograms\GitRepo\AspirexCVWS\Header"
for imPath in os.listdir(folderPath):
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
header = overlayList[0]

# Initialize variables
brushThickness = 25
eraserThickness = 100
drawColor = (255, 0, 255)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# webcam
cap = cv2.VideoCapture(0)  
cap.set(3, 1280)  # width
cap.set(4, 720)   # height

detector = handDetector()

while True:
    #importing image
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break
    img = cv2.flip(img, 1)

    #handmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]

        #detecting fingers
        fingers = detector.fingersUp()

        # If Selection Mode - Two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            if y1 < 125:
                if 250 < x1 < 450:  # Purple brush
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:  # Blue brush
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:  # Green brush
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:  # Eraser
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # If Drawing Mode - Index finger is up
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Eraser
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    # Merge img and imgCanvas
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image
    img[0:125, 0:1280] = header

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
