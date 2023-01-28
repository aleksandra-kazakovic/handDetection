####################################################
#
# The code in progress.
# The idea is to take the first frame from the video and determine the bin size.
#
####################################################
import cv2
import numpy as np
videoPath = "snimak13.mp4";

def clahe(img, clip_limit=2.0, grid_size=(8,8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    return clahe.apply(img)

def getBinDimension(src):
    # HSV thresholding to get rid of as much background as possible
    hsv = cv2.cvtColor(src.copy(), cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 0, 120])
    upper_blue = np.array([180, 38, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(src, src, mask=mask)
    b, g, r = cv2.split(result)
    g = clahe(g, 5, (3, 3))

    # Adaptive Thresholding to isolate the bin
    img_blur = cv2.blur(g, (9, 9))
    img_th = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 51, 2)

    contours, hierarchy = cv2.findContours(img_th, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the rectangle by choosing only the big ones
    # and choose the brightest rectangle as the bin
    max_brightness = 0
    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        x, y, w, h = rect
        if (w*h > 100000) and (w*h < 400000):
            print(w*h)
            mask = np.zeros(src.shape, np.uint8)
            mask[y:y+h, x:x+w] = src[y:y+h, x:x+w]
            brightness = np.sum(mask)
            if brightness > max_brightness:
                brightest_rectangle = rect
                max_brightness = brightness
            cv2.rectangle(mask, (x,y), (x+w, y+h), (255, 255, 0), 1)
            cv2.putText(mask, "Position", (550,50), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
            cv2.putText(mask, "binStartX: "+str(x), (550,100), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
            cv2.putText(mask, "binStartY: " + str(y), (550,150), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
            cv2.putText(mask, "binWidth: "+str(x+w), (550,200), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
            cv2.putText(mask, "binHeight: " + str(y+h), (550,250), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
            cv2.putText(mask, "press tab to continue", (220,410), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
            cv2.imshow("mask", mask)
            cv2.waitKey(0)
    return brightest_rectangle

cap = cv2.VideoCapture(videoPath)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(680))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(420))

success, src = cap.read()
if not success:
    exit(1)
src = cv2.resize(src, (854, 480))
x, y, w, h = getBinDimension(src)
print(x,y,w,h)
cv2.rectangle(src, (x,y), (x+w, y+h), (255, 255, 0), 1)
cv2.putText(src, "Position", (550,50), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
cv2.putText(src, "binStartX: "+str(x), (550,100), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
cv2.putText(src, "binStartY: " + str(y), (550,150), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
cv2.putText(src, "binWidth: "+str(x+w), (550,200), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
cv2.putText(src, "binHeight: " + str(y+h), (550,250), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
cv2.putText(src, "press tab to exit", (220,410), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1) 
cv2.imshow("canvas", src)
cv2.waitKey(0)