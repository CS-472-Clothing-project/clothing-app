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
        
    def getMeasurementScale(self, middle_px, nose_px, user_hieght = 1828.8):
        """
            Function to get the scale of mm / px by finding the users pixel hieght
            and comparing it to the users actual hieght.
        """

        print(f"Segemented Imaged Shape:  {self.segmentedImage.shape}")
        print(f"Nose pixel = {nose_px}")
        x,y = nose_px


        def check_if_background(x, y):
            if (np.array_equal(self.segmentedImage[(y-1, x)], np.array([4, 244, 4]))): # Check up
                if (np.array_equal(self.segmentedImage[(y-2, x)], np.array([4, 244, 4]))): # Check up + 1
                    return True
            # if (np.array_equal(self.segmentedImage[(y,x)], np.array([4, 244, 4]))): # Check pixel
            #     return True
            #     if (np.array_equal(self.segmentedImage[(y , x + 1)], np.array([4, 244, 4]))): # Check right
            #         if ( np.array_equal(self.segmentedImage[(y,  x-1)], np.array([4, 244, 4]))): # Check left
            #             if (np.array_equal(self.segmentedImage[(y-1, x)], np.array([4, 244, 4]))): # Check up
            #                 if (np.array_equal(self.segmentedImage[(y+1, x)], np.array([4, 244, 4]))): # Check down
            #                     return True
            return False

        # Loops from nose, until it hits green background, currently breaking too early
        green_count = 0
        for y_pixel in range(y, 0, -1):
            top_pixel = (x, y_pixel)
            # print(f"Temp pixel = {top_pixel} with color {self.segmentedImage[y_pixel, x]}")
            if check_if_background(x = top_pixel[0], y= top_pixel[1]):
                break
                
        # visualizing findings
        cv2.circle(self.segmentedImage, top_pixel, 1, (0, 255, 255), thickness=-1)
        cv2.line(self.segmentedImage, middle_px, top_pixel, (50,255,255), 2)

        # getting scale factor 
        pixel_height = np.linalg.norm(np.array(middle_px) - np.array(top_pixel))
        x,y = middle_px
        temp_px = (x,y - int(pixel_height))
        cv2.circle(self.segmentedImage, temp_px, 1, (0, 255, 255), thickness=-1)
        # print(pixel_height)

        scale = user_hieght/pixel_height # manually inputed user height to get scale
        print (scale)

        return scale 
    
    def saveImage(self):
        print("Saving image...")
        try:
            cv2.imwrite("results/segmented-image.png", self.segmentedImage)
        except:
            logging.exception("Error while saving image")
        print("Image saved to results as segmented-image.png")