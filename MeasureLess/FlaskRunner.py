import numpy as np
import cv2
from modules import ImageHandler, PoseLandmarkHandler, SegmentationHandler, MeasurementHandler
import logging
import json


def run_from_flask(frontImage, sideImage, height, bodyType):
    print("Run function received images")
    npArrayFront = np.frombuffer(frontImage, np.uint8)
    npArraySide = np.frombuffer(sideImage, np.uint8)
    
    imgFront = cv2.imdecode(npArrayFront, cv2.IMREAD_COLOR)
    imgSide = cv2.imdecode(npArraySide, cv2.IMREAD_COLOR)

    
    try:
        cv2.imwrite("results/frontOutput.png", imgFront)
        cv2.imwrite("results/sideOutput.png", imgSide)
    except Exception as e:
        return "There was an error: {e}"
    
    imageHandler = ImageHandler.ImageHandler(frontImage, sideImage)
    
    imageHandler.loadImages()
    
    # Creating landmark handler object using provided data
    landmarkHandler = PoseLandmarkHandler.PoseLandmarkHandler(imageHandler)
    
    # Try loading detector module
    print("Loading Detector...")
    try:
        landmarkHandler.loadDetector()
    except:
        logging.exception("An error occurred when loading the detector: ")
        
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
    
    # Saving processed images
    imageHandler.saveResults()
    
    # Measurements from calculated images, in inches
    measurementHandler = MeasurementHandler.MeasurementHandler(imageHandler, int(height))
    measurementHandler.getMeasurements()
    
    # Saving processed images
    # imageHandler.saveResults()
    
    try:
        with open('results/results.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        return f"There was an error opening the json: {e}"