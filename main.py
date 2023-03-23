import cv2
import PoseDetector as pd
import ImageOverlayer as io

webcam = cv2.VideoCapture(0)
personFrame = cv2.imread("PersonFrame.png",cv2.IMREAD_UNCHANGED)
h,w,_=personFrame.shape

overlay=io.ImageOverlayer()
if not webcam.isOpened() :
    exit()

while webcam.isOpened():
    lmList=[]
    detector = pd.PoseDetector()
    status, frame = webcam.read()

    if not status :
        webcam.waitKey()
        break

    BackH,BackW,_=frame.shape
    added_img=overlay.overlay_transparent(frame,personFrame,int(((BackW-1)/2)-((w-1)/2)),int(((BackH-1)/2)-((h-1)/2)))
    img = detector.findPose(frame)
    lmList = detector.findPosition(frame)

    cv2.imshow("frame",added_img)

    if cv2.waitKey(10) & 0xFF == ord('q') :
        break

webcam.release()
cv2.destroyAllWindows()
