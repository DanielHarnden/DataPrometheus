# Data Prometheus

Data Prometheus is a tool that facilitates the discovery and visualization of implicit relationships within databases. By generating clear and intuitive image representations of the mapped databases, Data Prometheus aids in comprehending complex data models.

In addition to its database analysis capabilities, Data Prometheus can also map relationships between functions and files in Python and Java. This feature enables developers to gain a better understanding of the organization and dependencies within the codebase.

# Demo

An example of Data Prometheus mapping several databases and Python files:

![Data Prometheus Mapping Example](/documentation/mapExample.mp4)

An example of Data Prometheus merging several databases, and the SQL output generated:

![Data Prometheus Merging Example](/documentation/mergeExample.mp4)

---

# Before Running...

Ensure you have [Python](https://www.python.org/downloads/) and [Graphviz](https://graphviz.org/download/) installed and in your PATH.

# Running Data Prometheus

Double click on runDataPrometheus.bat. Two command prompts will open (one for hosting the HTML GUI with Python, the other to host the Flask API) and only contain debugging information. Once the Python server and API are running, the main menu of Data Prometheus will open in your browser.

# Stopping Data Prometheus

Simply close the command prompts.

# Finding Generated Files

Data Prometheus saves all output to the output folder. Currently, only one image and Graphviz dot document are stored at a time. Or just save them from the GUI.