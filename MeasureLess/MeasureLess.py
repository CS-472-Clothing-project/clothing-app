from modules import ImageHandler
from modules import PoseLandmarkHandler
from modules import SegmentationHandler
from CLArgsHandler import measureLessArgs

import logging
import os
import sys

# TODO: Update logic to accept and process 2 images at once. One side profile, one front profile
# TODO: For testing purposes, add the ability to use command-line arguments
def main(args):

    accepted_img_types = [".jpg", ".jpeg", ".png", ".bmp"]
    
    # Short intro message for development
    print("Welcome to MeasureLess, the measure-less app for tailoring.")

    # Check passed through arguments
    # print(args.fN)
    # print(args.dM)
    # print(args.sT)

    # TODO add error checking for file extentsions, for now only include .jpg, .png, and .bmp
    if(os.path.splitext(args.fN)[1] in accepted_img_types) == False:
        print(f"Unsupported file type: {args.fN}.")
        sys.exit(0)
    
    # Creating the image object by calling the import handler
    fileName = args.fN
    detectionMode = args.dM
    segmentationTightness = args.sT
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
        
    # Saving landmarked image
    landmarkHandler.saveImage()
    
    # Creating segmentationHandler object, processing image, and saving the result
    segmentationHandler = SegmentationHandler.SegmentationHandler(imageHandler)
    segmentationHandler.segmentImage()
    segmentationHandler.saveImage()

if __name__ == "__main__":
    args = measureLessArgs.parse_args()
    main(args)