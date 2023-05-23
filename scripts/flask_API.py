"""
The mediator between the frontend GUI (called through JavaScript)
and greater Data Prometheus (written in Python).
"""


from flask import Flask, request, jsonify
from flask_cors import CORS
from process_files import process_files


# Flask API, called when file is run
app = Flask(__name__)
CORS(app)


@app.route("/dataPrometheusAPI/<request_endpoint>", methods=["GET", "POST"])
def data_prometheus_api(request_endpoint):
    """
    The mediator between the frontend and Data Prometheus.
    """

    # Checks to see if the file was sent properly and can be read
    if request.method != 'POST':
        return jsonify('Invalid request method'), 200

    files = request.files.getlist('file')

    # Calls various functions depending on the request endpoint
    if request_endpoint == 'mapDatabase':
        status, error_message = process_files(files, request_endpoint)
    elif request_endpoint == 'mergeDatabase':
        status, error_message = process_files(files, request_endpoint)
    else:
        status, error_message = 0, "Endpoint not recognized."

    if status == 0:
        print(error_message)
        return jsonify(error_message), 200

    # Sends the image to the frontend
    with open("output/output.png", "rb") as output_image:
        encoded_image = output_image.read()
        return encoded_image, 200,  {'Content-Type': 'image/png'}


# Starts the Flask API
if __name__ == '__main__':
    app.run()
