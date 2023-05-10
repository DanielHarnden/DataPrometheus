# Parsers

Data Prometheus currently supports five file types, listed below in development priority (the higher the item is, the more attention has been paid to it).

1. SQLite
2. Python
3. SQL
4. CPP
5. Java

# The parsers in this folder should return a list of list of strings in the following format:
```
[
    ["fileOneName"],
    [
        ["tableOneName", "tableOneType"],
        ["key1", "key1Type"],
        ["key2", "key2Type"],
        ...
        ["keyN", "keyNType"]
    ],
    [
        ["tableTwoName", "tableTwoType"],
        ["key1", "key1Type"],
        ["key2", "key2Type"],
        ...
        ["keyN", "keyNType"]
    ],
    ...
    [
        ["tableNName", "tableNType"],
        ["key1", "key1Type"],
        ["key2", "key2Type"],
        ...
        ["keyN", "keyNType"]
    ]
]
```
# By this logic, runDataPrometheus.py looks like this:
```
[
    ['runDataPrometheus.py'], 
    [
        ['main', 'FUNCTION'], 
        ['checkForPackages', 'FUNCTION CALL'], 
        ['openFrontend', 'FUNCTION CALL'], 
        ['attemptFlask', 'FUNCTION CALL']
    ], 
    [
        ['checkForPackages', 'FUNCTION'], 
        ['print', 'Python - Built-In'], 
        ['import_module', 'FUNCTION CALL'], 
        ['import_module', 'FUNCTION CALL'], 
        ['import_module', 'FUNCTION CALL'], 
        ['print', 'Python - Built-In'], 
        ['check_call', 'FUNCTION CALL'], 
        ['print', 'Python - Built-In'], 
        ['input', 'Python - Built-In'], 
        ['exit', 'FUNCTION CALL'], 
        ['print', 'Python - Built-In']
    ], 
    [
        ['openFrontend', 'FUNCTION'], 
        ['open', 'Python - Built-In']
    ], 
    [
        ['attemptFlask', 'FUNCTION'], 
        ['print', 'Python - Built-In'], 
        ['check_call', 'FUNCTION CALL'], 
        ['main', 'FUNCTION CALL']
    ]
]
```

# VERY IMPORTANT!
### Keys are saved in the format:
```
{key: [value1, value2, value3]}
```
### If a value is paired to a key, it will be REPLACED by the key when generating the graph, so:
```
idNum: {idNum, badgeNumber, idNumber, identificationNum}
```

### All 4 values (idNum, badgeNumber, idNumber, identificationNum) will be replaced with idNum when graphed