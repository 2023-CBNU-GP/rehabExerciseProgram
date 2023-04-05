import cv2
import PoseDetector as pd
import AngleManager as af

file_name="tmp04.mp4"
cap = cv2.VideoCapture(file_name)
pTime = 0
detector = pd.PoseDetector()

frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)
patientAngle= {"LelbowAngle":0,"LshoulderAngle":0,"RelbowAngle":0,"RshoulderAngle":0
            ,"Lhip":0,"Rhip":0,"Lknee":0,"Rknee":0}

AngleManager=af.AngleManager()

teacherAngle=AngleManager.GetAvgAngle("Shoulder_1.mp4")
while True:
    success, img = cap.read()

    Curframe=cap.get(cv2.CAP_PROP_POS_FRAMES)
    if  Curframe>= frameCount/3 and Curframe<=frameCount-frameCount/3: #현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
            img = detector.findPose(img)
            lmList = detector.findPosition(img)
            AngleManager.GetAverageAngle(lmList,patientAngle)

    if img is None:
        break

    cv2.waitKey(1)

for i,value in patientAngle.items():
    patientAngle[i]=round(value/(frameCount/3),2)

AngleManager.ComparePose(teacherAngle,patientAngle)

#위 다 일치하나, 선생님용은 아래 함수를 적어야함.
#AngleManager.TransferJsonFile(file_name,TeacherAngleAvg)

cap.release()
cv2.destroyAllWindows()

