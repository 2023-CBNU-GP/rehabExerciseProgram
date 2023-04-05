# import cv2
# import PoseDetector as pd
# import ImageOverlayer as io
# import AngleFinder as af
# import math
#real time -저장용
#
# file_path = "/Users/songsuyeong/PycharmProjects/pythonProject/tmp04.mp4"
# webcam = cv2.VideoCapture(0)
# personFrame = cv2.imread("PersonFrame.png",cv2.IMREAD_UNCHANGED)
# h,w,_=personFrame.shape
# width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)
# size = (int(width), int (height))
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter(file_path, fourcc, 10, size)
#
# overlay=io.ImageOverlayer()
# while webcam.isOpened():
#     lmList=[]
#     detector = pd.PoseDetector()
#     status, frame = webcam.read()
#
#     if not status :
#         webcam.waitKey()
#         break
#     out.write(frame)
#     BackH,BackW,_=frame.shape
#     added_img=overlay.overlay_transparent(frame,personFrame,int(((BackW-1)/2)-((w-1)/2)),int(((BackH-1)/2)-((h-1)/2)))
#     img = detector.findPose(frame)
#     lmList = detector.findPosition(frame)
#
#     cv2.imshow("frame",added_img)
#     if cv2.waitKey(10) & 0xFF == ord('q') :
#         break
#
# webcam.release()
# cv2.destroyAllWindows()
