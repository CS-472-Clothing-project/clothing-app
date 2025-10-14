import cv2
import numpy
import mediapipe as mp

class ImageHandler:
    def __init__(self, fileName, segTightness=.7):
        self.fileName = fileName
        self.segTightness = segTightness
        try:
            print("Loading image ", fileName)
            self.rawImage = cv2.imread(fileName)
            print("Length of loaded image vector: ", self.rawImage.shape)
        except:
            print("Error loading image")
            
        
        # self.rgbImage = self.convertToMPImage()
        self.mpImage = mp.Image.create_from_file(fileName)
        
    # def convertToMPImage(self):
    #     try:
    #         # self.rgbImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.rawImage)
    #         return mp.Image(image_format=mp.ImageFormat.SRGB, data=self.rawImage)
    #     except:
    #         print("Error converting image to Mediapipe object")