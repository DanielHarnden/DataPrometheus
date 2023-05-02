import sqlite3

#TODO: This code is able to get all data stored in the database. This information is relevant if we want to retain data and copy them between databases
#for table in tables:
#    table_name = table[0]
#    rows = cur.execute(f"SELECT * FROM {table_name}").fetchall()
#    print(f"Data from {table_name}: {rows}")

def sqlite3Parse(file, originalFileName):

    allTables = []

    #TODO: Handle multiple tables as input
    if True:
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
                tempTable += table
                tempTable += [column[0] for column in cur.description]
                cleanedTables.append(tempTable)

        # Closes the connection and returns the list of cleaned tables
        conn.close()
    
        allTables.append(cleanedTables)

    print(allTables)

    return allTables