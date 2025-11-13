import numpy as np
import logging
import mediapipe as mp
import cv2

# points for landmarked image
NOSE = 0
LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3
RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6
LEFT_EAR = 7
RIGHT_EAR = 8
MOUTH_LEFT = 9
MOUTH_RIGHT = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_HEEL = 29
RIGHT_HEEL = 30
LEFT_FOOT = 31
RIGHT_FOOT = 32

# TODO Get measurements from the scale calculated
# TODO Use both images , currently just uses front view
class MeasurementHandler:
    def __init__(self, imageHandler, user_height=188, debug=True):
        self.imageHandler = imageHandler
        self.measurementData = None
        self.user_height = user_height # currently in cm for testing
        self.debug = debug

        # landmarked points, need to be converted in order to use in image
        self.frontLandmarks = self.imageHandler.detectedImage[0].pose_landmarks[0]
        self.sideLandmarks = self.imageHandler.detectedImage[1].pose_landmarks[0]

        # image shapes, used for calculating points
        self.front_h,self.front_w,_ = self.imageHandler.annotatedImage[0].shape
        self.side_h,self.side_2,_ = self.imageHandler.annotatedImage[0].shape

        # segmented image, used to find new points not given and for printing
        self.front_segmented_image =  self.imageHandler.segmentedImage[0]
        self.side_segmented_image = self.imageHandler.segmentedImage[1]
        print("Measurement Handler Stuff ...")
    

    def saveToCSV(self):
        pass
    

    # Translate normalized landmark to pixel coordinates CV2 can use
    def getPixel(self, index, landmarks, image_h, image_w):
        x_coord = int(landmarks[index].x * image_w)
        y_coord = int(landmarks[index].y * image_h)
        return (x_coord,y_coord)
    

    def checkBackground(self, pixel, segmentedImage, direction ='up', ):
        """
        Check if a pixel is next to the background of a segmented image.
        Used for making new points that are important for sizing but mediapipe does not provide

        Args: 
            pixel (int, int): Pixel coordinates on segmented image, has gone through getPixel()
            segmentedImage: Processed segmented image
            direction (string): Which direction are we checking for background default is 'up' 

        Returns:
            (bool) : True if background found, False if not
        """
        (x,y) = pixel
        bgColor = [4, 244, 4]

        if direction == 'up':       
            if (np.all(segmentedImage[y-1,x] == bgColor)): # check 1 up
                if(np.all(segmentedImage[y-2,x] == bgColor)): # check 2 up
                    return True
            return False
        
        elif direction == 'down':
            if (np.all(segmentedImage[y+1,x] == bgColor)): # check 1 down
                if(np.all(segmentedImage[y+2,x] == bgColor)): # check 2 down
                    return True
            return False
        
        elif direction == 'right':
            if (np.all(segmentedImage[y,x+1] == bgColor)): # check 1 right
                if(np.all(segmentedImage[y,x+2] == bgColor)): # check 2 right
                    return True
            return False
        
        elif direction == 'left':
            if (np.all(segmentedImage[y,x-1] == bgColor)): # check 1 left
                if(np.all(segmentedImage[y,x-2] == bgColor)): # check 2 left
                    return True
            return False
        

    # Find the middle pixel between both feet for a better height measurement
    def getMiddlePx(self):
        left_px = self.getPixel(LEFT_FOOT, self.frontLandmarks, self.front_h, self.front_w)
        right_px = self.getPixel(RIGHT_FOOT, self.frontLandmarks, self.front_h, self.front_w)
        
        middle_px = (
                int((left_px[0] + right_px[0]) / 2),
                int((left_px[1] + right_px[1]) / 2)
        )

        return middle_px
    

    def getMeasurementScale (self):
        """
        Uses user height to get a scale for 
        Finds actual top-of-head pixel starting from noise
        Uses top-of-head pixel and midpoint pixel to get height, used for cm/pixel scale
        """

        # Get the two points we need for height cal
        mid_px = self.getMiddlePx()
        nose_px = self.getPixel(NOSE, self.frontLandmarks, self.front_h, self.front_w)

        # Start from nose and keep moving up till we hit background, then we know we are at top of head
        x,y = nose_px
        for y_pixel in range(y, 0, -1):
            temp_px = (x, y_pixel)
            if self.checkBackground(temp_px, segmentedImage= self.front_segmented_image, direction='up'):
                break

        # Show the pixel found and draw a height line on the segemented image
        # cv2.circle(segmentedImage, temp_px, 3, color=(0, 0, 0), thickness=-1)
        # cv2.line(segmentedImage, mid_px, temp_px, (255,0,0), 2) 
        # print(f"Top Pixel found = {temp_px} with color {segmentedImage[(temp_px)]}")

        pixel_height = abs(mid_px[1] - temp_px[1])
        # print(pixel_height)

        self.scale = self.user_height/pixel_height
        # print(self.scale)


    def getHipPx(self):
        front_right_hip = self.getPixel(RIGHT_HIP, self.frontLandmarks, self.front_h, self.front_w)
        front_left_hip = self.getPixel(LEFT_HIP, self.frontLandmarks, self.front_h, self.front_w)
        x,y = front_right_hip
        for x_pixel in range(x,self.front_w, 1):
            temp_px = (x_pixel,y)
            if self.checkBackground(temp_px, segmentedImage=self.front_segmented_image, direction="right"):
                break
            
        front_right_hip_px = temp_px
        # print(f"New hip pixel printed {temp_px}")
        cv2.circle(self.front_segmented_image, temp_px, 15, color=(255,0,50), thickness=-1)

        x,y = front_left_hip
        for x_pixel in range(x, 0, -1):
            temp_px = (x_pixel,y)
            if self.checkBackground(temp_px, segmentedImage=self.front_segmented_image, direction="left"):
                break
        front_left_hip_px = temp_px
        cv2.circle(self.front_segmented_image, temp_px, 15, color=(255,0,50), thickness=-1)

        front_view_hip_pixel_dist = np.linalg.norm(np.array(front_right_hip_px) - np.array(front_left_hip_px)) # Front view pixel distance

        return front_view_hip_pixel_dist

    

    def getMeasurements(self):

        self.getMeasurementScale()
        # Chest / Bust

        # Shoulder to Hip (length for shirts)

        # sleeve length (long)

        #sleeve length (short)

        #shoulders


        # Waist

        # Hip 
        hip_pixel_dist = self.getHipPx()
        hip_width = hip_pixel_dist * self.scale
        # print(f"Hip Size (cm):{hip_width:.2f}")

        # Hip to inseam

        #Inseam to floor (pant length)

        # Hip to floor (not usually used for pants but why not)
