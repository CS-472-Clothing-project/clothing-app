import logging
import sys
import MeasureLess

from modules.CLArgsHandler import measureLessArgs

# For testing purposes more than anything, retains the commandline usage
def main(args):
    acceptedImgTypes = ["jpg", "jpeg", "png", "bmp"]

    if args.iExt not in acceptedImgTypes:
        print(f"Unsupported file extension: {args.iExt}. Supported extensions are: {acceptedImgTypes}")
        sys.exit(0)
    # Make the ml class
    ml = MeasureLess.MeasureLess(args.fImg, args.sImg, args.uH, detectionMode=args.dM, 
                                 segmentationTightness=args.sT, debug=True)
    # Run the pipeline
    result = ml.runMeasureLess()
    


if __name__ == "__main__":
    args = measureLessArgs.parse_args()
    main(args)