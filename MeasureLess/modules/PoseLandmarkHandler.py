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
RIGHT_FOOT = 32

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
        

    def getMeasurements(self, user_height = None):
        world_landmarks = self.processedImage.pose_world_landmarks[0] # currently working for one "pose" object at a time

        def dist(a,b):
            distanceArr =  np.linalg.norm(np.array(
                [
                world_landmarks[a].x - world_landmarks[b].x,
                world_landmarks[a].y - world_landmarks[b].y,
                world_landmarks[a].z - world_landmarks[b].z,
                ]
             ))
            
            return distanceArr*1000

        body_height = dist(NOSE, RIGHT_FOOT)
        scale = 1.0
        if user_height:
            scale = user_height / body_height
        
        return {
            "height_mm" : body_height * scale,
            "scale_factor" : scale ,
        }
    
    # Placeholder for future functionality
    def displayImage(self):
        pass