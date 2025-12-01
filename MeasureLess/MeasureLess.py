import numpy as np
import cv2 as cv
import logging
import json
import os
import sys

from modules import ImageHandler, PoseLandmarkHandler, SegmentationHandler, MeasurementHandler
# from modules.CLArgsHandler import measureLessArgs # Currently not working

# TODO: Update logic to accept and process 2 images at once. One side profile, one front profile
# TODO: Update to accept either image directories or bytestreams, to ensure command line isn't broken
class MeasureLess:
    def __init__(self, frontImage, sideImage, userHeight, bodyType=None, detectionMode = 3, segmentationTightness = 0.5, debug=False):
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
        print("Running the pipeline for measureless")
        # Will be utilized for ImageHandler to determine if the passed through images are
        # either directories or bytestreams
        isByteStream = False
        # Error checking
        # Check if byte streams or if file directories
        if (isinstance(self.fImg, bytes) and isinstance(self.sImg, bytes)):
            # Check if the bytestreams passed through are actually images
            npArrayFront = np.frombuffer(self.fImg, np.uint8)
            npArraySide = np.frombuffer(self.sImg, np.uint8)
            
            imgFront = cv.imdecode(npArrayFront, cv.IMREAD_COLOR)
            imgSide = cv.imdecode(npArraySide, cv.IMREAD_COLOR)

            if imgFront is None or imgSide is None:
                raise ValueError("Image could not be decoded from bytes.")

            try:
                cv.imwrite("results/frontOutput.png", imgFront)
                cv.imwrite("results/sideOutput.png", imgSide)
                isByteStream = True
            except Exception as e:
                return "There was an error: {e}"
        elif(isinstance(self.fImg, str) and isinstance(self.sImg, str)):
            # Check if images exist, this will only run if
            # Change to try blocks?
            if not (os.path.isfile(self.fImg)):
                raise ValueError(f"{self.fImg} is not a valid image directory. Ensure image is located in /MeasureLess")
            if not (os.path.isfile(self.sImg)):
                raise ValueError(f"{self.sImg} is not a valid image directory. Ensure image is located in /MeasureLess")
                
            isByteStream = False
        else:
            raise ValueError(f"{self.fImg} or {self.sImg} are not valid images")
            


        # Tightness now has a default value of 0.5
        # Updated to handle bytestreams and image directories
        imageHandler = ImageHandler.ImageHandler(self.fImg, self.sImg, isByteStream=isByteStream, debug=self.debug)
            
        # Assumes that fileNames are handled on passthrough
        imageHandler.loadImages()
            
        # Creating landmark handler object using provided data
        landmarkHandler = PoseLandmarkHandler.PoseLandmarkHandler(imageHandler, debug=self.debug)
        
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
        segmentationHandler = SegmentationHandler.SegmentationHandler(imageHandler, self.debug)
        segmentationHandler.segmentImage()

        # Measurements from calculated images, in inches
        # height has to be casted to an integer
        measurementHandler = MeasurementHandler.MeasurementHandler(imageHandler, user_height=int(self.height), debug=self.debug)
        results = measurementHandler.getMeasurements()

        # Saving processed images
        if (self.debug):
            imageHandler.saveResults()

        if not results:
            raise ValueError(f"There was an error with the dictionary. {results}")

        return results
        
        # try:
        #     with open('results/results.json', 'r') as f:
        #         return json.load(f)
        # except Exception as e:
        #     return f"There was an error opening the json: {e}"