import cv2
import mediapipe as mp
import math 

fingersIds = [8, 12, 16, 20]
thumbId = 4
distance = 4

class HandDetector():
    def __init__(self, static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.model_complexity, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNumber=0):
        lmList = [] #all lendmark possitions
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id, lm in enumerate(myHand.landmark):
                height, width, _ = img.shape
                centerX, centerY = int(lm.x*width), int(lm.y*height)
                lmList.append([id,centerX, centerY])
        return lmList

    def takingType1(self, lmHand1):
        if len(lmHand1) != 0:
            for id in fingersIds:
                if(lmHand1[id][2] > lmHand1[id-3][2]):
                    return True
        return False     

    def takingType2(self, lmHand1):
        if len(lmHand1) != 0:
            return (lmHand1[thumbId][1] > lmHand1[fingersIds[len(fingersIds)-1]][1] and lmHand1[thumbId][1] < lmHand1[fingersIds[1]][1]) or (lmHand1[thumbId][1] < lmHand1[fingersIds[len(fingersIds)-1]][1] and lmHand1[thumbId][1] > lmHand1[fingersIds[1]][1])

    def  distanceBetweenTwoFingers(self, finger1, finger2):
        return math.sqrt(pow(finger1[1]-finger2[1],2) + pow(finger1[2]-finger2[2],2))

    def takingType3(self, lmHand1):
        if len(lmHand1) != 0:
            for id in fingersIds:
                if self.distanceBetweenTwoFingers(lmHand1[id], lmHand1[thumbId]) < distance:
                    return True

    def takingSomething(self, lmHand1):
        return self.takingType1(lmHand1) or self.takingType2(lmHand1) or self.takingType3(lmHand1)
