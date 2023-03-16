import cv2
import time
import PoseDetector as pd

cap = cv2.VideoCapture("OpenCV_video1.mp4")
pTime = 0
detector = pd.PoseDetector()
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)