import mediapipe as mp
import numpy as np
import cv2
import logging

class SegmentationHandler:
    def __init__(self, imageHandler):
        self.segmentedImage = imageHandler.cvImage.copy()
        self.imageHandler = imageHandler
        self.tightness = imageHandler.segTightness
        
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
        
    def find_head_measurement(self, middle_px, nose_px):
        """
            Function to try and find an actual hieght pixel from Nose pixel,
            loops starting from nose pixel until it hits background. Found 
            pixel is printed to segmented-image.png

            TODO:
                Issue with for loop breaking too early
                Creating hieght line once top pixel is found
        """
        # cv2.circle(self.segmentedImage, middle_px, 3, (255,0,255), thickness=-1)
        # cv2.circle(self.segmentedImage, nose_px, 3, (255,0,255), thickness=-1)
        print(f"Segemented Imaged Shape:  {self.segmentedImage.shape}")
        print(f"Nose pixel = {nose_px}")
        x,y = nose_px
        # test_pixel = (x,y-55)
        # print(f"test pixel = {test_pixel}")
        # print(f"test pixel color value = {self.segmentedImage[test_pixel]}")
        # cv2.circle(self.segmentedImage, test_pixel, 3, (255,0,255,), thickness=-1)

        # Loops from nose, until it hits green background, currently breaking too early
        for y_pixel in range(y, 0, -5):
            temp_pixel = (x,y_pixel)
            print(f"Temp pixel = {temp_pixel} with color {self.segmentedImage[temp_pixel]}")
            if np.array_equal(self.segmentedImage[temp_pixel], np.array([4, 244, 4])):
                break
            
        print(temp_pixel)

        cv2.circle(self.segmentedImage, temp_pixel, 1, (255,0,0), thickness=-1)
    def saveImage(self):
        print("Saving image...")
        try:
            cv2.imwrite("results/segmented-image.png", self.segmentedImage)
        except:
            logging.exception("Error while saving image")
        print("Image saved to results as segmented-image.png")