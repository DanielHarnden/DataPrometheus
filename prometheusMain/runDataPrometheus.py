import importlib, webbrowser, subprocess, sys

def main():
    checkForPackages()

    print("Opening GUI in user's web browser...")
    webbrowser.open("http://localhost:8000/")
    
    print("Attempting to start the Flask API...")
    try:
        subprocess.check_call("python .\\prometheusMain\\flaskAPI.py")
    except:
        print("There was an error starting the Flask API.")
        sys.exit()


# Checks to see if the proper Python packages exist
def checkForPackages():
    print("Determining if the correct Python packages are installed...")

    # The list of packages that should be installed using pip
    packages = ['flask', 'flask-cors', 'graphviz', 'snowballstemmer']

    for package in packages:
        # Attempts to import the module; if it can not, that means it is not installed.
        try:
            if package == "flask-cors":
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

if __name__ == "__main__":
    main()