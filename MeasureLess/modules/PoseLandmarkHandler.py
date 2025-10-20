import numpy as np
import mediapipe as mp
import logging
import cv2

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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
        self.annotedImage = None # Don't need
        self.processedImage = None # Don't need
        
    # This needs to be called once
    def loadDetector(self):
        # Setting the options for the pose landmarker and loading the detector
        baseOptions = python.BaseOptions(model_asset_path=self.landmarkerPath)
        options = vision.PoseLandmarkerOptions(
            base_options=baseOptions,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)
        
    # This needs to be called once
    def detectImage(self):
        # Runs the detection method and returns the processed image
        for i in range(len(self.imageHandler.detectedImage)):
            self.imageHandler.detectedImage[i] = self.detector.detect(self.imageHandler.mpImage[i])
        
    # This needs to be called twice
    def drawLandmarks(self, detectedImage, ndArrayImage) -> np.ndarray:
        landmarksList = detectedImage.pose_landmarks
        
        print("Copying image...")
        annotedImage = np.copy(ndArrayImage)
        
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
                annotedImage,
                landmarksProto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())
        
        print("Drawing complete. Retuning annotated image.")
        # Not strictly necessary to return the image, but it might prove useful later
        return annotedImage
        
    def hasDetector(self) -> bool:
        if not self.detector:
            return False
        else:
            return True
        
    # This should probably go in the imageHandler
    # def saveImage(self):
    #     print("Saving image...")
    #     try:
    #         cv2.imwrite("results/landmarked-image.png", self.annotedImage)
    #     except:
    #         logging.exception("Error while saving image: ")
    #     print("Image saved to results as landmarked-image.png")
        
    # Placeholder for future functionality
    def displayImage(self):
        pass
    
    # Function to pass the resultant image to the image handler
    # def storeImage(self):
    #     self.imageHandler.annotatedImage = np.copy(self.annotedImage)