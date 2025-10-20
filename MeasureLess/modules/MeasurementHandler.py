import numpy as np
import logging
import mediapipe as mp
import cv2
import pandas

class MeasurementHandler:
    def __init__(self, imageHandler, debug=True):
        self.imageHandler = imageHandler
        self.measurementData = None
        self.debug = debug
    
    def saveToCSV(self):
        pass