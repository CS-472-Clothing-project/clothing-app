from modules import ImageHandler
from modules import PoseLandmarkHandler
from modules import SegmentationHandler

import logging
import argparse
import sys

# TODO: Update logic to accept and process 2 images at once. One side profile, one front profile
# TODO: For testing purposes, add the ability to use command-line arguments
def main():
    # Show usage
    if(len(sys.argv) != 7):
        print("Usage: python MeasureLess.py --fN <fileName> --dM <detectorMode> --sT <segTightness>")
        sys.exit(0)

    accepted_img_types = [".jpg", ".jpeg", ".png", ".bmp"]
    # Add support for command line arguments, will be useful for testing and further development
    argParser = argparse.ArgumentParser(description="To make testing easier, we implemented commandline arguments")
    argParser.add_argument("--fN", type=str, help="Image file name.")
    argParser.add_argument("--dM", type=int, help="Detector mode (1 = lite, 2 = full, 3 = heavy)")
    argParser.add_argument("--sT", type=float, default=0.5, help="Segmentation tightness in [0, 1] (default .5)")

    args = argParser.parse_args()
    
    # Short intro message for development
    print("Welcome to MeasureLess, the measure-less app for tailoring.")

    # Check passed through arguments
    # print(args.fN)
    # print(args.dM)
    # print(args.sT)

    # TODO add error checking for file extentsions, for now only include .jpg, .png, and .bmp
    if(os.path.splittext(args.fN)[1] in accepted_img_types) == False:
        print(f"Unsupported file type: {args.fN}.")
        sys.exit(0)
    
    # Creating the image object by calling the import handler
    fileName = args.fileName
    detectionMode = args.detectionMode    
    segmentationTightness = args.segmentationTightness
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
    main()