builtInPythonFunctions = ['abs', 'aiter', 'all', 'any', 'anext', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__']

setFunctions = ['frozenset', 'len', 'all', 'any', 'max', 'min', 'sum', 'sorted', 'reversed', 'enumerate', 'zip', 'filter', 'map', 'union', 'intersection', 'difference', 'symmetric_difference', 'copy', 'add', 'remove', 'discard', 'pop', 'clear', 'update', 'intersection_update', 'difference_update', 'symmetric_difference_update', 'isdisjoint', 'issubset', 'issuperset']

listFunctions = ['append', 'extend', 'insert', 'remove', 'pop', 'clear', 'index', 'count', 'sort', 'reverse', 'copy']

osFunctions = ['name', 'path', 'access', 'altsep', 'chdir', 'chmod', 'chown', 'clearenv', 'curdir', 'defpath', 'device_encoding', 'devnull', 'dup', 'dup2', 'environ', 'errno', 'error', 'execl', 'execle', 'execlp', 'execlpe', 'execv', 'execve', 'execvp', 'execvpe', 'extsep', 'fchdir', 'fchmod', 'fchown', 'fdopen', 'fsdecode', 'fsencode', 'fspath', 'fstat', 'fstatvfs', 'fsync', 'ftruncate', 'get_blocking', 'get_exec_path', 'get_handle_inheritable', 'get_inheritable', 'get_terminal_size', 'getcwd', 'getcwdb', 'getenv', 'getlogin', 'getpid', 'getppid', 'isatty', 'kill', 'linesep', 'link', 'listdir', 'lseek', 'lstat', 'makedirs', 'mkdir', 'name', 'nice', 'open', 'pardir', 'path', 'pathconf', 'pathsep', 'pipe', 'popen', 'putenv', 'read', 'readlink', 'remove', 'removedirs', 'rename', 'renames', 'replace', 'rmdir', 'scandir', 'sep', 'set_blocking', 'set_handle_inheritable', 'set_inheritable', 'spawnl', 'spawnle', 'spawnlp', 'spawnlpe', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe', 'stat', 'stat_float_times', 'stat_result', 'statvfs', 'statvfs_result', 'strerror', 'supports_bytes_environ', 'supports_dir_fd', 'supports_effective_ids', 'supports_fd', 'supports_follow_symlinks', 'symlink', 'sys', 'system', 'tcgetpgrp', 'tcsetpgrp', 'terminal_size', 'times', 'times_result', 'truncate', 'umask', 'uname', 'unlink', 'unsetenv', 'urandom', 'utime', 'waitpid', 'walk', 'write']

tempFileFunctions = ['mkstemp', 'mkdtemp', 'mktemp', 'NamedTemporaryFile', 'TemporaryDirectory', 'gettempdir', 'gettempprefix', 'template', 'SpooledTemporaryFile']

timeFunctions = ['asctime', 'clock', 'ctime', 'daylight', 'gmtime', 'localtime', 'mktime', 'monotonic', 'monotonic_ns', 'perf_counter', 'perf_counter_ns', 'process_time', 'process_time_ns', 'sleep', 'strftime', 'strptime', 'struct_time', 'time', 'time_ns', 'timezone', 'tzname']



def pythonParse(file, originalFileName):

    cleanedTables = [[originalFileName]]

    with open(file.name, 'r') as f:
        pythonText = f.read()

    for line in pythonText.split("\n"):
        if "def " in line:
            line = line.split(" ")[1]
            line = line.split("(")[0]

            temp = [[line, "FUNCTION"]]
            cleanedTables.append(temp)


    i = 0
    for line in pythonText.split("\n"):
        if "(" in line:
            line = line.split("(")[0]
            line = line.split(".")[-1]

            if "def " in line:
                i += 1
            else:
                line = line.split(" ")[-1]
                if line != cleanedTables[i][0] and line != "":
                    if line in builtInPythonFunctions:
                        cleanedTables[i].append([line, "Built-In Python Function"])
                    elif line in setFunctions:
                        cleanedTables[i].append([line, "Built-In Python Set Function"])
                    elif line in listFunctions:
                        cleanedTables[i].append([line, "Built-In Python List Function"])
                    elif line in osFunctions:
                        cleanedTables[i].append([line, "Built-In Python OS Function"])
                    elif line in tempFileFunctions:
                        cleanedTables[i].append([line, "Built-In Python TempFile Function"])
                    elif line in tempFileFunctions:
                        cleanedTables[i].append([line, "Built-In Python Time Function"])
                    else:
                        cleanedTables[i].append([line, "FUNCTION CALL"])
                        

    return cleanedTables