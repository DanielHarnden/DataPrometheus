"""
This module contains the root function that calls all other functions in Data Prometheus.
Each call is handled for errors, which are returned to the frontend GUI.
"""


from time import perf_counter
from parse_files import parse_files
from map_files import map_files
from generate_graph_output import generate_graph_output
from generate_sql_output import generate_sql_output


def process_files(files, operation):
    """
    Checks for errors before calling the other Data Prometheus functions.
    If an error occurs at any time, error message is printed and returned to the frontend GUI.
    """

    # Checks for common errors
    begin_time = perf_counter()
    status, error_message = error_check(files, operation)
    if status == 0:
        return 0, error_message


    # 1) Parse an inputted file for relevant information.
    parsed_text, parsed_inserts = parse_files(files, operation)
    # Error message stored in parsedInserts (if there is an error)
    if parsed_text == 0:
        return 0, parsed_inserts


    # 2) Map the parsed information to itself to find relationships between "keys" and "tables."
    start_time = perf_counter()
    print("Beginning mapping...")
    try:
        key_list, banned_words = map_files(parsed_text)
    except Exception as exception:
        print(exception)
        error_message = (
            "There was an error while mapping the files. "
            "Please make sure that Data Prometheus is in a stable build, "
            "or restart the program and try again."
        )
        return 0, error_message
    print(f"Mapping completed. Time Elapsed: {perf_counter() - start_time} seconds.\n")


    start_time = perf_counter()
    print("Generating GraphViz PNG...")
    error_message = (
        "There was an error while generating the graph output. "
        "Please make sure that Data Prometheus is in a stable build, "
        "or restart the program and try again."
    )
    # 3) (Mapping Only) Generate a visualization of the mapped information using GraphViz.
    if operation == "mapDatabase":
        try:
            generate_graph_output(parsed_text, key_list, banned_words)
        except Exception as exception:
            print(exception)
            return 0, error_message
        print(f"PNG generated. Time Elapsed: {perf_counter() - start_time} seconds.\n")

    # 3) (Merging Only) Generate visualization and SQL file
    elif operation == "mergeDatabase":
        try:
            combined_parsed_text = combine_files(parsed_text)
            edges_to_add = generate_graph_output(combined_parsed_text, key_list, banned_words)
        except Exception as exception:
            print(exception)
            return 0, error_message
        print(f"PNG generated. Time Elapsed: {perf_counter() - start_time} seconds.\n")

        start_time = perf_counter()
        print("Generating SQL file...")

        try:
            generate_sql_output(parsed_text, parsed_inserts, key_list, edges_to_add)
        except Exception as exception:
            print(exception)
            error_message = (
                "There was an error while generating the SQL output. "
                "Please make sure that Data Prometheus is in a stable build, "
                "or restart the program and try again."
            )
            return 0, error_message

        print(f"SQL generated. Time Elapsed: {perf_counter() - start_time} seconds.\n")

    print(f"Total Operational Time: {perf_counter() - begin_time} seconds.\n")
    return 1, "Successful operation."


def error_check(files, operation):
    """
    Checks for common errors that may be encountered when using the frontend GUI.
    """

    if len(files) == 1 and files[0].filename == "":
        error_message = "No file(s) chosen."
        return 0, error_message

    if operation == "mergeDatabase" and len(files) < 2:
        error_message = "Please choose two or more files to merge."
        return 0, error_message

    return 1, "Successful operation."


def combine_files(parsed_text):
    """
    When merging, combines all inputted files into one file named "output.sql".
    This creates a single subgraph when creating the GraphViz DOT image.
    """

    new_parsed_text = [["output.sql"]]
    for file in parsed_text:
        new_parsed_text.extend(file[1:])

    return [new_parsed_text]
