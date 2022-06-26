import numpy as np
import cv2
from matplotlib import pyplot as plt

def standard(imgFile1):
    # image read
    #a = "C:\\Users\\seokh\\OneDrive\\Desktop\KBSC\\project\\res_res.jpg"
    #b = "C:\\Users\\seokh\\OneDrive\\Desktop\\KBSC\\test_image\\1F.jpg"
    print(imgFile1[0])
    
    img1 = cv2.imread(imgFile1[0])

    #x,y,_ = img1.shape
    img1 =  cv2.resize(img1, dsize=(640, 480), interpolation=cv2.INTER_AREA)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    rtn, img1_thr = cv2.threshold(img1_gray, 127, 255, cv2.THRESH_BINARY)
    img_binary = cv2.bitwise_not(img1_thr)

    img_binary2 = img_binary.copy()
    img_binary2 = 255-img_binary
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))

    dilate = cv2.dilate(img_binary2, kernel2, anchor=(-1, -1), iterations=1)
    erode = cv2.erode(dilate, kernel2, anchor=(-1, -1), iterations=2)
    dilate2 = cv2.dilate(erode, kernel, anchor=(-1, -1), iterations=1)


    result = cv2.morphologyEx(img_binary2, cv2.MORPH_CROSS, kernel3)
    erode = cv2.dilate(result, kernel2, anchor=(-1, -1), iterations=1)
    dilate2 = cv2.erode(erode, kernel, anchor=(-1, -1), iterations=5)
    erode = cv2.dilate(dilate2, kernel2, anchor=(-1, -1), iterations=5)


    dst = np.concatenate((dilate, dilate2), axis=1)

    erode =  cv2.resize(erode, dsize=(420, 300), interpolation=cv2.INTER_AREA)

    cv2.imwrite("standard.jpg",erode)