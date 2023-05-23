import importlib, webbrowser, subprocess, sys

def main():
    checkForPackages()

    print("Opening GUI in user's web browser...")
    webbrowser.open("http://localhost:8000/")
    
    print("Attempting to start the Flask API...")
    try:
        subprocess.check_call("python .\\prometheusMain\\flask_API.py")
    except:
        print("There was an error starting the Flask API.")
        sys.exit()


# Checks to see if the proper Python packages exist
def checkForPackages():
    print("Determining if the correct Python packages are installed...")

    packages = ['flask', 'flask-cors', 'graphviz', 'snowballstemmer']

    for package in packages:
        try:
            if package == "flask-cors":
                importlib.import_module("flask_cors")
            else:
                importlib.import_module(package)
        except ModuleNotFoundError:
            print(f"{package} is not downloaded on the local machine. Please run requirements.txt or pip install {package}.")
            sys.exit()
            
    print("All packages installed!\n")

if __name__ == "__main__":
    main()