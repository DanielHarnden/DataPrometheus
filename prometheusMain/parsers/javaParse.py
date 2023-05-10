import re

def javaParse(file, originalFileName):

    with open(file.name, 'r') as f:
        javaText = f.read()

    print(javaText)
    

    return 0