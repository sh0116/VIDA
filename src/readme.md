# 주요 소스코드

| 파일명 | 설명 | 
| ------ | ------ | 
| FloorPlan_standard.py | 입력한 평면도 이미지를 자동 정규화하는 소스 |
| braille_transfer.py | 태깅된 건물의 구조와 건물명을 점자로 변환해주는 소스 |
| split_cubeV2.py | 정규화된 평면도 이미지를 3D 모델 제작을 위해 작은 Cube형태로 쪼개고 좌표와 크기를 반환하는 소스|
| excute_blender.py | Blender background python 을 실행하고 위에서 만들어진 데이터를 스크립트로 넘기는 소스 |
| blender_script.py | 태깅 데이터와 큐브 데이터를 기반으로 모델을 생성하는 소스 |

