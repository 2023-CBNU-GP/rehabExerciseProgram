import cv2
import PoseDetector as pd
import AngleManager as af


class Doctorlib():

    poselist=[]
    DoctorAngleAvg= {"LelbowAngle":0,"LshoulderAngle":0,"RelbowAngle":0,"RshoulderAngle":0
            ,"Lhip":0,"Rhip":0,"Lknee":0,"Rknee":0} #doctor angle 정보 저장
    filename="" #backend에서 넘어올 파일 이름으로 바꿀것

    def __init__(self,name):
        self.poselist()
        self.filename=name
        self.poselist=self.listinit()

    def listinit(self):
        cap = cv2.VideoCapture(self.filename)

        detector = pd.PoseDetector()
        frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)
        AngleManager=af.AngleManager()
        DoctorAngle= {"LelbowAngle":0,"LshoulderAngle":0,"RelbowAngle":0,"RshoulderAngle":0
            ,"Lhip":0,"Rhip":0,"Lknee":0,"Rknee":0} #doctor angle 정보 저장

        while True:
            success, img = cap.read()

            Curframe=cap.get(cv2.CAP_PROP_POS_FRAMES)

            if  Curframe>= frameCount/3 and Curframe<=frameCount-frameCount/3: #현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
                img = detector.findPose(img)
                lmList = detector.findPosition(img)
                AngleManager.GetAngle(lmList,DoctorAngle)
                #평균을 구하기 위해 모든 프레임을 덧셈 함수
                AngleManager.GetAverageJoint(lmList,self.poselist)
                AngleManager.GetAverageAngle(lmList,self.DoctorAngleAvg)
                if img is None:
                    break
        #의사의 경우 프레임당 평균을 구해야함.
        for i,value in self.DoctorAngleAvg.items():
            self.DoctorAngleAvg[i]=round(value/(frameCount/3),2)

        AngleManager.TransferJsonFile(self.filename,self.DoctorAngleAvg)

        cv2.waitKey(1)





#위 다 일치하나, 선생님용은 아래 함수를 적어야함.
#AngleManager.TransferJsonFile(file_name,TeacherAngleAvg)
