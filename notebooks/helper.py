import inspect

def logger(comment):
    # Getting the previous frame in the stack
    frame = inspect.currentframe().f_back
    # Extracting the name of the function from where logger is called
    function_name = frame.f_code.co_name

    # Use "MAIN" if the function name is "<module>", indicating the main script
    if function_name == "<module>":
        function_name = "MAIN"

    print(f"[{function_name}]: {comment}")