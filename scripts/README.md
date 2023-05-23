## Core of Data Prometheus

Below is a visualization of the function interactions of Data Prometheus as mapped by Data Prometheus. 
![Data Prometheus 5/22](https://github.com/DanielHarnden/DataPrometheus/assets/103148290/b8b3095c-1149-4a67-9b9b-6d2d3cc38174)


This directory contains the core code of Data Prometheus. Data Prometheus is structured in a three step process:
1) Parse an inputted file for relevant information.
2) Map the parsed information to itself to find relationships between "keys" and "tables."
3) Generate a visualization of the mapped information using GraphViz.

---

#### Step 0: Running Data Prometheus

runDataPrometheus.py is used to start the Frontend GUI and Flask API servers. This file also ensures that all of the necessary Python packages are installed on the user's system and uses pip to install packages that are missing.
flaskAPI.py is used to connect the Frontend GUI to the greater codebase.
dataPrometheus.py is used to begin the three step process outlined above. The only way to properly use this file (currently) is to call it using the Frontend GUI.

---

#### Step 1: Parsing Inputted Files

The subdirectory "parsers" holds the Python files that parse the inputted files. Different file types require different parsing logic, though the parsing functions all return a standardized input that is detailed in the parsers subdirectory README.

---

#### Step 2: Mapping Inputted Files

mapText.py is used to map the parsed input. The mapper ignores file and table names, focussing only on whether or not keys are related to each other. The goal of Data Prometheus is to develop a mapping algorithm that is able to identify like keys (e.g. identificationNumber and idNum) and correctly flag them as related so that they are able to be properly graphed. To achieve this, the mapper uses basic artifical intelligence and other methods to determine if keys are related.
Keys (whether or not synonyms or like keys have been found) are stored in the keyInformation subdirectory. Further information on how keys work can be found in the parsers subdirectory README.

---

#### Step 3: Generate a Visualization

Using the parsing and mapping information, generateGraph.py has enough information to recreate the inputted files' file structure in the form of GraphViz nodes, subgraphs, and edges. Files are created as subgraphs, which contain all of the nodes generated for each file. Each node represents a "table" (this can be a table from a database file, or a function from a programming language file) and "keys" (this can be a key from a database file, or a function call from a programming language file). Relationships between keys are found, marked, and mapped both between nodes within the current subgraph and nodes in other subgraphs (files) as edges between nodes.

Once every node, subgraph, and edge are found, the output is saved as a GraphViz dot file and a PNG of that dot file is generated. Both are stored in the output directory (in the base DataPrometheus directory). The GUI is then updated with the newly generated image.
