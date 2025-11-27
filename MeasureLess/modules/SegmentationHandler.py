import mediapipe as mp
import numpy as np
import cv2
import logging

class SegmentationHandler:
    def __init__(self, imageHandler, debug=True):
        # self.segmentedImage = imageHandler.cvImage.copy()
        # Create the mutable image objects
        self.imageHandler = imageHandler
        self.tightness = imageHandler.segTightness
        self.debug = True

        for i in range(len(self.imageHandler.segmentedImage)):
            self.imageHandler.segmentedImage[i] = self.imageHandler.cvImage[i].copy()
        
        
    # This needs to be called twice
    def segmentImage(self):
        # Using the mediapipe pose module to set options and process the image
        # provided with imageHandler
        processedImage = [None] * self.imageHandler.imageCount
        image = [None] * self.imageHandler.imageCount
        condition = [None] * self.imageHandler.imageCount
        with mp.solutions.pose.Pose(static_image_mode=True,
                                    model_complexity=2,
                                    enable_segmentation=True) as pose:
            for i in range(len(self.imageHandler.segmentedImage)):
                image[i] = self.imageHandler.cvImage[i].copy()
                processedImage[i] = pose.process(cv2.cvtColor(image[i], cv2.COLOR_BGR2RGB))
            
        # Creates a boolean mask to use to apply the greenscreen
        for i in range(len(self.imageHandler.segmentedImage)):
            condition[i] = np.stack((processedImage[i].segmentation_mask,) * 3, axis=-1) > self.tightness
        
        for i in range(len(self.imageHandler.segmentedImage)):
            backgroundImage = np.zeros(image[i].shape, dtype=np.uint8)
        
            # For every pixel in backgroundImage, change the color to greenscreen
            backgroundImage[:] = self.imageHandler.backgroundColor.copy()
            self.imageHandler.segmentedImage[i] = np.where(condition[i], self.imageHandler.segmentedImage[i], backgroundImage)