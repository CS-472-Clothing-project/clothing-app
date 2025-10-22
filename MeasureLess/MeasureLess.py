from modules import ImageHandler
from modules import PoseLandmarkHandler
from modules import SegmentationHandler
from CLArgsHandler import measureLessArgs

import logging
import os
import sys

# TODO: Update logic to accept and process 2 images at once. One side profile, one front profile
def main(args):

    accepted_img_types = [".jpg", ".jpeg", ".png", ".bmp"]
    fileNames = []
    
    # Short intro message for development
    print("Welcome to MeasureLess, the measure-less app for tailoring.")

    # TODO add error checking for file extentsions, for now only include .jpg, .png, and .bmp
    # if(os.path.splitext(args.fImg)[1] in accepted_img_types) == False:
    #     print(f"Unsupported file type: {args.fImg}.")
    #     sys.exit(0)
    
    if not(os.path.splitext(args.fImg)[1] in accepted_img_types and os.path.splitext(args.sImg)[1] in accepted_img_types):
        print(f"Unsupported file type detected. {args.fImg} or {args.sImg}.")
        sys.exit(0)


    # Creating the image object by calling the import handler
    # Make fileName a list and pass that into imageHandler. Might work well for opening the two images
    fileNames.append(args.fImg)
    fileNames.append(args.sImg)
    print(fileNames)
    detectionMode = args.dM
    segmentationTightness = args.sT

    # print("segmentation type: ", type(segmentationTightness))
    # detectionMode = int(input("Select detector mode (1 = lite, 2 = full, 3 = heavy): "))
    # segmentationTightness = input("Provide segmentation tightness in [0,1] (default .5): ")
    
    # Checking if tightness was specified
    if not segmentationTightness:
        imageHandler = ImageHandler.ImageHandler(fileNames)
    else:
        imageHandler = ImageHandler.ImageHandler(fileNames, float(segmentationTightness))
        
    
    imageHandler.loadImages(fileNames)
        
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

if __name__ == "__main__":
    args = measureLessArgs.parse_args()
    main(args)