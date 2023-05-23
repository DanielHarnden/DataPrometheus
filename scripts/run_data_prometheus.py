"""
This module starts Data Prometheus.
Intended to be run from the runDataPrometheus.bat file in the base directory.
"""


import importlib
import subprocess
import sys
import webbrowser


def main():
    """
    Entry point of Data Prometheus.
    Checks for required packages, opens the GUI, and starts the Flask API.
    """

    check_for_packages()

    print("Opening GUI in user's web browser...")
    webbrowser.open("http://localhost:8000/")

    print("Attempting to start the Flask API...")
    try:
        subprocess.check_call("python .\\scripts\\flask_api.py")
    except subprocess.CalledProcessError:
        print("There was an error starting the Flask API.")
        sys.exit()


def check_for_packages():
    """
    Checks if the required packages are installed (from requirements.txt).
    Throws an error and terminates the program if they are not.
    """

    print("Determining if the correct Python packages are installed...")

    try:
        with open("requirements.txt", "r", encoding="utf-8") as file:
            packages = [line.strip() for line in file.readlines()]
            packages = [line.split("=")[0].strip() for line in packages]
    except FileNotFoundError:
        print("Could not find requirements.txt in base directory.")
        sys.exit()

    for package in packages:
        try:
            if package == "flask-cors":
                importlib.import_module("flask_cors")
            else:
                importlib.import_module(package)
        except ModuleNotFoundError:
            print(
                f"{package} is not downloaded on the local machine. " 
                f"Please run requirements.txt or pip install {package}.")
            sys.exit()

    print("All packages installed!\n")


if __name__ == "__main__":
    main()
