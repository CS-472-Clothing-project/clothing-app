import numpy as np
import logging
import mediapipe as mp
import cv2
import pandas as pd
import json
import os
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
    def __init__(self, imageHandler,user_height, debug=False):
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
    
    def saveToJSON(self, measurements):
        # Check if directory exists
        print("Saving measurements to 'results/results.json'")
        os.makedirs("results", exist_ok=True)
        with open('results/results.json', 'w') as file:
            json.dump(measurements, file, indent=4)
        return
    
    # Translate normalized landmark to pixel coordinates CV2 can use
    def getPixel(self, index, landmarks):

        if landmarks == self.front_landmarks:
            image_w = self.front_w
            image_h = self.front_h
        else:
            image_w = self.side_w
            image_h = self.side_h

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
        bg_color = self.imageHandler.backgroundColor.copy()

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
        """
        Args:
            point: starting point
            segmented_image: which segmented image
            direction: which way to go
        """
        x,y = point

        if direction == "right":
            for x_pixel in range(x, segmented_image.shape[1]-3, 1):
                temp = (x_pixel, y)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp

        elif direction == "left":
            for x_pixel in range(x, 3, -1):
                temp = (x_pixel, y)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp

        elif direction == "up":
            for y_pixel in range(y, 3, -1):
                temp = (x, y_pixel)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp

        elif direction == "down":
            for y_pixel in range(y, segmented_image.shape[0]-3, 1):
                temp = (x, y_pixel)
                if self.checkBackground(temp, segmented_image, direction):
                    return temp

    # Find the middle pixel between both feet for a better height measurement
    def getMiddlePx(self, p1, p2):
        
        middle_px = (
                int((p1[0] + p2[0]) / 2),
                int((p1[1] + p2[1]) / 2)
        )

        return middle_px
    
    def getPointFromDistance(self, p1, p2, amount=1):
        # amount is the amount of the distance to apply to the point
        x_dist = (p2[0]-p1[0]) * amount
        new_x = int(p1[0] + x_dist)

        y_dist = (p2[1]-p1[1]) * amount
        new_y = int(p1[1] + y_dist)

        return (new_x,new_y)

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
        front_left_foot = self.getPixel(LEFT_FOOT, self.front_landmarks)
        front_right_foot = self.getPixel(RIGHT_FOOT, self.front_landmarks)
        mid_px = self.getMiddlePx(front_left_foot, front_right_foot)
        nose_px = self.getPixel(NOSE, self.front_landmarks)

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
        front_right_hip_px = self.getPixel(LEFT_HIP, self.front_landmarks)
        front_left_hip_px = self.getPixel(LEFT_HIP, self.front_landmarks)

        # front_right_hip_px = self.getPointFromBackground(front_right_hip, self.front_segmented_image, direction="right")
        # front_left_hip_px = self.getPointFromBackground(front_left_hip, self.front_segmented_image, direction="left")

        # Calculate pixel distance between both front points
        front_view_hip_dist = np.linalg.norm(np.array(front_right_hip_px) - np.array(front_left_hip_px)) # Front view pixel distance
        # cv2.line(self.front_segmented_image, front_right_hip_px, front_left_hip_px, (255,0,0), 5) 

        # ----- Side Image Logic ------ (really the same as front)
        side_right_hip = self.getPixel(RIGHT_HIP, self.side_landmarks)
        side_left_hip = self.getPixel(LEFT_HIP, self.side_landmarks)

        side_right_hip = self.getPointFromBackground(side_right_hip, self.side_segmented_image, direction="right")
        # cv2.circle(self.side_segmented_image, side_right_hip, 20, color=(255,0,50), thickness=-1)

        side_left_hip = self.getPointFromBackground(side_left_hip, self.side_segmented_image, direction="left")
        # cv2.circle(self.side_segmented_image, side_left_hip, 20, color=(255,0,50), thickness=-1)

        # cv2.line(self.side_segmented_image, side_right_hip, side_left_hip, (255,0,0), 5) 

        # Calculate side view distance 
        side_view_hip_dist = np.linalg.norm(np.array(side_right_hip) - np.array(side_left_hip))

        # print(f"Front view hip distance calculation: {front_view_hip_dist}")
        # print(f"Side view hip distance calculation: {side_view_hip_dist}")

        # ----- Ellipse logic -----
        # Convert to inches using calculated scale
        a = front_view_hip_dist * self.scale
        b = side_view_hip_dist * self.scale

        # convert distance to "axis" that we can use for ellipse approx
        a = a / 2
        b = b / 2
        return self.getEllipseCircum(a,b)

    def getShoulderMeasurements(self):
            
        # ----- Front Image Logic ------

        front_right_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks)
        front_left_shoulder = self.getPixel(LEFT_SHOULDER, self.front_landmarks)
        front_view_shoulder_dist = np.linalg.norm(np.array(front_right_shoulder) - np.array(front_left_shoulder)) # Front view pixel distance

        # ----- Side Image Logic ------
        side_shoulder_start = self.getPixel(LEFT_SHOULDER, self.side_landmarks)
        side_shoulder_end = self.getPointFromBackground(side_shoulder_start, self.side_segmented_image, direction="right")

        # cv2.circle(self.side_segmented_image, side_shoulder_end, 20, color=(255,0,50), thickness=-1)

        side_view_shoulder_dist = np.linalg.norm(np.array(side_shoulder_start) - np.array(side_shoulder_end)) # Front view pixel distance
        # cv2.line(self.side_segmented_image, side_shoulder_start, side_shoulder_end, (255,0,0), 5) 

        # ----- Ellipse logic -----
        a = front_view_shoulder_dist * self.scale
        b = side_view_shoulder_dist * self.scale

        a = a / 2

        return self.getEllipseCircum(a,b)/2 # divide by 2 because shoulder width isn't measured all the way around like hip

    def getChestMeasurement(self):
        # there is no chest landmark, we can estimate by doing a double mid point between chest and waist
       
        # ---- Front Logic ------
        front_right_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks)
        front_left_shoulder = self.getPixel(LEFT_SHOULDER,self.front_landmarks)

        front_right_hip = self.getPixel(RIGHT_HIP, self.front_landmarks)
        front_left_hip = self.getPixel(LEFT_HIP, self.front_landmarks)

        # cv2.line(self.front_segmented_image, front_right_shoulder, front_right_hip, (255,0,0), 5) 
        
        fr_chest = self.getPointFromDistance(front_right_shoulder,front_right_hip,.3) # I'm using ~30% for a general rule of thumb
        # cv2.circle(self.front_segmented_image, fr_chest, 15, color=(255,0,50), thickness=-1)
        fl_chest = self.getPointFromDistance(front_left_shoulder,front_left_hip,.3) 
        # cv2.circle(self.front_segmented_image, fl_chest, 15, color=(255,255,50), thickness=-1)

        # fr_chest = self.getPointFromBackground(fr_chest, self.front_segmented_image, "left")
        # fl_chest = self.getPointFromBackground(fl_chest, self.front_segmented_image, "right")
        # cv2.circle(self.front_segmented_image, fr_chest, 15, color=(255,0,50), thickness=-1)
        # cv2.circle(self.front_segmented_image, fl_chest, 15, color=(255,255,50), thickness=-1)

        front_dist = np.linalg.norm(np.array(fr_chest) - np.array(fl_chest)) 

        # ---- SIDE LOGIC -----
        side_shoulder = self.getPixel(LEFT_SHOULDER, self.side_landmarks)
        side_hip = self.getPixel(LEFT_HIP, self.side_landmarks)
        # cv2.line(self.side_segmented_image, side_shoulder, side_hip, (255,0,0), 5)

        side_mid_chest = self.getPointFromDistance(side_shoulder, side_hip, .4)
        # cv2.circle(self.side_segmented_image, side_mid_chest, 20, color=(255,0,50), thickness=-1)

        side_right_chest = self.getPointFromBackground(side_mid_chest, self.side_segmented_image, "right")
        # cv2.circle(self.side_segmented_image, side_right_chest, 20, color=(255,0,50), thickness=-1)


        side_left_chest = self.getPointFromBackground(side_mid_chest, self.side_segmented_image, "left")
        # cv2.circle(self.side_segmented_image, side_left_chest, 20, color=(50,0,255), thickness=-1)

        side_dist = np.linalg.norm(np.array(side_right_chest) - np.array(side_left_chest))

        # Ellipse logic
        a = side_dist * self.scale
        b = front_dist * self.scale

        a = a/2
        b = b/2

        return self.getEllipseCircum(a,b)
        
    def getChestLength(self):
        # --- Front logic ----
        front_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks)
        front_hip = self.getPixel(RIGHT_HIP, self.front_landmarks)

        front_dist = np.linalg.norm(np.array(front_hip) - np.array(front_shoulder))

        # ----- Side Logic -----
        side_hip = self.getPixel(RIGHT_HIP, self.side_landmarks)
        side_hip_left = self.getPointFromBackground(side_hip, self.side_segmented_image, "left")
        # cv2.circle(self.side_segmented_image, side_hip_left, 20, color=(50,0,255), thickness=-1)
        side_hip_right = self.getPointFromBackground(side_hip, self.side_segmented_image, "right")
        # cv2.circle(self.side_segmented_image, side_hip_right, 20, color=(50,0,255), thickness=-1)

        side_dist = np.linalg.norm(np.array(side_hip_right) - np.array(side_hip_left))

        # Ellipse logic

        a = front_dist * self.scale
        b = side_dist * self.scale

        a = a/2
        b = b/2

        return self.getEllipseCircum(a,b) / 2
        # return front_dist * self.scale

    def getShortSleeve(self):
        # ---- Front Logic -----
        front_right_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks)
        front_right_elbow = self.getPixel(RIGHT_ELBOW, self.front_landmarks)

        front_sleeve = self.getPointFromDistance(front_right_shoulder, front_right_elbow, .6)
        # cv2.circle(self.front_segmented_image, front_sleeve, 20, color=(255,0,50), thickness=-1)
        # cv2.circle(self.side_segmented_image, side_shoulder_end, 20, color=(255,0,50), thickness=-1)
        front_dist = np.linalg.norm(np.array(front_sleeve) - np.array(front_right_shoulder))

        # ---- Side logic -----
        side_right_shoulder = self.getPixel(RIGHT_SHOULDER, self.side_landmarks)
        side_right_elbow = self.getPixel(RIGHT_ELBOW, self.side_landmarks)

        side_sleeve = self.getPointFromDistance(side_right_shoulder, side_right_elbow, .6)
        # cv2.circle(self.side_segmented_image, side_sleeve, 20, color=(255,0,50), thickness=-1)

        side_sleeve_up = self.getPointFromBackground(side_sleeve, self.side_segmented_image, "up")
        side_sleeve_down = self.getPointFromBackground(side_sleeve, self.side_segmented_image, "down")

        side_dist = np.linalg.norm(np.array(side_sleeve_down) - np.array(side_sleeve_down))

        # Ellipse Logic

        a = front_dist * self.scale
        b = side_dist * self.scale

        a = a/2
        b = b/2

        return self.getEllipseCircum(a,b) / 2
 
    def getLongSleeve(self):
        # ---- Front Logic -----
        front_right_elbow = self.getPixel(RIGHT_ELBOW, self.front_landmarks)
        front_elbow_left = self.getPointFromBackground(front_right_elbow, self.front_segmented_image, "left")
        front_elbow_right = self.getPointFromBackground(front_right_elbow, self.front_segmented_image, "right")

        # cv2.line(self.front_segmented_image, front_right_shoulder, front_right_hip, (255,0,0), 5) 

        # cv2.line(self.front_segmented_image, front_elbow_left, front_elbow_right, (255,0,50), 5)
        front_dist = np.linalg.norm(np.array(front_elbow_left) - np.array(front_elbow_right))

        # ---- Side Logic -----
        side_left_shoulder = self.getPixel(LEFT_SHOULDER, self.side_landmarks)
        side_left_wrist = self.getPixel(LEFT_WRIST, self.side_landmarks)

        side_dist = np.linalg.norm(np.array(side_left_wrist) - np.array(side_left_shoulder))

        # Ellipse Logic
        a = front_dist * self.scale
        b = side_dist * self.scale

        a = a/2
        b = b/2

        return self.getEllipseCircum(a,b) / 2
        
    def getWaistMeasurement(self):
        # ---- Front logic ----
        front_right_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks)
        front_left_shoulder = self.getPixel(LEFT_SHOULDER, self.front_landmarks)
        front_right_hip = self.getPixel(RIGHT_HIP, self.front_landmarks)
        front_left_hip = self.getPixel(LEFT_HIP, self.front_landmarks)

        front_right_waist = self.getPointFromDistance(front_right_shoulder, front_right_hip, .65)
        front_left_waist = self.getPointFromDistance(front_left_shoulder, front_left_hip, .65)

        # cv2.line(self.front_segmented_image, front_right_shoulder, front_right_hip, color=(0,0,255))
      
        # front_right_waist = self.getPointFromBackground(front_right_waist, self.front_segmented_image, "left")
        # front_left_waist = self.getPointFromBackground(front_left_waist, self.front_segmented_image, "right")
        # cv2.circle(self.front_segmented_image, front_right_waist, 20, color=(255,0,50), thickness=-1)
        # cv2.circle(self.front_segmented_image, front_left_waist, 20, color=(255,0,255), thickness=-1)

        front_dist = np.linalg.norm(np.array(front_right_waist) - np.array(front_left_waist))

        # ----- Side Logic -----
        side_shoulder = self.getPixel(LEFT_SHOULDER, self.side_landmarks)
        side_hip = self.getPixel(LEFT_HIP, self.side_landmarks)
        side_waist = self.getPointFromDistance(side_shoulder, side_hip, .65)
        side_right_waist = self.getPointFromBackground(side_waist, self.side_segmented_image, "right")
        side_left_waist = self.getPointFromBackground(side_waist, self.side_segmented_image, "left")

        # cv2.circle(self.side_segmented_image, side_right_waist, 30, color=(25,0,25), thickness=-1)
        # cv2.circle(self.side_segmented_image, side_left_waist, 30, color=(100,0,100), thickness=-1)

        side_dist = np.linalg.norm(np.array(side_right_waist) - np.array(side_left_waist))

        # -- Ellipse logic --
        a = front_dist * self.scale
        b = side_dist * self.scale

        a = a/2
        b = b/2
        return self.getEllipseCircum(a,b)

    def getInseamMeasurement(self):
        front_right_hip = self.getPixel(RIGHT_HIP, self.front_landmarks)
        front_right_ankle = self.getPixel(RIGHT_ANKLE, self.front_landmarks)

        front_dist = np.linalg.norm(np.array(front_right_ankle) - np.array(front_right_hip))

        side_knee = self.getPixel(LEFT_KNEE, self.side_landmarks)
        right_side_knee = self.getPointFromBackground(side_knee, self.side_segmented_image, "right")
        left_side_knee = self.getPointFromBackground(side_knee, self.side_segmented_image, "left")

        side_dist = np.linalg.norm(np.array(right_side_knee) - np.array(left_side_knee))

        # -- Ellipse logic --
        a = front_dist * self.scale
        b = side_dist * self.scale

        a = a/2
        b = b/2

        return self.getEllipseCircum(a,b) / 2

    def getOutseamMeasurement(self):
        front_right_shoulder = self.getPixel(RIGHT_SHOULDER, self.front_landmarks)
        front_right_hip = self.getPixel(RIGHT_HIP, self.front_landmarks)
        front_right_waist = self.getPointFromDistance(front_right_shoulder, front_right_hip, .65)
        # front_right_waist = self.getPointFromBackground(front_right_waist, self.front_segmented_image, "left")
        # cv2.circle(self.front_segmented_image, front_right_waist, 30, color=(100,0,100), thickness=-1)

        front_right_ankle = self.getPixel(RIGHT_FOOT, self.front_landmarks)

        front_dist = np.linalg.norm(np.array(front_right_waist) - np.array(front_right_ankle))

        side_knee = self.getPixel(LEFT_KNEE, self.side_landmarks)
        right_side_knee = self.getPointFromBackground(side_knee, self.side_segmented_image, "right")
        left_side_knee = self.getPointFromBackground(side_knee, self.side_segmented_image, "left")

        side_dist = np.linalg.norm(np.array(right_side_knee) - np.array(left_side_knee))

        # -- Ellipse logic --
        a = front_dist * self.scale
        b = side_dist * self.scale

        a = a/2
        b = b/2
        return self.getEllipseCircum(a,b) / 2
        # return front_dist * self.scale

    def getMeasurements(self):

        self.getMeasurementScale()

        # Chest / Bust
        chest_measurement = round(self.getChestMeasurement(),2)

        # Shoulder to Hip (length for shirts)
        chest_length = round(self.getChestLength(),2)

        # sleeve length (long)
        long_sleeve_measurement = round(self.getLongSleeve(),2)
        #sleeve length (short)
        short_sleeve_measurement = round(self.getShortSleeve(),2)
        #shoulders
        shoulder_measurement = round(self.getShoulderMeasurements(),2)
        # Waist
        waist_measurement = round(self.getWaistMeasurement(),2)
        # Hip 
        hip_measurement = round(self.getHipMeasurement(),2)
        #Inseam 
        inseam_measurement = round(self.getInseamMeasurement(),2)
        #Outseam
        outseam_measurement = round(self.getOutseamMeasurement(),2)

        measurements = {
            "chest": chest_measurement,
            "length": chest_length,
            "long_sleeve": long_sleeve_measurement,
            "short_sleeve": short_sleeve_measurement,
            "shoulder":shoulder_measurement,
            "waist": waist_measurement,
            "hip": hip_measurement,
            "inseam": inseam_measurement,
            "outseam": outseam_measurement
        }
        # Update to return dictionary will be changed to json
        if(self.debug):
            self.saveToJSON(measurements)
        return measurements