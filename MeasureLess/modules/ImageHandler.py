import cv2
import numpy
import mediapipe as mp

class ImageHandler:
    def __init__(self, fileName, segTightness=.5):
        self.fileName = fileName
        self.segTightness = segTightness
        self.segmentedImage = None
        
        try:
            print("Loading image: ", fileName)
            
            # Current workflow requires the file to be read twice,
            # once for each framework. Should look into how to just
            # read once
            self.cvImage = cv2.imread(fileName)
            self.mpImage = mp.Image.create_from_file(fileName)
            self.ndArrayImage = self.mpImage.numpy_view()
            
        except:
            print("Error loading image")
        
    # Placeholder for later when checking for image type compatibility
    def checkImageType(self):
        pass