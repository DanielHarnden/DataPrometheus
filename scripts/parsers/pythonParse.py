# TODO: Optimize how this works
builtInPythonFunctions = ["Python - Built-In", 'abs', 'aiter', 'all', 'any', 'anext', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__']
setFunctions = ["Set (Py) - Built-In", 'frozenset', 'len', 'all', 'any', 'max', 'min', 'sum', 'sorted', 'reversed', 'enumerate', 'zip', 'filter', 'map', 'union', 'intersection', 'difference', 'symmetric_difference', 'copy', 'add', 'remove', 'discard', 'pop', 'clear', 'update', 'intersection_update', 'difference_update', 'symmetric_difference_update', 'isdisjoint', 'issubset', 'issuperset']
listFunctions = ["List (Py) - Built-In", 'append', 'extend', 'insert', 'remove', 'pop', 'clear', 'index', 'count', 'sort', 'reverse', 'copy']
osFunctions = ["OS (Py) - Built-In", 'name', 'path', 'access', 'altsep', 'chdir', 'chmod', 'chown', 'clearenv', 'curdir', 'defpath', 'device_encoding', 'devnull', 'dup', 'dup2', 'environ', 'errno', 'error', 'execl', 'execle', 'execlp', 'execlpe', 'execv', 'execve', 'execvp', 'execvpe', 'extsep', 'fchdir', 'fchmod', 'fchown', 'fdopen', 'fsdecode', 'fsencode', 'fspath', 'fstat', 'fstatvfs', 'fsync', 'ftruncate', 'get_blocking', 'get_exec_path', 'get_handle_inheritable', 'get_inheritable', 'get_terminal_size', 'getcwd', 'getcwdb', 'getenv', 'getlogin', 'getpid', 'getppid', 'isatty', 'kill', 'linesep', 'link', 'listdir', 'lseek', 'lstat', 'makedirs', 'mkdir', 'name', 'nice', 'open', 'pardir', 'path', 'pathconf', 'pathsep', 'pipe', 'popen', 'putenv', 'read', 'readlink', 'remove', 'removedirs', 'rename', 'renames', 'replace', 'rmdir', 'scandir', 'sep', 'set_blocking', 'set_handle_inheritable', 'set_inheritable', 'spawnl', 'spawnle', 'spawnlp', 'spawnlpe', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe', 'stat', 'stat_float_times', 'stat_result', 'statvfs', 'statvfs_result', 'strerror', 'supports_bytes_environ', 'supports_dir_fd', 'supports_effective_ids', 'supports_fd', 'supports_follow_symlinks', 'symlink', 'sys', 'system', 'tcgetpgrp', 'tcsetpgrp', 'terminal_size', 'times', 'times_result', 'truncate', 'umask', 'uname', 'unlink', 'unsetenv', 'urandom', 'utime', 'waitpid', 'walk', 'write']
tempFileFunctions = ["TempFile (Py) - Built-In", 'mkstemp', 'mkdtemp', 'mktemp', 'NamedTemporaryFile', 'TemporaryDirectory', 'gettempdir', 'gettempprefix', 'template', 'SpooledTemporaryFile']
timeFunctions = ["Time (Py) - Built-In", 'asctime', 'clock', 'ctime', 'daylight', 'gmtime', 'localtime', 'mktime', 'monotonic', 'monotonic_ns', 'perf_counter', 'perf_counter_ns', 'process_time', 'process_time_ns', 'sleep', 'strftime', 'strptime', 'struct_time', 'time', 'time_ns', 'timezone', 'tzname']
stringFunctions = ["String (Py) - Built-In", "capitalize", "casefold", "center", "count", "encode", "endswith", "expandtabs", "find", "format", "format_map", "index", "isalnum", "isalpha", "isascii", "isdecimal", "isdigit", "isidentifier", "islower", "isnumeric", "isprintable", "isspace", "istitle", "isupper", "join", "ljust", "lower", "lstrip", "maketrans", "partition", "replace", "rfind", "rindex", "rjust", "rpartition", "rsplit", "rstrip", "split", "splitlines", "startswith", "strip", "swapcase", "title", "translate", "upper", "zfill"]
flask_functions = ["Flask (Py) - Built-In", "abort", "after_this_request", "appcontext_popped", "appcontext_pushed", "appcontext_tearing_down", "before_render_template", "before_request", "before_this_request", "blueprints", "command", "script_info_option", "with_appcontext", "with_click_context", "with_command_context", "with_context", "with_filecontext", "with_appcontext", "with_click_context", "with_command_context", "with_context", "with_filecontext", "with_flask_context", "with_ignore_defaults", "with_nested_commands", "with_options", "without_options", "without_parent_args", "Config", "ConfigAttribute", "ConfigError", "ConfigValueMissing", "Configurable", "has_app_context", "has_request_context", "copy_current_request_context", "current_app", "escape", "flash", "get_debug_flag", "get_flashed_messages", "globals", "has_app_context", "has_request_context", "_PackageBoundObject", "find_package", "get_env", "get_debug_flag", "get_flashed_messages", "locked_cached_property", "url_for", "safe_join", "send_file", "get_root_path", "get_package_path", "find_package", "get_env", "get_debug_flag", "get_flashed_messages", "jsonify", "make_response", "request", "send_file", "send_from_directory", "session", "stream_with_context", "url_for", "url_parse", "url_quote", "url_unquote", "url_unquote_plus", "Request", "Response", "SessionMixin", "ResponseStream", "BaseResponse", "ResponseReturnValueMixin"]


allFunctions = [builtInPythonFunctions, setFunctions, listFunctions, osFunctions, tempFileFunctions, timeFunctions, stringFunctions]

import ast

def processNode(node, cleanedTables, currentClass=None, currentFunction=None):

    # Determines if node is a class
    if isinstance(node, ast.ClassDef):
        currentClass = node.name

        # Continue to next child
        for child_node in node.body:
            processNode(child_node, cleanedTables, currentClass)
    
    # Determines if node is a function definition
    elif isinstance(node, ast.FunctionDef):
        functionName = node.name

        if currentClass is not None:
            functionName = currentClass + '.' + functionName

        currentFunction = functionName
        cleanedTables.append([[currentFunction, "FUNCTION"]])

        # Continue to next child
        for child_node in node.body:
            processNode(child_node, cleanedTables, currentClass, currentFunction)

    # Determines if node is a function call
    elif isinstance(node, ast.Call):

        if currentFunction is not None:
            currentCall = ''

            # Call can either be an attribute or a name
            if isinstance(node.func, ast.Name):
                currentCall = node.func.id
            elif isinstance(node.func, ast.Attribute):
                currentCall = node.func.attr

            # Iterates backwards until it finds the correct function to append call to
            for i, function in enumerate(cleanedTables):
                if cleanedTables and cleanedTables[-i][0][0] == currentFunction:

                    for functionType in allFunctions:
                        if currentCall in functionType:
                            cleanedTables[-i].append([currentCall, functionType[0]])
                            break
                    else:
                        cleanedTables[-i].append([currentCall, "FUNCTION CALL"])

    # If node is none of the above, continue to next child
    else:
        for child_node in ast.iter_child_nodes(node):
            processNode(child_node, cleanedTables, currentClass, currentFunction)

def pythonParse(file, originalFileName):

    cleanedTables = [[originalFileName]]

    with open(file.name, 'r') as f:
        tree = ast.parse(f.read())

    processNode(tree, cleanedTables)

    return cleanedTables