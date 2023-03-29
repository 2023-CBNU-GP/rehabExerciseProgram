import cv2
import PoseDetector as pd
import ImageOverlayer as io
import math
import time

def FindDistance(jointPos1, jointPos2) :

    _,x1,y1=jointPos1
    _,x2,y2=jointPos2
    x=x2-x1
    y=y2-y1
    distance=math.sqrt((x*x)+(y*y))

    return distance

def TransOneDegree(b,c,a):

    b2=math.pow(b,2)
    c2=math.pow(c,2)
    a2=math.pow(a,2)

    resultDeg=math.degrees(math.acos((b2+c2-a2)/(2*b*c)))

    if resultDeg>180 :
        return -1  #error넘버 지정하기, 사람의 몸은 180도 이상 측정 불가
    return resultDeg

def TransDegree(b,c,a):

    return 0

cap = cv2.VideoCapture("Shoulder_1.mp4")
pTime = 0
detector = pd.PoseDetector()

frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(frameCount)
while True:
    cTime = time.time()
    success, img = cap.read()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    if cap.get(cv2.CAP_PROP_POS_FRAMES) >= frameCount/3 : #현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
            img = detector.findPose(img)
            lmList = detector.findPosition(img)


            distance1=int(FindDistance(lmList[11],lmList[13])) #b
            distance2=int(FindDistance(lmList[13], lmList[15]))  #c
            distance3=int(FindDistance(lmList[11], lmList[15])) #a

            #print(str(distance1)+" "+str(distance2)+" "+str(distance3))
            print(TransOneDegree(distance1,distance2,distance3))

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
