from flask import Flask, request, jsonify
from flask_cors import CORS
import dataPrometheus

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
        status, errorMessage, operationalTime = dataPrometheus.mapDatabase(files)
    elif requestEndpoint == 'mergeDatabase':
        status, errorMessage, operationalTime = dataPrometheus.mergeDatabase(files)

    if status == 0:
        print(errorMessage, "\n", f"Total Operational Time before error: {operationalTime}")
        return jsonify(errorMessage), 200
        
    # Sends the image to the frontend
    with open("output/output.png", "rb") as outputImage:
        encodedImage = outputImage.read()
        return encodedImage, 200,  {'Content-Type': 'image/png'}
    
# Starts the Flask API
if __name__ == '__main__':
    app.run()