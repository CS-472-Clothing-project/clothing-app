import numpy as np
import mediapipe as mp
import logging
import cv2

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Considering rolling this into another class. Might be more effective
# to just inherit this or make it a member of the image handler.

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


class PoseLandmarkHandler:
    def __init__(self, imageHandler, landmarkerMode=2):
        # Set the model path
        if landmarkerMode == 1:
            self.landmarkerPath = 'models/pose_landmarker_lite.task'
        elif landmarkerMode == 2:
            self.landmarkerPath = 'models/pose_landmarker_full.task'
        elif landmarkerMode == 3:
            self.landmarkerPath = 'models/pose_landmarker_heavy.task'
        else:
            print("Invalid model selected")
            
        # Saving passed ImageHandler object and initializing instance members
        self.imageHandler = imageHandler
        self.detector = None
        self.annotedImage = None
        self.processedImage = None
        
    def loadDetector(self):
        # Setting the options for the pose landmarker and loading the detector
        baseOptions = python.BaseOptions(model_asset_path=self.landmarkerPath)
        options = vision.PoseLandmarkerOptions(
            base_options=baseOptions,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)
        
    def detectImage(self):
        # Runs the detection method and returns the processed image
        self.processedImage = self.detector.detect(self.imageHandler.mpImage)
        
    def drawLandmarks(self) -> np.ndarray:
        landmarksList = self.processedImage.pose_landmarks
        
        print("Copying image...")
        self.annotedImage = np.copy(self.imageHandler.ndArrayImage)
        
        print("Entering The LOOP...")
        # Iterating over all landmarks found by the detector
        for i in range(len(landmarksList)):
            poseLandmarks = landmarksList[i]
            
            # Draw the landmarks
            landmarksProto = landmark_pb2.NormalizedLandmarkList()
            
            # NOTE: This might *pose* a problem when using the height to calculate the lengths between 
            # points. We will need to take this into account when drawing up an algorithm as we
            # will need to normalize the same way
            landmarksProto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in poseLandmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                self.annotedImage,
                landmarksProto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
        
        print("Drawing complete. Retuning annotated image: ")
        # Not strictly necessary to return the image, but it might prove useful later
        return self.annotedImage
        
    def hasDetector(self) -> bool:
        if not self.detector:
            return False
        else:
            return True
        
    def saveImage(self):
        print("Saving image...")
        try:
            cv2.imwrite("results/landmarked-image.png", self.annotedImage)
        except:
            logging.exception("Error while saving image: ")
        print("Image saved to results as landmarked-image.png")
        
    # def draw_height_line(self, a, b):
    #     landmarks = self.processedImage.pose_landmarks[0] # currently working for one "pose" object at a time

    #     h,w,_ = self.annotedImage.shape
    #     x1 = int(landmarks[a].x * w)
    #     x2 = int(landmarks[b].x * w)
    #     y1 = int(landmarks[a].y * h)
    #     y2 = int(landmarks[b].y * h)

    #     cv2.line(self.annotedImage, (x1,y1), (x2,y2), (255,0,0), 5)
        
    def getMeasurements(self, user_height = None):
        """
            Catch all function currently used to calculated and return pixels needed for 
            measurement calculation. Probably needs to be moved in later iterations but 
            for now is just used to get values from PoseLandmarkHandler.py to 
            SegmentationHandler.py throught Measureless.PY
        """
        
        if not self.processedImage.pose_world_landmarks:
            print("No pose landmarks detected int this image.")
            return None
        
        landmarks = self.processedImage.pose_landmarks[0] # currently working for one "pose" object at a time
        h,w,_ = self.annotedImage.shape
        
        #  Helper function to convert our coord into values cv2 can use
        def getPixel(index):
            x_coor = int(landmarks[index].x * w)
            y_coor = int(landmarks[index].y * h)
            return(x_coor,y_coor)
        
        # get both feet for an average middle pixel that can be used for hieght
        left_pixel = getPixel(LEFT_FOOT)
        right_pixel = getPixel(RIGHT_FOOT)
        middle_pixel = (int((left_pixel[0] + right_pixel[0]) / 2), int((right_pixel[1] + left_pixel[1]) / 2))

        # draw middle "base" pixel
        cv2.circle(self.annotedImage, middle_pixel, 3, color = (0, 255, 0), thickness=-1)

        # draw hieghest pixel we have for "top" pixel
        nose_pixel = getPixel(NOSE)
        cv2.line(self.annotedImage, nose_pixel, middle_pixel, (255,0,0), 5)

        # print("Mid-point printed\n")

        
        return middle_pixel, nose_pixel
    
    # Placeholder for future functionality
    def displayImage(self):
        pass