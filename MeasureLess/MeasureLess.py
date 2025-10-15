from modules import ImageHandler
from modules import PoseLandmarkHandler
import cv2
import logging

def main():
    # Short intro message for development
    print("Welcome to MeasureLess, the measure-less app for tailoring.")
    
    # Creating the image object by calling the import handler
    fileName = input("Input name of the image file (with extension): ")
    detectionMode = int(input("Select detector mode (1 = lite, 2 = full, 3 = heavy): "))
    segmentationTightness = input("Provide segmentation tightness in [0,1] (default .5): ")
    # print("segmentation type: ", type(segmentationTightness))
    
    if not segmentationTightness:
        imageFrame = ImageHandler.ImageHandler(fileName)
    else:
        imageFrame = ImageHandler.ImageHandler(fileName, float(segmentationTightness))
        
    print("imageFrame type: ", type(imageFrame))
    landmarkDetector = PoseLandmarkHandler.PoseLandmarkHandler(imageFrame, detectionMode)
    
    print("Loading Detector...")
    try:
        landmarkDetector.loadDetector()
    except:
        logging.exception("And error occurred when loading the detector: ")
        
    print("Detector loaded. Running image detection...")
    try:
        landmarkDetector.detectImage()
    except:
        logging.exception("Error when detecting image: ")
        
    print()
    print("Image processed. Drawing image landmarks: ")
    try:
        landmarkDetector.drawLandmarks()
    except:
        logging.exception("Error while drawing landmarks: ")
        
    landmarkDetector.saveImage()

if __name__ == "__main__":
    main()