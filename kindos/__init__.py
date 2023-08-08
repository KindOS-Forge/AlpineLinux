import os

def execute_command(cmd: str, ignore_errors: bool = False):
    """ Execute a command and raises exception if it fails """
    print(f"Executing command: {cmd}")
    if os.system(cmd) != 0:
        if ignore_errors:
            return
        raise Exception(f"Failed to execute command:\n {cmd}")