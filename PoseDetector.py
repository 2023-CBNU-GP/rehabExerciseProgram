import cv2
import mediapipe as mp
class PoseDetector() :

    def __init__(self, mode=False,upper=False,
                 smooth=True,detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.smooth = smooth
        self.upper=upper
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upper,
                                     self.smooth,self.detectionCon, self.trackCon)

    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        return img

    #좌표를 그리는 함수인데, 하나만 가져가면 된다. 아래 하나는 임시 시험용 ... 색을 다르게하기 위함
    def drawPose(self,img,list,color,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        for id,landmark in enumerate(list) :
            cx,cy = landmark[0],landmark[1] #해당 지점에 대한 x,y좌표를 찾아냄.
            print(landmark)
            cv2.circle(img,(int(cx),int(cy)),5,(0,0,color),thickness=-1) #그려지는 원형이 작아짐.

        return img

    def findPosition(self,img,draw=True):
        lmList=[]
        PoseList=[]
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark) :

                h,w,c=img.shape
                cx,cy = int(landmark.x*w),int(landmark.y*h) #해당 지점에 대한 x,y좌표를 찾아냄.
                lmList.append([id, cx, cy])
                PoseList.append([cx,cy])

        return lmList,PoseList
