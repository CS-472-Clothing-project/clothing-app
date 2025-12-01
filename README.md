# clothing-app

## Frontend usuage
Go to frontend directory and download packages
\
\
`npm install`
\
\
Than run the the webserver using Vite
\
\
`npm run dev`
\
\
It runs the server, so you can head over to http://localhost:5173/ or `o + enter` to open in your default browser.

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
Running through Flask:
\
Run the following command to launch the Flask server:

`flask --app flaskapp.py run`
\
\
Once both the front and backend server is running, use your browser to navigate to http://localhost:5173 and follow the instructions to enter height, body type, and take the images. Upon hitting "next" on the second image you should see a bunch of output on the flask console and if no errors were thrown, the page should redirect to the results. Currently the results are not properly getting sent back from the backend.
\
\
If you don't want to have to continuously use a webcam to take photos, I recommend using OBS to start a virtual camera with the source set to a stock image of a whole body photo (This will result in only using one photo for both front and side but it's good for checking functionality quickly)
\
\

Once you've ensured the images and models are in the right place, run the command as follows:
\
\
`python3 debugging.py --fImg <frontimage> --sImg <sideimage> --dM <detectorMode> --sT <segTightness>`
\
\
Where everything in <> is the appropriate value, for example:
\
\
`python3 debugging.py --fImg front.jpg --sImg side.jpg --dM 2 --sT .5`
## Todo:
* Refactor the backend code so all variables follow consistent naming conventions. Currently both camel case and snake case are used at varying points.
