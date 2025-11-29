import numpy as np
import cv2 as cv
import logging
import json

from modules import ImageHandler, PoseLandmarkHandler, SegmentationHandler, MeasurementHandler
# from modules.CLArgsHandler import measureLessArgs # Currently not working

# TODO: Update logic to accept and process 2 images at once. One side profile, one front profile
# TODO: Update to convert main function into a class
class MeasureLess:
    def __init__(self, frontImage, sideImage, userHeight, bodyType, detectionMode = 2, segmentationTightness = 0.5, debug=True):
        # Initialize the variables that will be needed for MeasureLess' pipeline
        # Image are passed through as byte
        self.fImg = frontImage
        self.sImg = sideImage
        self.height = userHeight
        self.bType = bodyType
        # Leftover from previous code, will probably be removed
        self.dM = detectionMode
        self.sT = segmentationTightness
        self.debug = debug
    def runMeasureLess(self):
        print("Run the pipeline for measureless")

        # Error checking
        
        # Incorporate Matt's code
        npArrayFront = np.frombuffer(self.fImg, np.uint8)
        npArraySide = np.frombuffer(self.sImg, np.uint8)

        # Read in the images now
        frontImage = cv.imdecode(npArrayFront, cv.IMREAD_COLOR)
        sideImage = cv.imdecode(npArraySide, cv.IMREAD_COLOR)
        

        # Tightness now has a default value of 0.5
        imageHandler = ImageHandler.ImageHandler(frontImage, sideImage)
            
        # Assumes that fileNames are handled on passthrough
        imageHandler.loadImages()
            
        # Creating landmark handler object using provided data
        landmarkHandler = PoseLandmarkHandler.PoseLandmarkHandler(imageHandler)
        
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
        if (self.debug):
            imageHandler.saveResults()

        try:
            with open('results/results.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            return f"There was an error opening the json: {e}"