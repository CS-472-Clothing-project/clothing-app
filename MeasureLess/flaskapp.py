import os
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
        
        result = run_from_flask(frontBytes.getvalue(), sideBytes.getvalue(), request.form.get('height'), request.form.get('bodyType'))
        print("Processing complete")
        
        return jsonify({'message': 'POST request received'}), 200
    return jsonify({'message': 'Send a POST request to upload a file'}), 200

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # Checks if file was passed
#         if 'file' not in request.files:
#             # Flash call to place the error on the error stack. Likely not necessary
#             # with implemented json return
#             flash('No file part')
#             return jsonify({'error': 'No file part'}), 400
#         file = request.files['file']
        
#         if file.filename == '':
#             # Flash call to place the error on the error stack. Likely not necessary
#             # with implemented json return
#             flash('No selected file')
#             return jsonify({'error': 'No selected file'}), 400
#         # File is good
#         if file and allowed_file(file.filename):
#             # Prevent directory manipulation attacks by securing the filename itself. Prevents
#             # names like ../../../filename.ext
#             filename = secure_filename(file.filename)
#             # Currently saves passed image. Aim is to change this to pass the object itself and 
#             # work with it that way
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
#     return