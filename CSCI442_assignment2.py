#Part one of assingment 2

import numpy as np
import cv2

def nothing(x):
    pass

cap = cv2.VideoCapture(0) #Capture live video from Webcam
cv2.namedWindow("Video") #Create window called Video
cv2.namedWindow("HSV") #Create window called HSV
cv2.namedWindow("Black+White") #Create window called Black+White

#Minimum and maximum value for HUE in HSV
minH = 0
maxH = 179 

#Minimum and maximum value for SATURATION in HSV
minS = 0 
maxS = 255

#Minimum and maximum value for VALUE in HSV
minV = 0
maxV = 255

#Create trackbars for the minimum and maximum value for HUE in HSV
cv2.createTrackbar('lowH','HSV',minH,179,nothing)
cv2.createTrackbar('highH','HSV',maxH,179,nothing)

#Create trackbars for the minimum and maximum value for SATURATION in HSV
cv2.createTrackbar('lowS','HSV',minS,255,nothing)
cv2.createTrackbar('highS','HSV',maxS,255,nothing)

#Create trackbars for the minimum and maximum value for VALUE in HSV
cv2.createTrackbar('lowV','HSV',minV,255,nothing)
cv2.createTrackbar('highV','HSV',maxV,255,nothing)

#On left mouse click of HSV display location and values of H, S, and V
def find_Values(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        px = hsv[y,x]    
        print ("You clicked at [",y,",",x,"]: H is",px[0],",","S is",px[1],",","V is",px[2],".")
        
#Set mouse click event
cv2.setMouseCallback('HSV',find_Values) 

while(1):
    # Take each frame from webcam
    status, frame = cap.read()

    #Get the trackbars position for the minimum and maximum of HUE in HSV
    minH = cv2.getTrackbarPos('lowH', 'HSV')
    maxH = cv2.getTrackbarPos('highH', 'HSV')

    #Get the trackbars position for the minimum and maximum of SATURATION in HSV
    minS = cv2.getTrackbarPos('lowS', 'HSV')
    maxS = cv2.getTrackbarPos('highS', 'HSV')
    
    #Get the trackbars position for the minimum and maximum of  VALUE in HSV
    minV = cv2.getTrackbarPos('lowV', 'HSV')
    maxV = cv2.getTrackbarPos('highV', 'HSV')
    
    # Convert the video from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Find the inRange values of HSV to obtain Black and White scaled image 
    min_hsv = np.array([minH, minS, minV])
    max_hsv = np.array([maxH, maxS, maxV])
    scaled = cv2.inRange(hsv, min_hsv, max_hsv)
    
    #Show the HSV image with the adjusted range of values
    hsv = cv2.bitwise_and(hsv,hsv, mask = scaled)

    #Dilate the scaled image 
    scaled = cv2.dilate(scaled, None, iterations = 2) 
    
    cv2.imshow("Video",frame) #display original video
    cv2.imshow("HSV",hsv) #display video in HSV
    cv2.imshow("Black+White", scaled) #display the black+white scaled version of the hsv video

    k = cv2.waitKey(1)
    if k == 27:
        break

# Release the capture and destroy all the windows when program ends
cap.release()
cv2.destroyAllWindows()
