from flask import Flask, request, send_file
from flask_cors import CORS
import dataPrometheus
from PIL import Image
import os, io

# Flask API, called when file is run
app = Flask(__name__)
CORS(app)

@app.route("/mapDatabase/<db>/<reversing>", methods=["GET", "POST"])
def mapDatabase(db, reversing):
    # Checks to see if the file was sent properly and can be read
    if request.method != 'POST':
        return 0

    f = request.files['file']
    dataPrometheus.mapDatabase(f.filename, f, reversing)
        
    # Gets the path of the resulting image
    imgPath = os.getcwd() + "\output\output.png"
    print(imgPath)

    # Opens the file and reads the binary
    with open(imgPath, 'rb') as input:
        # Stores bytes in a buffer
        img_bytes = io.BytesIO(input.read())
        img = Image.open(img_bytes)

    # Saves the image to a new buffer
    output_buffer = io.BytesIO()
    img.save(output_buffer, 'png')
    output_buffer.seek(0)

    # Returns the image from the new buffer
    return send_file(output_buffer, mimetype='image/png')


    
# Starts the Flask API
if __name__ == '__main__':
    app.run()