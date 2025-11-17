import numpy as np
import logging
import mediapipe as mp
import cv2
import pandas as pd
from math import pi, sqrt

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

class MeasurementHandler:
    def __init__(self, imageHandler, user_height=188, debug=True):
        self.imageHandler = imageHandler
        self.measurementData = None
        self.user_height = user_height # currently in inches for testing
        self.debug = debug

        # landmarked points, need to be converted in order to use in image
        self.front_landmarks = self.imageHandler.detectedImage[0].pose_landmarks[0]
        self.side_landmarks = self.imageHandler.detectedImage[1].pose_landmarks[0]

        # image shapes, used for calculating points
        self.front_h,self.front_w,_ = self.imageHandler.annotatedImage[0].shape
        self.side_h,self.side_w,_ = self.imageHandler.annotatedImage[1].shape

        # segmented image, used to find new points not given and for printing
        self.front_segmented_image =  self.imageHandler.segmentedImage[0]
        self.side_segmented_image = self.imageHandler.segmentedImage[1]
        print("Measurement Handler Stuff ...")
    

    def saveToCSV(self, hip, shoulder):
        print(f"Saving measurements to results/results.csv")
        df = pd.DataFrame([{
            "Hip Size":hip,
            "Shoulder Size":shoulder,
        }])
        df.to_csv("results/result.csv", mode="w", header=True, index=False)
    

    # Translate normalized landmark to pixel coordinates CV2 can use
    def getPixel(self, index, landmarks, image_h, image_w):
        x_coord = int(landmarks[index].x * image_w)
        y_coord = int(landmarks[index].y * image_h)
        return (x_coord,y_coord)
    

    def checkBackground(self, pixel, segmented_image, direction ='up', ):
        """
        Check if a pixel is next to the background of a segmented image.
        Used for making new points that are important for sizing but mediapipe does not provide

        Args: 
            pixel (int, int): Pixel coordinates on segmented image, has gone through getPixel()
            segmented_image: Processed segmented image
            direction (string): Which direction are we checking for background default is 'up' 

        Returns:
            (bool) : True if background found, False if not
        """
        (x,y) = pixel
        bg_color = [4, 244, 4]

        if direction == 'up':       
            if (np.all(segmented_image[y-1,x] == bg_color)): # check 1 up
                if(np.all(segmented_image[y-2,x] == bg_color)): # check 2 up
                    return True
            return False
        
        elif direction == 'down':
            if (np.all(segmented_image[y+1,x] == bg_color)): # check 1 down
                if(np.all(segmented_image[y+2,x] == bg_color)): # check 2 down
                    return True
            return False
        
        elif direction == 'right':
            if (np.all(segmented_image[y,x+1] == bg_color)): # check 1 right
                if(np.all(segmented_image[y,x+2] == bg_color)): # check 2 right
                    return True
            return False
        
        elif direction == 'left':
            if (np.all(segmented_image[y,x-1] == bg_color)): # check 1 left
                if(np.all(segmented_image[y,x-2] == bg_color)): # check 2 left
                    return True
            return False
        
    def getPointFromBackground(self, point, segmented_image, direction):
        x,y = point

        if direction == "right":
            for x_pixel in range(x, segmented_image.shape[1], 1):
                temp = (x_pixel, y)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp

        elif direction == "left":
            for x_pixel in range(x, 0, -1):
                temp = (x_pixel, y)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp

        elif direction == "up":
            for y_pixel in range(y, 0, -1):
                temp = (x, y_pixel)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp

        elif direction == "down":
            for y_pixel in range(y, segmented_image.shape[0], 1):
                temp = (x, y_pixel)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp


    # Find the middle pixel between both feet for a better height measurement
    def getMiddlePx(self):
        left_px = self.getPixel(LEFT_FOOT, self.front_landmarks, self.front_h, self.front_w)
        right_px = self.getPixel(RIGHT_FOOT, self.front_landmarks, self.front_h, self.front_w)
        
        middle_px = (
                int((left_px[0] + right_px[0]) / 2),
                int((left_px[1] + right_px[1]) / 2)
        )

        return middle_px
    
    # Ellipse circumference approximation using Ramanujan's second approximation: https://en.wikipedia.org/wiki/Perimeter_of_an_ellipse
    def getEllipseCircum(self, a, b):
        t = ((a-b) / (a+b))**2
        return pi*(a+b)*(1+3*t/(10 + sqrt(4-3*t))) 

    def getMeasurementScale (self):
        """
        Uses user height to get a scale for 
        Finds actual top-of-head pixel starting from noise
        Uses top-of-head pixel and midpoint pixel to get height, used for inches/pixel scale
        """

        # Get the two points we need for height cal
        mid_px = self.getMiddlePx()
        nose_px = self.getPixel(NOSE, self.front_landmarks, self.front_h, self.front_w)

        temp_px = self.getPointFromBackground(nose_px, self.front_segmented_image, direction='up')
        # Show the pixel found and draw a height line on the segemented image
        # cv2.circle(segmented_image, temp_px, 3, color=(0, 0, 0), thickness=-1)
        # cv2.line(segmented_image, mid_px, temp_px, (255,0,0), 2) 
        # print(f"Top Pixel found = {temp_px} with color {segmented_image[(temp_px)]}")

        pixel_height = abs(mid_px[1] - temp_px[1])
        # print(pixel_height)

        self.scale = self.user_height/pixel_height
        # print(self.scale)


    def getHipMeasurement(self):
        """
        Uses two images to get two axis of an ellipse for an accurate hip measurement.
        Starts with both hip points, and moves outward until it hits the background. Then calculates pixel
        distance from these two new points, for both front and side views. 
        Once both "axis" are calculated and converted to inches with scale, get ellipse approx to find final 
        hip distance     
        """
        # ----- Front Image Logic ------
        # Convert landmarks to real pixels we can use
        front_right_hip = self.getPixel(RIGHT_HIP, self.front_landmarks, self.front_h, self.front_w)
        front_left_hip = self.getPixel(LEFT_HIP, self.front_landmarks, self.front_h, self.front_w)

        front_right_hip_px = self.getPointFromBackground(front_right_hip, self.front_segmented_image, direction="right")
        front_left_hip_px = self.getPointFromBackground(front_left_hip, self.front_segmented_image, direction="left")

        # Calculate pixel distance between both front points
        front_view_hip_dist = np.linalg.norm(np.array(front_right_hip_px) - np.array(front_left_hip_px)) # Front view pixel distance
        # cv2.line(self.front_segmented_image, front_right_hip_px, front_left_hip_px, (255,0,0), 5) 

        # ----- Side Image Logic ------ (really the same as front)
        side_right_hip = self.getPixel(RIGHT_HIP, self.side_landmarks, self.side_h, self.side_w)
        side_left_hip = self.getPixel(LEFT_HIP, self.side_landmarks, self.side_h, self.side_w)

        side_right_hip = self.getPointFromBackground(side_right_hip, self.side_segmented_image, direction="right")
        # cv2.circle(self.side_segmented_image, side_right_hip, 20, color=(255,0,50), thickness=-1)

        side_left_hip = self.getPointFromBackground(side_left_hip, self.side_segmented_image, direction="left")
        # cv2.circle(self.side_segmented_image, side_left_hip, 20, color=(255,0,50), thickness=-1)

        # Calculate side view distance 
        side_view_hip_dist = np.linalg.norm(np.array(side_right_hip) - np.array(side_left_hip))

        # print(f"Front view hip distance calculation: {front_view_hip_dist}")
        # print(f"Side view hip distance calculation: {side_view_hip_dist}")

        # Convert to inches using calculated scale
        a = front_view_hip_dist * self.scale
        b = side_view_hip_dist * self.scale

        # convert distance to "axis" that we can use for ellipse approx
        a = a / 2
        b = b / 2
        return self.getEllipseCircum(a,b)

    def getShoulderMeasurements(self):
            
        # ----- Front Image Logic ------

        front_right_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks, self.front_h, self.front_w)
        front_left_shoulder = self.getPixel(LEFT_SHOULDER, self.front_landmarks, self.front_h, self.front_w)
        front_view_shoulder_dist = np.linalg.norm(np.array(front_right_shoulder) - np.array(front_left_shoulder)) # Front view pixel distance

        # ----- Side Image Logic ------
        side_shoulder_start = self.getPixel(LEFT_SHOULDER, self.side_landmarks, self.side_h, self.side_w)
        side_shoulder_end = self.getPointFromBackground(side_shoulder_start, self.side_segmented_image, direction="right")

        # cv2.circle(self.side_segmented_image, side_shoulder_end, 20, color=(255,0,50), thickness=-1)

        side_view_shoulder_dist = np.linalg.norm(np.array(side_shoulder_start) - np.array(side_shoulder_end)) # Front view pixel distance
        # cv2.line(self.side_segmented_image, side_shoulder_start, side_shoulder_end, (255,0,0), 5) 


        a = front_view_shoulder_dist * self.scale
        b = side_view_shoulder_dist * self.scale

        a = a / 2

        return self.getEllipseCircum(a,b)/2 # divide by 2 because shoulder width isn't measured all the way around like hip


    def getChestMeasurement(self):
        # there is no chest landmark, i can estimate by doing a double mid point between chest and waist
       
        def getPointsFromDistance(p1, p2, amount=1):
            # amount is the amount of the distance to apply to the point
            x_dist = (p2[0]-p1[0]) * amount
            new_x = int(p1[0] + x_dist)

            y_dist = (p2[1]-p1[1]) * amount
            new_y = int(p1[1] + y_dist)

            return (new_x,new_y)

        # ---- Front Logic ------
        fr_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks, self.front_h, self.front_w)
        fl_shoulder = self.getPixel(LEFT_SHOULDER,self.front_landmarks, self.front_h, self.front_w)

        fr_hip = self.getPixel(RIGHT_HIP, self.front_landmarks, self.front_h, self.front_w)
        fl_hip = self.getPixel(LEFT_HIP, self.front_landmarks, self.front_h, self.front_w)

        # cv2.line(self.front_segmented_image, fr_shoulder, fr_hip, (255,0,0), 5) 
        
        fr_chest = getPointsFromDistance(fr_shoulder,fr_hip,.3) # I'm using ~30% for a general rule of thumb
        # cv2.circle(self.front_segmented_image, fr_chest, 15, color=(255,0,50), thickness=-1)
        fl_chest = getPointsFromDistance(fl_shoulder,fl_hip,.3) 
        # cv2.circle(self.front_segmented_image, fl_chest, 15, color=(255,0,50), thickness=-1)

        front_dist = np.linalg.norm(np.array(fr_chest) - np.array(fl_chest)) 

        # ---- SIDE LOGIC -----
        side_shoulder = self.getPixel(RIGHT_SHOULDER, self.side_landmarks, self.side_h, self.side_w)
        side_hip = self.getPixel(RIGHT_HIP, self.side_landmarks, self.side_h, self.side_w)
        cv2.line(self.side_segmented_image, side_shoulder, side_hip, (255,0,0), 5)

        mid_chest = getPointsFromDistance(side_shoulder, side_hip, .3)
        cv2.circle(self.side_segmented_image, mid_chest, 15, color=(255,0,50), thickness=-1)



    def getMeasurements(self):

        self.getMeasurementScale()

        # Chest / Bust
        chest_measurement = self.getChestMeasurement()

        # Shoulder to Hip (length for shirts)

        # sleeve length (long)

        #sleeve length (short)

        #shoulders
        shoulder_measurement = self.getShoulderMeasurements()

        # Waist

        # Hip 
        hip_measurment = self.getHipMeasurement()
        # print(f"Hip Size (inches):{hip_measurment:.2f}")

        # Hip to inseam

        #Inseam to floor (pant length)

        # Hip to floor (not usually used for pants but why not)

        self.saveToCSV(hip_measurment, shoulder_measurement)