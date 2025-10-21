import logging
import argparse
import sys

# Will be used to handle any arguments needed by MeasureLess.py
# Show usage and exit
if(len(sys.argv) != 9):
    print("Usage: python MeasureLess.py --fImg <frontimage> --sImg <sideimage> --dM <detectorMode> --sT <segTightness>")
    sys.exit(0)

# Add support for command line arguments, will be useful for testing and further development
measureLessArgs = argparse.ArgumentParser(description="To make testing easier, we implemented commandline arguments")
# Get the arguments
measureLessArgs.add_argument("--fImg", type=str, help="Front image file name.")
measureLessArgs.add_argument("--sImg", type=str, help="Side image file name.")
measureLessArgs.add_argument("--dM", type=int, help="Detector mode (1 = lite, 2 = full, 3 = heavy)")
measureLessArgs.add_argument("--sT", type=float, default=0.5, help="Segmentation tightness in [0, 1] (default .5)")

