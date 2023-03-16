import mediapipe as mp
import cv2
import time

class PoseDetector() :

    def __init__(self, mode=False,complexity=1,
                 smooth=True, enableSeg=False,smoothSeg=True,detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.complexity=complexity
        self.enableSeg=enableSeg
        self.smoothSeg=smoothSeg

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity,self.smooth, self.enableSeg,
                                     self.smoothSeg,self.detectionCon, self.trackCon)

    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #print(results.pose_landmarks)
        if self.results.pose_landmarks :
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,
                                            self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self,img,draw=True):
        lmList=[]
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark) :
                h,w,c=img.shape
                cx,cy = int(landmark.x*w),int(landmark.y*h)
                lmList.append([id, cx, cy])

                if draw :
                    cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED) #그려지는 원형이 작아짐.

                #print(id,landmark) #landmark에 대한 x,y,z좌표가 출력된다. 이를 이용해서 각도를 구하면 될듯.

        return lmList