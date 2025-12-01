import logging
import argparse
import sys

# Will be used to handle any arguments needed by debugging.py
# Show usage and exit
if(len(sys.argv) != 13):
    print("Usage: python debugging.py --uH <userHeight> --fImg <frontImage> --sImg <sideImage> --iExt <imageExtension> --dM <detectorMode> --sT <segTightness>")

    sys.exit(0)



# Add support for command line arguments, will be useful for testing and further development
measureLessArgs = argparse.ArgumentParser(description="To make testing easier, we implemented commandline arguments")
# Get the arguments
measureLessArgs.add_argument("--fImg", type=str, help="Front image file name.")
measureLessArgs.add_argument("--sImg", type=str, help="Side image file name.")
measureLessArgs.add_argument("--dM", type=int, default=2, help="Detector mode (1 = lite, 2 = full, 3 = heavy).")
measureLessArgs.add_argument("--sT", type=float, default=0.5, help="Segmentation tightness in [0, 1] (default .5).")
measureLessArgs.add_argument("--iExt", type=str, help="Image file extension.")
measureLessArgs.add_argument("--uH", type=int, default=70, help="User height in inches.")