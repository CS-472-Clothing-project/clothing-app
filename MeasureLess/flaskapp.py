import os
import MeasureLess
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from FlaskRunner import run_from_flask
import io

# Sets the directory from the __file__ variable to generate a universal absolute path for uploads
# Will likely change functionality to not save the image and just accept the object itself
directory_name = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(directory_name, 'uploads')


# Setting allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

# Creating flask app object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CORS (cross origin resource sharing) enables locally hosted react frontend
# to talk to this app (may not be needed in final implementation)
CORS(app)

# Checks for valid filetype by extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask decorator
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print("Request received")
    if request.method == 'POST':
        print("Received POST request")
        print(f"Received height: {request.form.get('height')}")
        print(f"Received bodyType: {request.form.get('bodyType')}")
        print(f"BlobType" + str(type(request.files.get('frontImage'))))
        front_image = request.files.get('frontImage')
        side_image = request.files.get('sideImage')
        
        frontBytes = io.BytesIO()
        sideBytes = io.BytesIO()
        
        front_image.save(frontBytes)
        side_image.save(sideBytes)
        
        
        print("front image type: ", type(front_image.stream.read()))
        print("side image type: ", type(side_image.stream.read()))
        # MeasureLess.py variant, creates an instance of the MeasureLess class and runs the pipeline
        ml = MeasureLess.MeasureLess(frontBytes.getvalue(), sideBytes.getvalue(), request.form.get('height'), request.form.get('bodyType'))
        result = ml.runMeasureLess()
        
        # FlaskRunner.py variant 
        # result = run_from_flask(frontBytes.getvalue(), sideBytes.getvalue(), request.form.get('height'), request.form.get('bodyType'))
        
        print("Processing complete")
        # Updated measurement handler to return a dictionary that will be turned into a json went sent to the frontend
        # Ensures no user data is saved directly onto the server
        return jsonify(result), 200
    return jsonify({'message': 'Send a POST request to upload a file'}), 200