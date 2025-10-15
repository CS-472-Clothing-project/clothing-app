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
            
        # Saving passed ImageHandler object
        self.imageHandler = imageHandler
        self.detector = None
        self.annotedImage = None
        self.processedImage = None
        
    def loadDetector(self):
        baseOptions = python.BaseOptions(model_asset_path=self.landmarkerPath)
        options = vision.PoseLandmarkerOptions(
            base_options=baseOptions,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)
        
    def detectImage(self):
        self.processedImage = self.detector.detect(self.imageHandler.mpImage)
        
    def drawLandmarks(self):
        landmarksList = self.processedImage.pose_landmarks
        
        print("Copying image...")
        self.annotedImage = np.copy(self.imageHandler.ndArrayImage)
        
        print("Entering The LOOP...")
        # The LOOP
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
        return self.annotedImage
        
    def hasDetector(self):
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