import cv2
import numpy as np
from PIL import Image 
import pytesseract as pt 
import os 
import pytesseract as pt 
from itertools import chain

def Emergen(img_path):
    strg=""
    image = cv2.imread(img_path)
    (tH, tW) = image.shape[:2]
    img = image[743:845,00:tW]

    cv2.rectangle(img,(0, 0),(img.shape[1],img.shape[0]),(0, 255, 0), 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, img_bin) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = cv2.bitwise_not(img_bin)

    kernel_length_v = (np.array(img_gray).shape[1])//120
    #print(kernel_length_v)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_v)) 
    im_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=3)
    vertical_lines_img = cv2.dilate(im_temp1, vertical_kernel, iterations=3)

    kernel_length_h = (np.array(img_gray).shape[1])//50
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_h, 1))
    im_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(im_temp2, horizontal_kernel, iterations=3)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    table_segment = cv2.addWeighted(vertical_lines_img, 0.5, horizontal_lines_img, 0.5, 0.0)
    table_segment = cv2.erode(cv2.bitwise_not(table_segment), kernel, iterations=3)
    thresh, table_segment = cv2.threshold(table_segment, 0, 255, cv2.THRESH_OTSU)
   
    contours, hierarchy = cv2.findContours(table_segment, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(hierarchy)
    
    count = 0
    pos=0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (w <500):
            count += 1
            cropped = img[y:y + h, x-4:x + w]
            custom_config=r'--oem 3 --psm 6'
            text=pt.image_to_string(cropped, lang ="eng",config=custom_config) 
            str = ""
            list = []
            key=""
            value=""
            list = text.split("\n")
            if len(list) == 0:
                pass
            else:
                if len(list) == 1:
                    key = list[0]
                    value=""
                else:
                    #print(list)
                    key = list[0]
                    for i in list[1:]:
                        if i==' ' or '':
                            pass
                        else:
                            str = str +" "+i
                            value = str
            ind=key.find("Guardian")
            if key=="":
                pass
            if ind ==-1:
                qwe=key+":"+value
                if len(qwe)>7:
                    strg += qwe+"\n"
            else:
                key="Is Local Guardian"
                qwe=key+":"+value
                if len(qwe)>7:
                    strg += qwe+"\n"
        cv2.rectangle(img,(x, y),(x + w, y + h),(0, 255, 0), 0)
        pos += 1
    return (strg)