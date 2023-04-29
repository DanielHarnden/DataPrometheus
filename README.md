# Data Atlas

The primary repository for the Data Atlas capstone project.

## Running Data Atlas

To run Data Atlas, use Python to execute runDataAtlas.py. This will install the flask, flask_cors, and PIL Python libraries before attempting to run the Frontend, Middleware, and Backend Docker containers. A Flask API will then begin running in the prompt that you executed runDataAtlas.py.

## Stopping Data Atlas

Manually stop the Flask API, then execute stopDataAtlas.py to stop the Docker containers from running.

## Finding Generated Files

Data Atlas saves a .db file of the newly generated database, as well as an the image file, to the local machine. Databases can be found in the directory DataAtlas/Dockers/volume/databases in the format originalName_updated.db, and images can be found in the directory DataAtlas/Dockers/volume/generatedPngs in the format originalName_updated.sqlite.png

## Data Atlas Structure

Once Data Atlas is running, the end user is directed to a React webpage that hosts the GUI. The user is prompted to choose a database to be atlased. Once the database is chosen, React will call a Flask API which starts the long process of parsing, mapping, and generating an image based on the database (a visual representation of the process is below). Once the image is generated, the Flask API returns that image to the React webpage, which updates accordingly.

![Data Atlas Flowchard](/Documentation/DataAtlas.png)