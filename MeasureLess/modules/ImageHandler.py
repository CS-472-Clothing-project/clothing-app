import cv2
import numpy
import mediapipe as mp
import logging
import os

class ImageHandler:
    # TODO: Update members to account for both images
    def __init__(self, fileName, segTightness=.5, debug=True):
        self.fileName = fileName
        self.segTightness = segTightness
        self.segmentedImage = None
        self.annotatedImage = None
        self.debug = debug
        
        try:
            print("Loading image: ", fileName)
            
            # Current workflow requires the file to be read twice,
            # once for each framework. Should look into how to just
            # read once
            self.cvImage = cv2.imread(fileName)
            # Change to only be read once, i.e. having opencv read in the image
            # and simply convert 
            tmp_image = cvImage.copy()
            # OpenCV reads in images as BGR instead of RGB, so convert it
            tmp_image = cv2.cvtColar(tmp_image, cv2.COLOR_BGR2RGB)
            self.mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=tmp_image)
            # self.mpImage = mp.Image.create_from_file(fileName)
            self.ndArrayImage = self.mpImage.numpy_view()
            
        except:
            logging.exception("Error loading image")
        
    # Placeholder for later when checking for image type compatibility
    def checkImageType(self):
        pass
    
    # Image saving function (to a file)
    def saveImage(self, imageSelection):
        pass
    
    # For privacy concerns, check if the file exists
    # If it does, delete it
    def __del__(self):
        if(self.debug == False):
            # Using the os library, check if the image is present, if it is and debug is False
            # Delete the image
            if os.path.isfile(self.fileName):
                os.remove(self.fileName)
                print(f"Image: {self.fileName} has been removed.")
        return