import cv2
import sys
import os
import mediapipe as mp
import numpy as np
from Detection.binModel import Bin, Compartment, Dot
from Detection.handDetector import HandDetector
import Configurations.helper as helper
import math
import statistics
from Subscribers.DatabaseSubscriber.compartmentPickModel import CompartmentPickModel

intensityMax = 20
class Vector():
    def __init__(self, X, Y, intensity):
        self.X = X
        self.Y = Y
        self.intensity = intensity

def isInGoodCompartment(img, lmHand1, compartment):
    return lmHand1[8][1] > compartment.upperLeft.x and lmHand1[8][1] < compartment.downRight.x and lmHand1[8][2] > compartment.upperLeft.y and lmHand1[8][2] < compartment.downRight.y

def hasDirectionChanged(img, lmHand1, prev_hand_coords, numberOfFrames, next_pos):
    if numberOfFrames > 2:
        if prev_hand_coords is not None and next_pos is not None:
            if (prev_hand_coords[1] <= lmHand1[9][2] and prev_hand_coords[1] >= next_pos[1]):
                cv2.putText(img, "Direction has changed", (440,150), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1)   
                return True

def handTrackingProcess(videoPath, portId, event):
    binConfig = helper.read_bin_config()
    binWidth = int(binConfig['BinConfig']['binWidth'])
    binHeight = int(binConfig['BinConfig']['binHeight'])
    typeOfBin = int(binConfig['BinConfig']['typeOfBin'])
    binStartX = int(binConfig['BinConfig']['binStartX'])
    binStartY = int(binConfig['BinConfig']['binStartY'])
    bin = Bin(typeOfBin)

    cap = cv2.VideoCapture(videoPath)
    videoConfig = helper.read_video_config()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(videoConfig['VideoConfig']['videoWidth']))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(videoConfig['VideoConfig']['videoHeight']))
    cap.set(cv2.CAP_PROP_FPS, int(videoConfig['VideoConfig']['videoFPS']))
    detector = HandDetector()

    vectorList = []
    intensityDifferences = []
    kalman = cv2.KalmanFilter(4, 2)
    kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
    kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
    kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03
    next_pos = None
    numberOfFrames = 0
    prev_hand_coords = None
    currentframe = 0;

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (int(videoConfig['VideoConfig']['videoWidth']), int(videoConfig['VideoConfig']['videoHeight'])))
        img = detector.findHands(img, True)
        lmHand1 = detector.findPosition(img, 0)
        cv2.rectangle(img, (binStartX, binStartY), (binStartX+binWidth,binStartY+binHeight), color=(255, 100, 0),thickness=2)
        if len(lmHand1) != 0:
            if len(vectorList) == 0:
                intensity=0
                vectorList.append(Vector(lmHand1[9][1], lmHand1[9][2], intensity))
            else:
                intensity =  int(math.sqrt(pow(lmHand1[9][1] - vectorList[-1].X, 2) + pow(lmHand1[9][2] - vectorList[-1].Y, 2)))
                intensityDifferences.append(abs(vectorList[-1].intensity - intensity))
                vectorList.append(Vector(lmHand1[9][1], lmHand1[9][2], intensity))
                cv2.putText(img, "Hand speed: "+str(intensity), (440,50), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1)    

            if detector.takingSomething(lmHand1):
                cv2.putText(img, "Hand in take position", (440,100), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 1)
            if detector.takingSomething(lmHand1) and hasDirectionChanged(img, lmHand1, prev_hand_coords, numberOfFrames, next_pos) and intensity <= intensityMax:
                numberOfCompartment =  bin.getCompartmentNumberUsingTheCoordinates(lmHand1[8][1], lmHand1[8][2])
                print("Taking something from ", numberOfCompartment)
                cv2.putText(img, f"Taking from {numberOfCompartment}.", (500,250), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255, 255), 2)
                data = CompartmentPickModel(0, portId, typeOfBin, numberOfCompartment)
                event.dispatch("Taking from compartment", data)

            #KalmanFilter
            if numberOfFrames == 0:
                kalman.statePost = np.array([[np.float32(lmHand1[9][1])],[np.float32(lmHand1[9][2])], [0], [0]], np.float32)
                kalman.predict()
            else:
                mp = np.array([[np.float32(lmHand1[9][1])],[np.float32(lmHand1[9][2])]])
                kalman.correct(mp)
                next_pos = kalman.predict()
                # Print the predicted position
                cv2.circle(img, (int(next_pos[0]), int(next_pos[1])), 4, (0, 255, 0), 2)
                prev_hand_coords = [lmHand1[9][1], lmHand1[9][2]]
            numberOfFrames = numberOfFrames + 1
        else:
            vectorList.clear()
            numberOfFrames = 0
            intensityDifferences.clear()

        #save each frame as an image 
        # filename = "images"
        # if not os.path.isdir(filename):
        #     os.mkdir(filename) 
        # imagePath = os.path.join(filename, f"frame{currentframe}.jpg")
        # currentframe = currentframe + 1
        # cv2.imwrite(imagePath, img) 

        cv2.imshow("Image", img)
        cv2.waitKey(1) 




