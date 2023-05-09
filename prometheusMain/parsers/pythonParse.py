builtInPythonFunctions = ["Python - Built-In", 'abs', 'aiter', 'all', 'any', 'anext', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__']
setFunctions = ["Set (Py) - Built-In", 'frozenset', 'len', 'all', 'any', 'max', 'min', 'sum', 'sorted', 'reversed', 'enumerate', 'zip', 'filter', 'map', 'union', 'intersection', 'difference', 'symmetric_difference', 'copy', 'add', 'remove', 'discard', 'pop', 'clear', 'update', 'intersection_update', 'difference_update', 'symmetric_difference_update', 'isdisjoint', 'issubset', 'issuperset']
listFunctions = ["List (Py) - Built-In", 'append', 'extend', 'insert', 'remove', 'pop', 'clear', 'index', 'count', 'sort', 'reverse', 'copy']
osFunctions = ["OS (Py) - Built-In", 'name', 'path', 'access', 'altsep', 'chdir', 'chmod', 'chown', 'clearenv', 'curdir', 'defpath', 'device_encoding', 'devnull', 'dup', 'dup2', 'environ', 'errno', 'error', 'execl', 'execle', 'execlp', 'execlpe', 'execv', 'execve', 'execvp', 'execvpe', 'extsep', 'fchdir', 'fchmod', 'fchown', 'fdopen', 'fsdecode', 'fsencode', 'fspath', 'fstat', 'fstatvfs', 'fsync', 'ftruncate', 'get_blocking', 'get_exec_path', 'get_handle_inheritable', 'get_inheritable', 'get_terminal_size', 'getcwd', 'getcwdb', 'getenv', 'getlogin', 'getpid', 'getppid', 'isatty', 'kill', 'linesep', 'link', 'listdir', 'lseek', 'lstat', 'makedirs', 'mkdir', 'name', 'nice', 'open', 'pardir', 'path', 'pathconf', 'pathsep', 'pipe', 'popen', 'putenv', 'read', 'readlink', 'remove', 'removedirs', 'rename', 'renames', 'replace', 'rmdir', 'scandir', 'sep', 'set_blocking', 'set_handle_inheritable', 'set_inheritable', 'spawnl', 'spawnle', 'spawnlp', 'spawnlpe', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe', 'stat', 'stat_float_times', 'stat_result', 'statvfs', 'statvfs_result', 'strerror', 'supports_bytes_environ', 'supports_dir_fd', 'supports_effective_ids', 'supports_fd', 'supports_follow_symlinks', 'symlink', 'sys', 'system', 'tcgetpgrp', 'tcsetpgrp', 'terminal_size', 'times', 'times_result', 'truncate', 'umask', 'uname', 'unlink', 'unsetenv', 'urandom', 'utime', 'waitpid', 'walk', 'write']
tempFileFunctions = ["TempFile (Py) - Built-In", 'mkstemp', 'mkdtemp', 'mktemp', 'NamedTemporaryFile', 'TemporaryDirectory', 'gettempdir', 'gettempprefix', 'template', 'SpooledTemporaryFile']
timeFunctions = ["Time (Py) - Built-In", 'asctime', 'clock', 'ctime', 'daylight', 'gmtime', 'localtime', 'mktime', 'monotonic', 'monotonic_ns', 'perf_counter', 'perf_counter_ns', 'process_time', 'process_time_ns', 'sleep', 'strftime', 'strptime', 'struct_time', 'time', 'time_ns', 'timezone', 'tzname']

allFunctions = [builtInPythonFunctions, setFunctions, listFunctions, osFunctions, tempFileFunctions, timeFunctions]

def pythonParse(file, originalFileName):

    cleanedTables = [[originalFileName]]

    with open(file.name, 'r') as f:
        pythonText = f.read()

    for line in pythonText.split("\n"):
        if "def " in line:
            line = line.strip()
            line = line.split(" ")[1]
            line = line.split("(")[0]

            temp = [[line, "FUNCTION"]]
            cleanedTables.append(temp)

    print(cleanedTables)

    # 0 is the file name, 1 is the first function
    functionNumber = 0
    subFunctionDepth = 0
    for line in pythonText.split("\n"):
        if "(" in line:
            line = line.split("(")[0]
            line = line.split(".")[-1]

            leadingSpaces = 4
            for i in range(subFunctionDepth):
                    leadingSpaces += 4
            
            if len(line) - len(line.lstrip()) < leadingSpaces and subFunctionDepth > 0:
                subFunctionDepth -= 1

            if "def " in line:
                if len(line) - len(line.lstrip()) < leadingSpaces:
                    functionNumber += 1
                else:
                    subFunctionDepth += 1
            else:
                tempLine = line.split(" ")[-1]
                if tempLine != cleanedTables[functionNumber + subFunctionDepth][0] and tempLine != "":
                    added = False
                    for functionType in allFunctions:
                        if tempLine in functionType and not added:
                            cleanedTables[functionNumber + subFunctionDepth].append([tempLine, functionType[0]])
                            added = True
                    
                    if not added:
                        cleanedTables[functionNumber + subFunctionDepth].append([tempLine, "FUNCTION CALL"])

            
            print(line)
            print("Leading whitespace real = ", len(line) - len(line.lstrip()))
            print("Leading spaces check = ", leadingSpaces)
            print("subfunctiondepth =", subFunctionDepth)
            print("function number = ", functionNumber, "\n\n\n")
                        
    return cleanedTables