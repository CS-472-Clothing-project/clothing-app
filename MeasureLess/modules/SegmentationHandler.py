import mediapipe as mp
import numpy as np
import cv2
import logging

class SegmentationHandler:
    def __init__(self, imageHandler):
        self.segmentedImage = imageHandler.cvImage.copy()
        self.imageHandler = imageHandler
        self.tightness = imageHandler.segTightness
        
    # This needs to be called twice
    def segmentImage(self):
        # Using the mediapipe pose module to set options and process the image
        # provided with imageHandler
        with mp.solutions.pose.Pose(static_image_mode=True,
                                    model_complexity=2,
                                    enable_segmentation=True) as pose:
            image = self.imageHandler.cvImage
            processedImage = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
        # Creates a boolean mask to use to apply the greenscreen
        condition = np.stack((processedImage.segmentation_mask,) * 3, axis=-1) > self.tightness
        
        backgroundImage = np.zeros(image.shape, dtype=np.uint8)
        
        # For every pixel in backgroundImage, change the color to greenscreen
        backgroundImage[:] = [4, 244, 4]
        self.segmentedImage = np.where(condition, self.segmentedImage, backgroundImage)
        
    
    def saveImage(self):
        print("Saving image...")
        try:
            cv2.imwrite("results/segmented-image.png", self.segmentedImage)
        except:
            logging.exception("Error while saving image")
        print("Image saved to results as segmented-image.png")