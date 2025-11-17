# clothing-app

## Command line usage for backend testing
The command line arguments and behaviors have changed, and the file name requirements have become more rigid. current usage:
python3 MeasureLess.py --iC <imageCount> --iName <imageName> --iExt <imageExtension> --dM <detectorMode> --sT <segTightness>  

To make it less of a pain and not have to enter 4 file names, we will enter a base name (iName), and an extension (iExt). For example, if the files were named:  
ex0.jpg  
ex1.jpg  
ex2.jpg  
ex3.jpg    
I would enter --iC 4 --iName ex --iExt jpg  
Note the absence of the number in the filename and the '.' in the extension.

## Todo:
Refactor the backend code so all variables follow consistent naming conventions. Currently both camel case and snake case are used at varying points.