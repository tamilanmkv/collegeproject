from pyexpat import model
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import os
import pytesseract

# swith video mode 
##read video and and read image
#cap = cv2.VideoCapture(0)
#cap.set(3,640)
#cap.set(4,480)
#cap.set(10,100)
#
#while(True):
#    # Capture frame-by-frame
#    ret, frame = cap.read()
#    # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



#read video from file
cap = cv2.VideoCapture('/home/mkv/Downloads/test.mp4')
#display every frame
while(cap.isOpened()):
    ret, frame = cap.read()
    #cv2.imshow('frame',frame)
    if ret == True:
        #cv2.imshow('frame',frame)
        img = frame.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 30, 200) #Edge detection

        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
            
            
            
        location
        mask = np.zeros(gray.shape, np.uint8)
        if location is not None:
            new_image = cv2.drawContours(mask, [location], 0,255, -1)
            new_image = cv2.bitwise_and(img, img, mask=mask)
            #plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
            (x,y) = np.where(mask==255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+1, y1:y2+1]
            #reader = easyocr.Reader(['en'])
            #result = reader.readtext(cropped_image)
            result = pytesseract.image_to_string(cropped_image, lang='eng')
        else:
            result = "No text found"

        print(result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    else:
        break

#img = cv2.imread('Dataset/1.jpeg')





#text = result[0][-2]
#font = cv2.FONT_HERSHEY_SIMPLEX
#res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
#res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
#plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))




