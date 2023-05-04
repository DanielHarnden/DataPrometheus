import importlib, webbrowser, subprocess, sys, os

def main():
    checkForPackages()
    openFrontend()
    attemptFlask()

# Checks to see if the proper Python packages exist
def checkForPackages():
    print("Determining if the correct Python packages are installed...")

    # The list of packages that should be installed using pip
    packages = ['flask', 'flask-cors', 'Pillow', 'graphviz', 'snowballstemmer', 'sqlparse']

    for package in packages:
        # Attempts to import the module; if it can not, that means it is not installed.
        try:
            if package == "Pillow":
                importlib.import_module("PIL")
            elif package == "flask-cors":
                importlib.import_module("flask_cors")
            else:
                importlib.import_module(package)
        except ModuleNotFoundError:
            print(package + " is not downloaded on the local machine. Downloading " + package + "...")
            command = "pip install " + package
            # Attempts to execute the command, throws an error and ends the program if the command does not run as intended.
            try:
                subprocess.check_call(command)

            except:
                print("There was an error importing the " + package + " package. Please make sure that pip is installed.")
                temp = input()
                sys.exit()
            
    print("All packages installed!\n")

# Opens the frontend page in the user's web browser
def openFrontend():
    webbrowser.open("http://localhost:8000/")

# Attempts to start the Flask API
def attemptFlask():
    print("Attempting to start the Flask API...")
    subprocess.check_call("python .\\prometheusMain\\flaskAPI.py")


if __name__ == "__main__":
    main()