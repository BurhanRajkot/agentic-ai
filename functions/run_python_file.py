import os  # Import OS module for handling file system paths and directories.
import subprocess  # Import subprocess to run external commands like executing Python files.
from google.genai import types  # Import the function declaration types for AI schema definition.


def run_python_file(working_directory: str, file_path: str, args = []):
    """
    run_python_file = This function executes a Python (.py) file inside a given working directory
    and returns the output from the stdout and stderr.

    args = Optional List of arguments that are passed to the Python script when executed.

    1 The file stays inside the working dir this is for saftey purpose.
    2 The target file exists and is actually a Python file only this doesnot run react,js or any other file.
    3 Captures the output and the errors that occur during the execution.
    """

    # abs_working_directory this is the absolute path.
    abs_working_directory = os.path.abspath(working_directory)
    
    # abs_file_path = Combine working dir and the file path.
    # os.path.join() automatically handles slashes for Linux, macOS, and Windows.
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        
        # If  outside  we reject it immediately and return an error.
        return f'Error: Cannot list "{file_path}" as it is outside the working directory dipshit'
    
    # Verify if the path provided actually points to a FILE and not a directory.
    # os.path.isfile() returns true if its only a file and not a dir.
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file dumbass'
    
    # This avoids accidentally running or executing system files like system 32 or deletion or making of such files.
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a python file'
    
    try:
        # final_args = The full command list that will be passed to subprocess.
        final_args = ["python3", file_path]
        
        # If additional arguments are provided, extend the list to include them instead of a try cath or giving any errors.
        final_args.extend(args)
        
        # cwd = current working directory
        # timeout = 30 sec helps to stop infinite loop
        output = subprocess.run(
            final_args, cwd=abs_working_directory, timeout=30, capture_output=True, text=True
        )
        
        # Combine both standard output and error into a final string for return.
        final_String = f"""
STDOUT:{output.stdout}
STDERR:{output.stderr}
    """
        
        # If both stdout and stderr are empty, that means script didn’t produce any output.
        if output.stdout == "" and output.stderr == "":
            final_String = "No output produced."
        
        # If the process returned a non-zero exit code, it means there was an error.
        # Add this info at the end for clarity.
        if output.returncode != 0:
            final_String += f"process exited with code {output.returncode}"
        
        # Return the full string containing all executed files.
        return final_String
        
    # Catch exceptions such as file missing, permission denied, timeout, etc.
    except Exception as e:
        # Return the error with message details for debugging.
        return f'error: executing the Python file {e}'
    


"""This is beyond my knowledge and directly taken from AI documentation used."""
schema_run_python_file = types.FunctionDeclaration(
    # Function name — must exactly match the function above for proper tool linkage.
    name="run_python_file",
    
    # Description — Tells the AI what this function actually does.
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    
    # Parameters — Defines what inputs the AI can provide.
    parameters=types.Schema(
        type=types.Type.OBJECT,
        
        # Each property defines one input argument for the function.
        properties={
            # file_path — The main Python file to be executed.
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            
            # args — Optional command-line arguments passed to the script.
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        
        # file_path is mandatory since without it, nothing can be executed.
        required=["file_path"],
    ),
)
