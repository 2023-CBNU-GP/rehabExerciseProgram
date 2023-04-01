import cv2
import PoseDetector as pd
import ImageOverlayer as io
import math

def GetJointAngle(CenterPos,jointPos1, jointPos2) :

    theta1=math.atan2((jointPos1[2]-CenterPos[2]), (jointPos1[1]-CenterPos[1]))
    theta2=math.atan2((jointPos2[2]-CenterPos[2]), (jointPos2[1]-CenterPos[1]))

    degree= abs(theta2-theta1)*180/math.pi

    return round(degree,3)

def MatchTwoAngle(joints1,leftSum): #두 영상으로 비교 예정...
    leftUpperBodyAngle={"LelbowAngle":[14,16,12],"LarmpitAngle":[12,14,24],"LbodyAngle":[12,11,24]}
    rightUpperBodyAngle={"RelbowAngle":[13,11,15],"RarmpitAngle":[11,13,23],"RbodyAngle":[11,12,23]}

    i=0
    for center,left,right in leftUpperBodyAngle.values():
        leftSum[i]+=GetJointAngle(joints1[center],joints1[left],joints1[right])
        if i==0:
            print(str(GetJointAngle(joints1[center],joints1[left],joints1[right])))
        i+=1

    return leftSum


def ComparePose(TeacherAngle,PatientAngle) :

    compareAngle=abs(TeacherAngle-PatientAngle)

    if compareAngle <= 5 :
        return 100
    elif compareAngle <= 10 :
        return 90
    elif compareAngle <= 20 :
        return 80
    elif compareAngle <= 30 :
        return 70
    # 60이하부터는 아예 fail 처리 예정
    return 60

cap = cv2.VideoCapture("Shoulder_1.mp4")
pTime = 0
detector = pd.PoseDetector()

frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)
TeacherAngleSum=[0,0,0]
while True:
    success, img = cap.read()

    Curframe=cap.get(cv2.CAP_PROP_POS_FRAMES)
    if  Curframe>= frameCount/3 and Curframe<=frameCount-frameCount/3: #현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
            img = detector.findPose(img)
            lmList = detector.findPosition(img)
            MatchTwoAngle(lmList,TeacherAngleSum)

    if img is None:
        break

    cv2.imshow("image", img)
    cv2.waitKey(1)

for i in range(0,len(TeacherAngleSum)):
    TeacherAngleSum[i]/=(frameCount/3)

print(TeacherAngleSum)


cap.release()
cv2.destroyAllWindows()
