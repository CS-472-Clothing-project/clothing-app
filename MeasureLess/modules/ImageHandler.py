import cv2
import numpy
import mediapipe as mp

class ImageHandler:
    def __init__(self, fileName, segTightness=.5):
        self.fileName = fileName
        self.segTightness = segTightness
        try:
            print("Loading image: ", fileName)
            
            # Inputting image in 2 separate ways. Will likely remove rawImage as 
            # the mediapipe image can be converted as needed
            self.rawImage = cv2.imread(fileName)
            self.mpImage = mp.Image.create_from_file(fileName)
            self.ndArrayImage = self.mpImage.numpy_view()
        except:
            print("Error loading image")
            
        
        # self.rgbImage = self.convertToMPImage()
        # self.mpImage = mp.Image.create_from_file(fileName)
        
    # def convertToMPImage(self):
    #     try:
    #         # self.rgbImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.rawImage)
    #         return mp.Image(image_format=mp.ImageFormat.SRGB, data=self.rawImage)
    #     except:
    #         print("Error converting image to Mediapipe object")