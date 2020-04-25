import cv2
import os
import pytesseract

def toText(location):
    image = cv2.imread(location)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255,255,255), 2)

    # Remove verticle
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, verticle_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255,255,255), 2)
    linux = False
    for i in location:
        if(i == '/'):
            linux = True
            break
    array_0 = []
    array_1 = []
    path = ''
    Tpath = ''
    if(linux):
        array_0 = location.split('/')
        array_1 = location.split('/')
        array_0[-1] = 'temp.' + array_0[-1].split('.')[-1]
        Tpath = '/'
        for item in array_0:
            Tpath = os.path.join(Tpath,item)
        array_1[-2] = 'input'
        array_1[-1] = array_1[-1].split('.')[0]+'.txt'
        path = '/'
        for item in array_1:
            path = os.path.join(path,item)
    else:
        array_0 = location.split('\\')
        array_1 = location.split('\\')
        array_0[-1] = 'temp.' + array_0[-1].split('.')[-1]
        Tpath = array_0[0]+'\\'
        for item in range(1,len(array_0)):
            Tpath = os.path.join(Tpath,array_0[item])
        array_1[-2] = 'input'
        array_1[-1] = array_1[-1].split('.')[0]+'.txt'
        path = array_1[0]+'\\'
        for item in range(1,len(array_1)):
            path = os.path.join(path,array_1[item])
    file=open(path,'w')
    cv2.imwrite(Tpath,image)
    img=cv2.imread(Tpath)
    custom_config=r'--oem 3 --psm 6'
    file.write(pytesseract.image_to_string(img,config=custom_config))
    file.close()
