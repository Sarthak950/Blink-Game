# All the dependencies
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
from pynput.keyboard import Key, Controller

# listning to the keyboard
keyboard = Controller()

# accessing the webcam
cap = cv2.VideoCapture(0)

# adding mesh to the face
detector = FaceMeshDetector(maxFaces=1)

# Accessing only the required points 
# only the surround the right eye
leftEyeLandmarks = [ 22, 22, 23, 24, 26, 110, 157, 159, 160, 161, 130, 243]
# can be modified for left eye as well


# Game Loop
while True:
    # reading the camera
    retval, frame = cap.read()
    
    #reading the mesh
    frame ,faces = detector.findFaceMesh(frame,draw= False)
    
    if faces:       #if an face is detected 
        
        face = faces[0]
        
        for i in leftEyeLandmarks:      # highliting the eye
            cv2.circle(frame, face[i], 5, (255, 0, 255), cv2.FILLED)

        # getting the eye points
        topEyelid = face[159]       # top eyelid
        bottomEyelid = face[23]     # bottom eyelid
        leftCorner = face[130]      # left corner
        rightCorner = face[243]     # right corner
        
        lengthVer,_= detector.findDistance(topEyelid, bottomEyelid)     # vertile line distance
        lengthHor,_= detector.findDistance(leftCorner, rightCorner)     # horizontal line distance
        
        cv2.line (frame, topEyelid, bottomEyelid, (0, 200, 0), 3)       # drawing the vertical line
        cv2.line(frame, leftCorner, rightCorner, (0, 200, 0), 3)        # drawing the horizontal line

        ratio = int((lengthVer/lengthHor)*100)   # calculating the ratio
        # if u move the eye away from the camera the length of the vertical line decrease
        # and can cause false detection
        # so we use horizontal line to normalize the ratio
        # the ratio only change when eye open and close
        
        
        eye_init_ratio = 32     #initial ration of the eye change if u want
        
        
        if ratio < eye_init_ratio:          # if the ratio is less than the initial ratio
            keyboard.press(Key.space)      #pressing the space bar
            
        if ratio > eye_init_ratio:          # if the ratio is greater than the initial ratio
            keyboard.release(Key.space)     # releasing the space bar
            
    if not retval:      # if camera is not working or no face detected
        break           # break the loop
                                                                                                
    cv2.imshow("BlinkDector2.0", frame)     # showing the frame
    
    key = cv2.waitKey(1)    # waiting for the key press
    if key == 27:           # if esc is pressed
        break               # break the loop

cap.release()       # releasing the camera  
cv2.distroyAllWindows()     # closing all the windows


# i know code is not perfect but it works
# thanks for reading 