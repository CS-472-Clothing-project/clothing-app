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
        self.segmentedImage = [None] * 2
        self.annotatedImage = [None] * 2
        self.detectedImage = [None] * 2
        self.cvImage = [None] * 2
        self.ndArrayImage = [None] * 2
        self.mpImage = [None] * 2
        self.loadSuccess = False
        
    # Load Image function
    def loadImages(self):
        try:
            fileName1 = input("Input first file name with extension: ")
            print("Loading image ", fileName1, "...")
            self.cvImage[0] = cv2.imread(fileName1)
            self.mpImage[0] = mp.Image.create_from_file(fileName1)
            self.ndArrayImage[0] = self.mpImage[0].numpy_view()
            
            # Current workflow requires the file to be read twice,
            # once for each framework. Should look into how to just
            # read once
            # Will be commented out for now as the implementation has changed a bit
            # self.cvImage = cv2.imread(fileName) 
            # Change to only be read once, i.e. having opencv read in the image
            # and simply convert 
            # self.tmp_image = self.cvImage.copy()
            # OpenCV reads in images as BGR instead of RGB, so convert it
            # self.mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.tmp_image)
            # self.mpImage = mp.Image.create_from_file(fileName)
            # self.ndArrayImage = self.mpImage.numpy_view()
            
        
            fileName2 = input("Input second file name with extension: ")
            self.cvImage[1] = cv2.imread(fileName2)
            self.mpImage[1] = mp.Image.create_from_file(fileName2)
            self.ndArrayImage[1] = self.mpImage[1].numpy_view()
            
        except:
            logging.exception("There was an error when loading the image")
            sys.exit()
            
    # Placeholder for later when checking for image type compatibility
    def checkImageType(self):
        pass
    
    # Image saving function (to a file)
    def saveResults(self):
        print("Saving results...")
        counter = 0
        for result in self.annotatedImage:
            try:
                cv2.imwrite("results/result" + str(counter) + ".png", result)
                print(f"Result {counter} saved to results/result{counter}.png")
                counter += 1
            except:
                logging.exception(f"Error while saving image{counter}: ")
                sys.exit()
        for result in self.segmentedImage:
            try:
                cv2.imwrite("results/result" + str(counter) + ".png", result)
                print(f"Result {counter} saved to results/result{counter}.png")
                counter += 1
            except:
                logging.exception(f"Error while saving image{counter}: ")
                sys.exit()
    
    # For privacy concerns, check if the file exists
    # If it does, delete it
    def __del__(self):
        if(self.debug == False):
            # Using the os library, check if the image is present, if it is and debug is False
            # Delete the image
            if os.path.isfile(self.fileName):
                os.remove(self.fileName)
                print(f"File: {self.fileName} has been removed.")
        return
