import cv2
import PoseDetector as pd
import AngleManager as af


file_name="test1.mp4"
cap = cv2.VideoCapture(file_name)
pTime = 0
detector = pd.PoseDetector()

frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)
patientAngle= {"LelbowAngle":0,"LshoulderAngle":0,"RelbowAngle":0,"RshoulderAngle":0
            ,"Lhip":0,"Rhip":0,"Lknee":0,"Rknee":0}
scoreAngle= {"LelbowAngle":0,"LshoulderAngle":0,"RelbowAngle":0,"RshoulderAngle":0
            ,"Lhip":0,"Rhip":0,"Lknee":0,"Rknee":0}
AngleManager=af.AngleManager()

teacherAngle=AngleManager.GetAvgAngle("test.mp4")


poselist={11:[0,0],12:[0,0],13:[0,0],14:[0,0],15:[0,0],16:[0,0],23:[0,0],24:[0,0],25:[0,0],26:[0,0],27:[0,0],28:[0,0]}

frame=0;
similarity=0.0
while True:
    success, img = cap.read()

    Curframe=cap.get(cv2.CAP_PROP_POS_FRAMES)

    if  Curframe>= frameCount/3 and Curframe<=frameCount-frameCount/3: #현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
          frame+=1
          img = detector.findPose(img)
          lmList = detector.findPosition(img)

          #사이각 구하기 공식
          AngleManager.GetAngle(lmList,patientAngle)
          AngleManager.GetAverageAngle(lmList,patientAngle)
          AngleManager.ComparePose(teacherAngle,patientAngle,scoreAngle)
          #cos유사도
          AngleManager.GetAverageJoint(lmList,poselist)
          similarity=AngleManager.GetSimiarityCos(teacherAngle,poselist)

                #의사용, 환자의 경우 실시간으로 비교가 일어나야하므로 필요없음.


          cv2.imshow('img',img)

    if img is None:
        break


print(similarity)
print(scoreAngle)

# for i,value in patientAngle.items():
#      patientAngle[i]=round(value/frameCount,2)
#print(patientAngle)
# # for id,value in poselist.items():
# #     x=value[0]
# #     y=value[1]
# #
# #     poselist[id]=[round(x/(frameCount/3),2),round(y/(frameCount/3),2)]
# #
# # print(poselist)
## round해서 나누지말고 그대로 저장해야함..
# # AngleManager.TransferJsonFile(file_name,poselist,patientAngle)
# cv2.waitKey(1)
#
#
#
#
#
#
#
# #위 다 일치하나, 선생님용은 아래 함수를 적어야함.
# #AngleManager.TransferJsonFile(file_name,TeacherAngleAvg)
#
# cap.release()
# cv2.destroyAllWindows()
#
