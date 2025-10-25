from modules import ImageHandler
from modules import PoseLandmarkHandler
from modules import SegmentationHandler

import cv2
import logging

def main():
    # Short intro message for development
    print("Welcome to MeasureLess, the measure-less app for tailoring.")
    
    # Creating the image object by calling the import handler
    # fileName = input("Input name of the image file (with extension): ")
    # detectionMode = int(input("Select detector mode (1 = lite, 2 = full, 3 = heavy): "))
    # segmentationTightness = input("Provide segmentation tightness in [0,1] (default .5): ")
    fileName = "582_6h_76w_male_33a.jpg"
    detectionMode = 3
    segmentationTightness = .5
    # print("segmentation type: ", type(segmentationTightness))
    
    # Checking if tightness was specified
    if not segmentationTightness:
        imageHandler = ImageHandler.ImageHandler(fileName)
    else:
        imageHandler = ImageHandler.ImageHandler(fileName, float(segmentationTightness))
        
    # Creating landmark handler object using provided data
    landmarkHandler = PoseLandmarkHandler.PoseLandmarkHandler(imageHandler, detectionMode)
    
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
    print()
    print("Landmarks processed. Drawing landmarks on image: ")
    try:
        landmarkHandler.drawLandmarks()
    except:
        logging.exception("Error while drawing landmarks: ")
    
    middle_pixel, nose_pixel = landmarkHandler.getMeasurements() # Get points needed for measurement calculations

    # Saving landmarked image
    landmarkHandler.saveImage()
    
    # Creating segmentationHandler object, processing image, and saving the result
    segmentationHandler = SegmentationHandler.SegmentationHandler(imageHandler)
    segmentationHandler.segmentImage()
    segmentationHandler.find_head_measurement(middle_pixel, nose_pixel) # Use points calculated to try and find a better top measurement
    segmentationHandler.saveImage()

if __name__ == "__main__":
    main()