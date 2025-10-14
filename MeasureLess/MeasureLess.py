from modules import ImageHandler
from modules import PoseLandmarkDetector
import cv2

def main():
    # Short intro message for development
    print("Welcome to MeasureLess, the measure-less app for tailoring.")
    
    # Creating the image object by calling the import handler
    fileName = input("Input name of the image file (with extension): ")
    detectionMode = int(input("Select detector mode (1 = lite, 2 = full, 3 = heavy): "))
    segmentationTightness = input("Provide segmentation tightness: ")
    imageFrame = ImageHandler.ImageHandler(fileName, segmentationTightness)
    
    # landmarkDetector = PoseLandmarkDetector.PoseLandmarkDetector(imageFrame.rgbImage, detectionMode)
    
    landmarkDetector = PoseLandmarkDetector.PoseLandmarkDetector(imageFrame.mpImage, detectionMode)
    
    # landmarkDetector.loadDetector()
    landmarkDetector.drawLandmarks()
    
    try:
        cv2.imwrite("result.png", landmarkDetector.landmarkedImage)
    except:
        print('error in saving image')

if __name__ == "__main__":
    main()