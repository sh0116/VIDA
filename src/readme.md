---
# 👩‍🦯VIDA : 시각장애인을 위한 촉지도 제작 도구 주요 소스코드📚
---


<div align="center"><img src="../asset/logo.png" width="300">
</div>


## Summary🔫

| 파일명 | 설명 | 
| ------ | ------ | 
| FloorPlan_standard.py | 입력한 평면도 이미지를 자동 정규화하는 소스 |
| braille_transfer.py | 태깅된 건물의 구조와 건물명을 점자로 변환해주는 소스 |
| split_cubeV2.py | 정규화된 평면도 이미지를 3D 모델 제작을 위해 작은 Cube형태로 쪼개고 좌표와 크기를 반환하는 소스|
| excute_blender.py | Blender background python 을 실행하고 위에서 만들어진 데이터를 스크립트로 넘기는 소스 |
| blender_script.py | 태깅 데이터와 큐브 데이터를 기반으로 모델을 생성하는 소스 |

 <br> <br> <br>
## Main Function 👨‍🏫
🔦소스 코드의 주요 함수 소개

### FloorPlan_standard.py 
자동 정규화는 morphology transformation를 기반으로 만들어진 소스코드이다. <br>
아래 OpenCV 함수 중 침식(Erosion), 팽창(Dilation)을 활용해 만들었다.

>    dilate = cv2.dilate(img_binary2, kernel2, anchor=(-1, -1), iterations=1) <br>
>    erode = cv2.erode(dilate, kernel2, anchor=(-1, -1), iterations=2) <br>
>    dilate2 = cv2.dilate(erode, kernel, anchor=(-1, -1), iterations=1) <br>

