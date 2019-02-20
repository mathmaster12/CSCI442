#Part two of assignment 2

import numpy as np
import cv2
import imutils

#Set the variable of stationary to none
stationary = None

cap = cv2.VideoCapture(0) #Capture live video from Webcam
cv2.namedWindow("Image") #Create window called Image
cv2.namedWindow("Gray")#Create window called Gray
cv2.namedWindow("Channel Image")#Create window called Channel Image
cv2.namedWindow("Abs Diff")#Create window called Abs Diff

while(1):
    # Take each frame from webcam
    status, frame = cap.read()

    #set the variable of motion to 0
    motion = 0

    #Convert the video from BGR to GRAY and then blur the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    # if first time through while loop set stationary to gray
    if stationary is None:
        stationary = gray
        continue

    #check for differences between the current gray frame and the stationary frame
    absdiff_frame = cv2.absdiff(stationary,gray)
    thresh_frame = cv2.threshold(absdiff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    #find contour of image
    cnts = cv2.findContours(thresh_frame.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    cv2.imshow("Image",frame)  #display original video
    cv2.imshow("Gray",gray) #display video in Gray scale
    cv2.imshow("Channel Image", thresh_frame) #display video in HSV
    cv2.imshow("Abs Diff", absdiff_frame) #display video that is the absolute difference of two frames

    #Set stationary as the current gray frame 
    stationary = gray
    
    k = cv2.waitKey(1)
    if k == 27:
        break

# Release the capture and destroy all the windows when program ends
cap.release()
cv2.destroyAllWindows()
