import sys
import glob
import os
import glob
import numpy as np
import cv2
from PIL import Image
import pytesseract
import re
import mysql.connector

mydb = mysql.connector.connect(
    host="sample.com",
    user="root",
    passwd="root",
    database="find"
)

#Detecting numberplate
def number_plate_detection(img):
    def clean2_plate(plate):
        gray_img = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    
        _, thresh = cv2.threshold(gray_img, 110, 255, cv2.THRESH_BINARY)
        if cv2.waitKey(0) & 0xff == ord('q'):
            pass
        num_contours,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
        if num_contours:
            contour_area = [cv2.contourArea(c) for c in num_contours]
            max_cntr_index = np.argmax(contour_area)
    
            max_cnt = num_contours[max_cntr_index]
            max_cntArea = contour_area[max_cntr_index]
            x,y,w,h = cv2.boundingRect(max_cnt)
    
            if not ratioCheck(max_cntArea,w,h):
                return plate,None
    
            final_img = thresh[y:y+h, x:x+w]
            return final_img,[x,y,w,h]
    
        else:
            return plate,None
    
    def ratioCheck(area, width, height):
        ratio = float(width) / float(height)
        if ratio < 1:
            ratio = 1 / ratio
        if (area < 1063.62 or area > 73862.5) or (ratio < 3 or ratio > 6):
            return False
        return True
    
    def isMaxWhite(plate):
        avg = np.mean(plate)
        if(avg>=115):
            return True
        else:
            return False
    
    def ratio_and_rotation(rect):
        (x, y), (width, height), rect_angle = rect
    
        if(width>height):
            angle = -rect_angle
        else:
            angle = 90 + rect_angle
    
        if angle>15:
            return False
    
        if height == 0 or width == 0:
            return False
    
        area = height*width
        if not ratioCheck(area,width,height):
            return False
        else:
            return True
    
    
    img2 = cv2.GaussianBlur(img, (5,5), 0)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    img2 = cv2.Sobel(img2,cv2.CV_8U,1,0,ksize=3)	
    _,img2 = cv2.threshold(img2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
    morph_img_threshold = img2.copy()
    cv2.morphologyEx(src=img2, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
    num_contours, hierarchy= cv2.findContours(morph_img_threshold,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img2, num_contours, -1, (0,255,0), 1)
    
    
    for i,cnt in enumerate(num_contours):
        min_rect = cv2.minAreaRect(cnt)
        if ratio_and_rotation(min_rect):
            x,y,w,h = cv2.boundingRect(cnt)
            plate_img = img[y:y+h,x:x+w]
            if(isMaxWhite(plate_img)):
                clean_plate, rect = clean2_plate(plate_img)
                if rect:
                    fg=0
                    x1,y1,w1,h1 = rect
                    x,y,w,h = x+x1,y+y1,w1,h1
                    plate_im = Image.fromarray(clean_plate)
                    cv2.imshow("plate",clean_plate)
                    cv2.waitKey(10000)
                    text = pytesseract.image_to_string(plate_im, lang='eng')
                    return text


print("Detect number plate:\n")

array=[]

dir = os.path.dirname(__file__)

for img in os.listdir("Dataset"):
    img=cv2.imread(dir+"/Dataset/"+img)    
   # img = cv2.resize(img,(1024,1024))
    number_plate=number_plate_detection(img)
    res2 = str(number_plate)
    res2 = res2.replace(" ", "")
    array.append(res2.upper())
    cv2.destroyAllWindows()
    mycursor = mydb.cursor()
    if res2 != "None":
        mycursor.execute("update findV set Latitude = '-1.111',Longitude = '0.1111' where Vehno = %s", (res2.upper().strip(),))
        mycursor.execute("insert into findBlock(Vehno,Location,latitude,longitude) values(%s,'Bangalore','9.854980','78.500504');",(res2.upper().strip(),))
    else:
        print("No number plate detected")
    mydb.commit()
    print(res2)

    			
