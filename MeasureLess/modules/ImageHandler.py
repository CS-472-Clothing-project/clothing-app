import cv2
import numpy
import mediapipe as mp
import logging
import sys

class ImageHandler:
    # TODO: Update members to account for both images
    def __init__(self, segTightness=.5):
        # fileName and segTightness can likely be deleted and replaced
        # with local variables
        # self.fileName = None
        self.segTightness = segTightness
        self.segmentedImage = [None] * 2
        self.annotatedImage = [None] * 2
        self.detectedImage = [None] * 2
        self.cvImage = [None] * 2
        self.ndArrayImage = [None] * 2
        self.mpImage = [None] * 2
        self.loadSuccess = False
        
        # This try/except block might be best served as a member function, 
        # not as part of the constructor
        # try:
        #     print("Loading image: ", fileName)
            
        #     # Current workflow requires the file to be read twice,
        #     # once for each framework. Should look into how to just
        #     # read once
        #     self.cvImage = cv2.imread(fileName)
        #     self.mpImage = mp.Image.create_from_file(fileName)
        #     self.ndArrayImage = self.mpImage.numpy_view()
        #     self.loadSuccess = True
            
        # except:
        #     print("Error loading image")
        
    # Load Image function
    def loadImages(self):
        try:
            fileName1 = input("Input first file name with extension: ")
            print("Loading image ", fileName1, "...")
            self.cvImage[0] = cv2.imread(fileName1)
            self.mpImage[0] = mp.Image.create_from_file(fileName1)
            self.ndArrayImage[0] = self.mpImage[0].numpy_view()
            
            fileName2 = input("Input second file name with extension: ")
            self.cvImage[1] = cv2.imread(fileName2)
            self.mpImage[1] = mp.Image.create_from_file(fileName2)
            self.ndArrayImage[1] = self.mpImage[1].numpy_view()
            
        except:
            logging.exception("There was an error when loading the image")
            sys.exit()
        # exitFlag = False
        # try:
        #     fileName = input("Input file name with extension (enter quit to exit): ")
        #     print("Loading image ", fileName, "...")
        #     self.cvImage = cv2.imread(fileName)
        #     self.mpImage = mp.Image.create_from_file(fileName)
        #     self.ndArrayImage = self.mpImage.numpy_view()
        # except:
        #     logging.exception("There was an error when loading the image. Please try again")
        #     sys.exit()
            
    
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
        # print("Saving image...")
        # try:
        #     cv2.imwrite("results/" + fileName, image)
        #     print("File saved to results/", fileName)
        # except:
        #     logging.exception("Error while saving imgage: ")
        #     sys.exit()
    