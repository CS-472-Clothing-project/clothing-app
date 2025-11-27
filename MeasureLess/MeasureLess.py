from modules import ImageHandler
from modules import PoseLandmarkHandler
from modules import SegmentationHandler
from modules import MeasurementHandler
from modules.CLArgsHandler import measureLessArgs

import logging
import os
import sys

# TODO: Update logic to accept and process 2 images at once. One side profile, one front profile
# TODO: Convert MeasureLess.py to be a class and maintain its function, 
#       hardcode values, and figure out how images will be passed through
#       Potentially get rid of debug
class MeasureLess:
    def __init__(self, images, userHeight, detectionMode = 2, segmentationTightness = 0.5):
        # Initialize the variables that will be needed for MeasureLess' pipeline
        # Not sure how images will be passed through, will be changed
        self.images = images
        self.userHeight = userHeight
        self.detectionMode = detectionMode
        self.segmentationTightness = segmentationTightness
        
    # Write a funciton that will essentially run the pipeline for MeasureLess
    def runMeasureLess(self):
        acceptedImgTypes = [".jpg", ".jpeg", ".png", ".bmp"]
        

        # Will have to be updated to a cleaner look
        # if not(os.path.splitext(args.fImg)[1] in acceptedImgTypes and os.path.splitext(args.sImg)[1] in acceptedImgTypes):
        #     print(f"Unsupported file type detected. {args.fImg} or {args.sImg}.")
        #     sys.exit(0)
        
        # Tightness now has a default value of 0.5
        imageHandler = ImageHandler.ImageHandler(self.images, float(self.segmentationTightness))
            
        # Assumes that fileNames are handled on passthrough
        imageHandler.loadImages(self.images)
            
        # Creating landmark handler object using provided data
        landmarkHandler = PoseLandmarkHandler.PoseLandmarkHandler(imageHandler, self.detectionMode)
        
        # Try loading detector module
        print("Loading Detector...")
        try:
            landmarkHandler.loadDetector()
        except:
            logging.exception("And error occurred when loading the detector: ")
            
        # On success, uses loaded detector to process the image (generating landmarks)
        print("Detector loaded. Running image detection...")
        try:
            landmarkHandler.detectImage()
        except:
            logging.exception("Error when detecting image: ")
            
        # Drawing landmarks onto image using landmarks generated above
        print("\nLandmarks processed. Drawing landmarks on image: ")
        try:
            for i in range(len(imageHandler.annotatedImage)):
                imageHandler.annotatedImage[i] = landmarkHandler.drawLandmarks(imageHandler.detectedImage[i],
                                                                            imageHandler.ndArrayImage[i])
        except:
            logging.exception("Error while drawing landmarks: ")

        # Creating segmentationHandler object, processing image, and saving the result
        segmentationHandler = SegmentationHandler.SegmentationHandler(imageHandler)
        segmentationHandler.segmentImage()

        # Measurements from calculated images, in inches
        measurementHandler = MeasurementHandler.MeasurementHandler(imageHandler, user_height=self.userHeight)
        measurementHandler.getMeasurements()

        # Saving processed images
        imageHandler.saveResults()
