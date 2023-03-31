import cv2
import PoseDetector as pd
import ImageOverlayer as io
import math
import time
import numpy as np

def GetJointAngle(CenterPos,jointPos1, jointPos2) :

    theta1=math.atan2((jointPos1[2]-CenterPos[2]), (jointPos1[1]-CenterPos[1]))
    theta2=math.atan2((jointPos2[2]-CenterPos[2]), (jointPos2[1]-CenterPos[1]))

    degree= abs(theta2-theta1)*180/math.pi

    return degree

def MatchTwoAngle(lmList): #두 영상으로 비교 예정...
    leftUpperBodyAngle={"LelbowAngle":[14,16,12],"LarmpitAngle":[12,14,24],"LbodyAngle":[12,11,24]}
    rightUpperBodyAngle={"RelbowAngle":[13,11,15],"RarmpitAngle":[11,13,23],"RbodyAngle":[11,12,23]}

    return False

cap = cv2.VideoCapture("Shoulder_1.mp4")
pTime = 0
detector = pd.PoseDetector()

frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)

while True:
    cTime = time.time()
    success, img = cap.read()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    if cap.get(cv2.CAP_PROP_POS_FRAMES) >= frameCount/3 : #현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
            img = detector.findPose(img)
            lmList = detector.findPosition(img)

            print(MatchTwoAngle(lmList))

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)


#real time
#
# webcam = cv2.VideoCapture(0)
# personFrame = cv2.imread("PersonFrame.png",cv2.IMREAD_UNCHANGED)
# h,w,_=personFrame.shape
#
# overlay=io.ImageOverlayer()
# if not webcam.isOpened() :
#     exit()
#
# while webcam.isOpened():
#     lmList=[]
#     detector = pd.PoseDetector()
#     status, frame = webcam.read()
#
#     if not status :
#         webcam.waitKey()
#         break
#
#     BackH,BackW,_=frame.shape
#     added_img=overlay.overlay_transparent(frame,personFrame,int(((BackW-1)/2)-((w-1)/2)),int(((BackH-1)/2)-((h-1)/2)))
#     img = detector.findPose(frame)
#     lmList = detector.findPosition(frame)
#
#     cv2.imshow("frame",added_img)
#
#     if cv2.waitKey(10) & 0xFF == ord('q') :
#         break
#
# webcam.release()
# cv2.destroyAllWindows()
