"""
This module is used to determine which parser to call when given a list of files.
Each file is then send to its appropriate parser, regardless of the types of
the other files.
"""


from os import unlink
from tempfile import NamedTemporaryFile
from time import perf_counter
from parsers.sqliteParse import sqliteParse, sqliteInsertParse
from parsers.sqlParse import sqlParse, sqlInsertParse
from parsers.pythonParse import pythonParse
from parsers.javaParse import javaParse


# The name of the parser function and insert statement parser.
sqlite = [sqliteParse, sqliteInsertParse,
          # The file extensions those parsers support.
          "db", "db3", "s3db", "sqlite", "sqlite3", "sqlitedb", "sl3"]
sql = [sqlParse, sqlInsertParse,
       "sql"]
py = [pythonParse, None,
      "py"]
java = [javaParse, None,
        "java"]

# A list containing the previous lists (for streamlining)
supportedFileTypes = [sqlite, sql, py, java]
supportedMergeFileTypes = [sqlite, sql]



def parse_files(files, operation):
    """
    Goes through each file individually and sends it to its appropriate parser.
    Appends the parser's (standardized) output to a list.
    If the user is merging databases, insert statements are also added to a list.
    Once all the files are parsed, the lists is returned.
    """

    parsed_text = []
    parsed_inserts = []

    # Determine which file types are supported based on the current operation
    file_types = []
    if operation == "mapDatabase":
        file_types = supportedFileTypes
    elif operation == "mergeDatabase":
        file_types = supportedMergeFileTypes      

    for i, file in enumerate(files):
        # Generates a temporary file to send to the parser
        temp_file = NamedTemporaryFile(delete=False)
        file.save(temp_file.name)
        extension = determine_file_type(file.filename)
        parsing_function = None
        insert_parsing_function = None

        # Chooses the appropriate parser
        for type_list in file_types:
            if extension in type_list:
                parsing_function = type_list[0]
                insert_parsing_function = type_list[1]
                break

        # Returns an error if there is no parser
        if parsing_function is None:
            if operation == "mapDatabase":
                error_message = (
                    f"Files of extension .{extension} are not currently supported "
                    "by Data Prometheus's mapping function."
                )
            elif operation == "mergeDatabase":
                error_message = (
                    f"Files of extension .{extension} are not currently supported "
                    "by Data Prometheus's database merging function. "
                    "If you want to view a graph visualization of this file, "
                    "please try Data Prometheus's mapper."
                )
            else:
                error_message = "Operation not defined."
            return 0, error_message

        start_time = perf_counter()
        print(f"Beginning parse {i+1} of {len(files)}...")

        try:
            parsed_text.append(parsing_function(temp_file, file.filename))
        except Exception as exception:
            print(exception)
            error_message = (
                f"There was an error parsing {file.filename}. "
                f"Please make sure that the file is a valid {extension} file "
                "or that Data Prometheus is in a stable build."
            )
            return 0, error_message

        # Add the insert statements (if merging)
        if operation == "mergeDatabase" and insert_parsing_function is not None:
            parsed_inserts.append(insert_parsing_function(temp_file))

        # Deletes the temporary file
        temp_file.close()
        unlink(temp_file.name)
        print(f"Parse {i+1} completed. Time Elapsed: {perf_counter() - start_time} seconds.\n")

    return parsed_text, parsed_inserts



def determine_file_type(file_name):
    """
    Determines the file type given a file name in the format "fileName.fileType".
    """

    if "." not in file_name:
        return ""
    extension = file_name.split(".")[-1]
    return extension
