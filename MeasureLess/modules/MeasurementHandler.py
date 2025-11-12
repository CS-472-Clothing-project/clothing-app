import numpy as np
import logging
import mediapipe as mp
import cv2

# points for landmarked image
NOSE = 0
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_FOOT = 31
RIGHT_FOOT = 32
LEFT_EYE = 2
RIGHT_EYE = 5
LEFT_HEEL = 29
RIGHT_HEEL = 30
LEFT_EAR = 7
RIGHT_EAR = 8
RIGHT_HIP = 24
LEFT_HIP = 23

# TODO Get measurements from the scale calculated
# TODO Use both images , currently just uses front view
class MeasurementHandler:
    def __init__(self, imageHandler, user_height=72, debug=True):
        self.imageHandler = imageHandler
        self.measurementData = None
        self.user_height = user_height
        self.debug = debug
        self.landmarks = self.imageHandler.detectedImage[0].pose_landmarks[0]
        self.image_h,self.image_w,_ = self.imageHandler.annotatedImage[0].shape
        print("Measurement Handler Stuff ...")
    
    def saveToCSV(self):
        pass
    
    # Translate normalized landmark to pixel coordinates CV2 can use
    def getPixel(self, index):
        x_coord = int(self.landmarks[index].x * self.image_w)
        y_coord = int(self.landmarks[index].y * self.image_h)
        return (x_coord,y_coord)

    # find the middle pixel between both feet for a better height measurement
    def getMiddlePx(self):
        left_px = self.getPixel(LEFT_FOOT)
        right_px = self.getPixel(RIGHT_FOOT)
        
        middle_px = (
                int((left_px[0] + right_px[0]) / 2),
                int((left_px[1] + right_px[1]) / 2)
        )

        return middle_px
    
    # Does 2 things:
    #   First it finds the actual top height point starting from nose
    #   Second it uses that point and midpoint to calculate hieght in pixels
    #   this height is then used to get a scale of cm/pixels
    def getMeasurementScale (self):
        # Get the two points we need for height cal
        mid_px = self.getMiddlePx()
        nose_px = self.getPixel(NOSE)

        # draw on segmented image
        segmentedImage = self.imageHandler.segmentedImage[0]

        # cv2.circle(segmentedImage, mid_px, 2, color=(50, 255, 255), thickness=-1)
        # cv2.line(segmentedImage, mid_px, nose_px, (255,0,0), 2) # temp height line from middle of feet to nose

        # Helper to continuously go up until we hit segmentation background
        # used to get the top of the head that mediapipe does not have
        def checkIfBackground(pixel):
            x = pixel[0]
            y = pixel[1]
            bgColor = [4, 244, 4]
            if (np.all(segmentedImage[y-1,x] == bgColor)): # check 1 up
                if(np.all(segmentedImage[y-2,x] == bgColor)): # check 2 up
                    return True
                
            return False
          
        # Use the checkIfBackground function on the nose to get top of head
        x,y = nose_px
        # print(checkIfBackground(nose_px))
        for y_pixel in range(y, 0, -1):
            temp_px = (x, y_pixel)
            if checkIfBackground(temp_px):
                break

        # Show the pixel found and draw a height line on the segemented image
        cv2.circle(segmentedImage, temp_px, 3, color=(0, 0, 0), thickness=-1)
        cv2.line(segmentedImage, mid_px, temp_px, (255,0,0), 2) 
        # print(f"Top Pixel found = {temp_px} with color {segmentedImage[(temp_px)]}")

        pixel_height = abs(mid_px[1] - temp_px[1])
        # print(pixel_height)

        self.scale = self.user_height/pixel_height
        # print(self.scale)
