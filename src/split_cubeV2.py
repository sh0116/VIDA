import numpy as np, cv2

def func_find(img):
    x,y = img.shape
    box = list()
    visit = set()
    x_dict = dict()
    for i in range(x-5):
        for j in range(y-5):
            cnt = 0
            while True:
                for cnt_plus in range(5,0,-1):
                    if (i,j+cnt+cnt_plus) not in visit and img[i][j+cnt+cnt_plus].tolist() == 0:
                        cnt+=cnt_plus
                        visit.add((i,j+cnt))
                        break
                else:
                    break
            if cnt:
                if i not in x_dict.keys():
                    x_dict[i] = list()

                x_dict[i].append([j,j+cnt])
                box.append([j,j+cnt,i,i])
    x_dict_keys = sorted(x_dict.keys())
    box_sorted = list()
    pre = 0

    for i in range(len(x_dict_keys)):
        if (x_dict_keys[i]-x_dict_keys[pre]) == (i-pre) and x_dict[x_dict_keys[pre]] == x_dict[x_dict_keys[i]]:
            continue
        else:
            #print(x_dict[x_dict_keys[i-1]])
            #print(x_dict[x_dict_keys[pre]])
            #print("____________________________")
            for temp in x_dict[x_dict_keys[i-1]]:
                box_sorted.append(temp+[x_dict_keys[pre],x_dict_keys[i-1]])
            pre = i

    #for i in x_dict_keys:
    #    print(i,x_dict[i])
 
    return box_sorted

def main():
    # B1_temp 1F_temp 2F_temp 3F_temp
    # test1_temp FP_temp
    img = cv2.imread('.\\temp.jpg')
    img = cv2.flip(img, 1)
    img = cv2.resize(img,dsize=(420,300), interpolation=cv2.INTER_AREA)
    img2 = img.copy()
    img2 = 255-img2
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgray, 127, 255, 0)
    boxs = func_find(thresh)
    print("successful : split cube {}".format(len(boxs)))
    for box in boxs:
        x1,x2,y1,y2 = box
        img = cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),1)
    #cv2.imshow('approx', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #7,8,10,14,15,17

    

    with open(r'sales.txt', 'w') as fp:
        fp.write("{}".format(boxs))

    return boxs
if __name__=="__main__":
    main()
