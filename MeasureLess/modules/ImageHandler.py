import cv2
import numpy
import mediapipe as mp
import logging
import sys
import logging
import os

class ImageHandler:
    # TODO: Update members to account for both images
    def __init__(self, fileNames, segTightness=.5, debug=True):
        self.fileNames = fileNames
        self.segTightness = segTightness
        self.backgroundColor = [4, 244, 4]
        self.segmentedImage = [None] * 2
        self.annotatedImage = [None] * 2
        self.detectedImage = [None] * 2
        self.cvImage = [None] * 2
        self.ndArrayImage = [None] * 2
        self.mpImage = [None] * 2
        self.loadSuccess = False
        self.debug = debug
        
    # Load Image function
    def loadImages(self, fileNames):
        # TODO Update this change this
        try:
            # Should be unneeded for now
            # fileName1 = input("Input first file name with extension: ")
            # print("Loading image ", fileName1, "...")
            self.cvImage[0] = cv2.imread(fileNames[0])
            # self.mpImage[0] = mp.Image.create_from_file(fileName1)
            tmp_image = self.cvImage[0].copy()
            self.mpImage[0] = mp.Image(image_format=mp.ImageFormat.SRGB, data=tmp_image)
            self.ndArrayImage[0] = self.mpImage[0].numpy_view()
        
            # fileName2 = input("Input second file name with extension: ")
            self.cvImage[1] = cv2.imread(fileNames[1])
            tmp_image = self.cvImage[1].copy()
            self.mpImage[1] = mp.Image(image_format=mp.ImageFormat.SRGB, data=tmp_image)
            # self.mpImage[1] = mp.Image.create_from_file(fileName2)
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
	        # Will have to be adjusted or even removed if we figure out to receive images directly from the front end
            for i in range(len(self.fileNames)):
                if os.path.isfile(self.fileNames[i]):
                    os.remove(self.fileNames[i])
                    print(f"File: {self.fileNames[i]} has been removed.")
        return
