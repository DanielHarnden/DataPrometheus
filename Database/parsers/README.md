# The parsers in this folder should return a list of lists in the following format:
```
[ ["tableOneName", "key1", "key2", ... "keyN"], ["tableTwoName", "key1", "key2", ... "keyN"], ... ["tableNName", "key1", "key2", ... "keyN"] ]
```

# VERY IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### Keys are saved in the format:
```
{key: [value1, value2, value3]}
```
### If a value is paired to a key, it will be REPLACED by the key when generating the graph, so:
```
idNum: {idNum, badgeNumber, idNumber, identificationNum}
```

### All 4 values (idNum, badgeNumber, idNumber, identificationNum) will be replaced with idNum when graphed