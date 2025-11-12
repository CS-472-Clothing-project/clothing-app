import os
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

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
        # Checks if file was passed
        if 'file' not in request.files:
            # Flash call to place the error on the error stack. Likely not necessary
            # with implemented json return
            flash('No file part')
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        
        if file.filename == '':
            # Flash call to place the error on the error stack. Likely not necessary
            # with implemented json return
            flash('No selected file')
            return jsonify({'error': 'No selected file'}), 400
        # File is good
        if file and allowed_file(file.filename):
            # Prevent directory manipulation attacks by securing the filename itself. Prevents
            # names like ../../../filename.ext
            filename = secure_filename(file.filename)
            # Currently saves passed image. Aim is to change this to pass the object itself and 
            # work with it that way
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    return