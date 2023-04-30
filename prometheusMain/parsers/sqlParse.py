import sqlparse, re

def sqlParse(file):

    with open(file.name, 'r') as f:
        sql_text = f.read()

    # parse SQL into statement list
    statements = sqlparse.parse(sql_text)

    cols = []
    for statement in statements:
        statement = str(statement)

        if "INSERT INTO" in statement:
            splitStatement = statement.split("INSERT INTO")

            styleOne = r"`(.*?)`"
            styleTwo = r"\[(.*?)\]"

            for insert in splitStatement:
                resultsOne = re.findall(styleOne, insert)
                resultsTwo = re.findall(styleTwo, insert)
                results = resultsOne + resultsTwo

                if results != [] and len(results) > 1:
                    cols.append(results)
        elif "TABLE" in statement:
            print(statement)
            results = re.findall(r"(.*?)\s", statement)
            print(results)

            if results != [] and len(results) > 1:
                cols.append(results)


    print(cols)
    return cols