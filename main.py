import cv2
import numpy as np

import cv2
import PoseDetector as pd

#벡터 1로 정규화
## 12번을 기준으로 벡터 1로 만들어 정규화 해볼 예정

## 1. 기준벡터(의사의 좌표값)을 벡터 1로 정규화한다.
## 2. 의사의 크기/크기 1을 나눈 n배수를 구한다.
## 3. 환자의 x,y값을 벡터 1값을 가지는 x,y좌표로 바꾼다. (x/dist,y/dist)
## 4. 의사의 n배수를 곱하면, 두 크기가 같아진다?
## ** 의사를 환자한테 맞춘다. 환자 영상을 볼 수 있기 때문 ?

#######
# 12 - 14 | 14 - 16
# 11 - 13 | 13 - 15
# 12 - 24 | 11 - 23
# 24 - 26 | 26 - 28
# 23 - 25 | 25 - 27
#######
def adjustStd(patient, doctor):
    thresh=[[12,14],[14,16],[11,13],[13,15],[12,24],[11,23],[24,26],[26,28],[23,25],[25,27],[28,32],[28,30],[27,29],[27,31]]
    #thresh의 리스트 idx번에 해당하는 x,y좌표 리스트를 numpy화
    #patient Standard 의 줄인말로, 환자 기준치를 의미한다.

    for idx in range(len(thresh)) :
        patiStd1 = np.array(patient[thresh[idx][0]])
        patiStd2 = np.array(patient[thresh[idx][1]])
        patiDist=np.linalg.norm(patiStd1-patiStd2) # 두 좌표간의 길이을 측정하는 함수

        doctStd1 = np.array(doctor[thresh[idx][0]])
        doctStd2 = np.array(doctor[thresh[idx][1]])
        doctDist=np.linalg.norm(doctStd1-doctStd2)

        newDoct2=doctStd1+((doctStd2-doctStd1)/doctDist)*patiDist
        doctor[thresh[idx][1]]=newDoct2 #새로운 값으로 초기화

    return doctor

#환자의 동영상에 매치된 의사의 스켈레톤을 보여줌!!!
#계산된 의사의 좌표값은 사라짐. DB에 저장하지 않는다는 점.
file_name="test1.mp4" #test1을 환자라고 생각한다.
detector = pd.PoseDetector() #환자용
detector1 = pd.PoseDetector() #의사용

cap = cv2.VideoCapture(file_name) #환자 동영상을 읽는다.

file_name1="test.mp4" #의사용
cap1 = cv2.VideoCapture(file_name1) #의사의 데이터를 읽는다.

##저장용
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
#mp4확장자 선택을 위함
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#앞 string 파일 이름
out=cv2.VideoWriter("patint1.mp4",fourcc, fps, (w, h))
while (cap.isOpened()):
    success, target_image = cap.read() #환자 동영상을 읽어온다.
    _,skeleton_image=cap1.read() #의사 동영상을 읽어온다.

    #두 이미지의 크기 정규화 : 의사의 이미지 -> 환자의 이미지 크기로 키우거나 줄임.
    skeleton_image = cv2.resize(skeleton_image, (target_image.shape[1], target_image.shape[0]))

    skeleton_image = detector.findPose(skeleton_image)     #의사의 이미지로부터 좌표값을 찾는다
    target_image=detector1.findPose(target_image)       #환자의 이미지로부터 좌표값을 찾는다

    lmList,doctor = detector.findPosition(skeleton_image) #의사
    lmList2,patient = detector1.findPosition(target_image) #환자

    adjustStd(patient, doctor)
    target_image=detector1.drawPose(target_image,doctor,100)    #의사 색

    if skeleton_image is None:
        break
    out.write(target_image) #data저장용
    cv2.imshow('img2',target_image)
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
#송수영 이미지 프레임 2
#영상 두개 가져와서 길이 일치시키기
# try:
#     json_data={}
#     with open(file_path) as json_file:
#         json_data=json.load(json_file)
#
#         dic={}
#         dic["jiwoo"]={
#             "apple":3,"orange":5
#         }
#
#         json_data.update(dic)
#         print(json_data)
#
#         with open('fruit.json','w') as make_file :
#             fruit=json.dump(json_data,make_file,indent='\t')
#
# except :
#     dic={}
#     dic["suyoung"]={
#         "apple":3,"orange":5
#     }
#
#     with open('fruit.json','w') as make_file :
#         fruit=json.dump(dic,make_file,indent='\t')


##수학식
    #c=np.array([1,1])
    #d=np.array([5,5])

    #dist2=np.linalg.norm(d-c)
    #c1=c+((d-c)/dist2)*dist
