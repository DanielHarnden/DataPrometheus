from flask import Flask, request, jsonify
from flask_cors import CORS
from process_Files import processFiles

# Flask API, called when file is run
app = Flask(__name__)
CORS(app)

@app.route("/dataPrometheusAPI/<requestEndpoint>", methods=["GET", "POST"])
def dataPrometheusAPI(requestEndpoint):
    # Checks to see if the file was sent properly and can be read
    if request.method != 'POST':
        return jsonify('Invalid request method'), 200

    files = request.files.getlist('file')

    # Calls various functions depending on the request endpoint
    if requestEndpoint == 'mapDatabase':
        status, errorMessage = processFiles(files, requestEndpoint)
    elif requestEndpoint == 'mergeDatabase':
        status, errorMessage = processFiles(files, requestEndpoint)
    else:
        status, errorMessage = 0, "Endpoint not recognized.", 0

    if status == 0:
        print(errorMessage)
        return jsonify(errorMessage), 200
        
    # Sends the image to the frontend
    with open("output/output.png", "rb") as outputImage:
        encodedImage = outputImage.read()
        return encodedImage, 200,  {'Content-Type': 'image/png'}
    
# Starts the Flask API
if __name__ == '__main__':
    app.run()