import sqlite3

#TODO: This code is able to get all data stored in the database. This information is relevant if we want to retain data and copy them between databases
#for table in tables:
#    table_name = table[0]
#    rows = cur.execute(f"SELECT * FROM {table_name}").fetchall()
#    print(f"Data from {table_name}: {rows}")

def sqliteParse(file, originalFileName):

    # Connect to the sqlite3 database. file is a FileObject type or something like that, so the .name is necessary 
    conn = sqlite3.connect(file.name)
    cur = conn.cursor()

    # Finds all the tables (with keys!)
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    
    # Stores and cleans the information
    cleanedTables = [[originalFileName]]
    for table in tables:
        # Excludes SQLite system tables
        if not table[0].startswith("sqlite_"):
            tempTable = []
            cur.execute("SELECT * FROM {} LIMIT 0;".format(table[0]))
            tempTable += [[', '.join(table), "TABLE"]]

            # Use PRAGMA statement to retrieve column metadata
            pragmaQuery = "PRAGMA table_info({})".format(table[0])
            pragmaResults = cur.execute(pragmaQuery).fetchall()

            for column in pragmaResults:
                if column[2] != "":
                    tempTable += [[column[1], column[2]]]
                else:
                    tempTable += [[column[1], "NULL"]]
            cleanedTables.append(tempTable)

    # Closes the connection and returns the list of cleaned tables
    conn.close()

    return cleanedTables