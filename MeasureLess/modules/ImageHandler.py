import cv2
import numpy
import mediapipe as mp
import logging
import sys
import logging
import os

class ImageHandler:
    # TODO: Update members to account for both images
    def __init__(self, fileName, segTightness=.5, debug=True):
        self.fileName = fileName
        self.segTightness = segTightness
        self.segmentedImage = None
        self.annotatedImage = None
        self.loadSuccess = False
        self.cvImage = None
        self.ndArrayImage = None
        self.mpImage = None
        self.debug = debug
        
        # This try/except block might be best served as a member function, 
        # not as part of the constructor
        try:
            print("Loading image: ", fileName)
            
            # Current workflow requires the file to be read twice,
            # once for each framework. Should look into how to just
            # read once
            self.cvImage = cv2.imread(fileName)
            self.mpImage = mp.Image.create_from_file(fileName)
            self.ndArrayImage = self.mpImage.numpy_view()
            self.loadSuccess = True
            
        except:
            print("Error loading image")
        
    # Load Image function
    def loadImage(self):
        while self.loadSuccess == False:
            try:
                fileName = input("Input file name with extension (enter quit to exit): ")
                if fileName == "quit":
                    print("Exiting...")
                    sys.exit()
                print("Loading image ", fileName, "...")
                self.cvImage = cv2.imread(fileName)
                self.mpImage = mp.Image.create_from_file(fileName)
                self.ndArrayImage = self.mpImage.numpy_view()
                if self.cvImage and self.mpImage and self.ndArrayImage:
                    self.loadSuccess = True
            except:
                logging.exception("There was an error when loading the image")
        pass
    
    # Placeholder for later when checking for image type compatibility
    def checkImageType(self):
        pass
    
    # Image saving function (to a file)
    def saveImage(self, imageSelection):
        pass
    
    # For privacy concerns, check if the file exists
    # If it does, delte it
    def __del__(self):
        if(self.debug == False):
            # Using the os library, check if the image is present, if it is and debug is False
            # Delete the image
            if os.path.isfile(self.fileName):
                os.remove(self.fileName)
                print(f"File: {self.fileName} has been removed.")
        return