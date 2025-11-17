# clothing-app
## Backend usage
Make sure that your preferred version of conda is installed (I recommend miniconda) and create an environment for the app using python 3.12, then run:
\
\
`pip install -r requirements.txt`
\
\
When requirements are installed, make sure the images you intend to use are in the Measureless directory (at the same level as MeasureLess.py). Also make sure the appropriate mediapipe models are located in `Measureless/models/`. They can be downloaded from [this page.](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/index#models)
\
\
Once you've ensured the images and models are in the right place, run the command as follows:
\
\
`python3 MeasureLess.py --fImg <frontimage> --sImg <sideimage> --dM <detectorMode> --sT <segTightness>`
\
\
Where everything in <> is the appropriate value, for example:
\
\
`python3 MeasureLess.py --fImg front.jpg --sImg side.jpg --dM 2 --sT .5`
## Todo:
* Refactor the backend code so all variables follow consistent naming conventions. Currently both camel case and snake case are used at varying points.