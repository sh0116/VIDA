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

### braille_transfer.py
Hangul to Braille Converter 라이브러리 hbcvt를 사용하여 만든 소스코드이다.<br>

>        for i in hbcvt.h2b.text(place):
>         for j in i[1:]:
>             for k in j:
>                 braille_list.append(k[1:][0][0])


### split_cubeV2.py
Binary Image로 만든 평면도를 X값을 기준으로 전수 조사한다 0과 1로 구분하고 시작하는 부분과 끝나는 부분을 찾아 X길이가 1인 긴 막대를 생성한다.
<br>

>     for i in range(x-5):
>        for j in range(y-5):
>            cnt = 0
>            while True:
>                for cnt_plus in range(5,0,-1):
>                    if (i,j+cnt+cnt_plus) not in visit and img[i][j+cnt+cnt_plus].tolist() == 0:
>                        cnt+=cnt_plus
>                        visit.add((i,j+cnt))
>                        break
>                else:
>                    break
>            if cnt:
>                if i not in x_dict.keys():
>                    x_dict[i] = list()
>
>                x_dict[i].append([j,j+cnt])
>                box.append([j,j+cnt,i,i])

X길이가 1인 긴 막대를 모두 출력하면 모델 생성시 과부하가 걸린다.<br>
X의 위치를 기준으로 막대의 처음과 끝의 좌표가 같은 막대들을 찾아 하나로 합친다. <br>
즉 같은 크기, 같은 위치에 있는 막대를 합쳐 X가 2인 긴 막대를 만드는 과정이다
<br>
>      for i in range(len(x_dict_keys)):
>          if (x_dict_keys[i]-x_dict_keys[pre]) == (i-pre) and x_dict[x_dict_keys[pre]] == x_dict[x_dict_keys[i]]:
>              continue
>          else:
>              for temp in x_dict[x_dict_keys[i-1]]:
>                  box_sorted.append(temp+[x_dict_keys[pre],x_dict_keys[i-1]])
>              pre = i



### excute_blender.py
현재 Blender의 Python Lib인 BPY의 최신 버전이 호환성 문제로 배포가 안됐다.<br>
Blender를 백그라운드로 돌리면서 내부에 존재하는 Python Console를 사용하면 최신 버전의 BPY를 사용할 수 있다 <br>
Blender background에서 돌아가는 프로세스로 메인 인터페이스 프로세스와 별개의 프로세스로 구성된다 <br>
>      os.system("C:\\VIDA\\Blender_dir\\blender.exe --background --python C:\\VIDA\\FloorPlan\\blender_script.py "+tagstring.replace(" ","")+" "+str(title).replace(" ",""))


### blender_script.py
Function 
- Cube객체를 생성하는 함수
- UV객체(반구)를 생성하는 함수
- 점자를 제작하는 함수
- 건물 벽을 제작하는 함수
- 건물의 메인 보드를 제작하는 함수
- 촉지도의 Summary를 만드는 함수 
- 촉지도를 모델 파일(stl)로 반환하는 함수
