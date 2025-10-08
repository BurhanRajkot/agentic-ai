import os  # Import OS module for handling file system operations and directory paths.
from google.genai import types  # Import the function declaration types for AI schema definition.


def write_file(working_directory, file_path, content):
    """
    write_file = This function writes content to a file inside the given working directory.
    If the file or parent directory does n0t exist, it creates them automatically.

    working_directory = The main directory where files are to be managed or created.
    file_path = The specific file inside the working directory to which data is written.
    content = The text content or data to be written into the file.

    1 Ensures the file is inside the working directory for safety.
    2 Automatically creates any missing parent folders before writing.
    3 Writes the content and returns a success message with character count.
    """

    # abs_working_directory this converts the working dir to absolute path.
    abs_working_directory = os.path.abspath(working_directory)
    
    # abs_file_path = Joins the working dir and the file path into one absolute file location.
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Security check: ensures we are not escaping outside the working directory.
    # Example: trying to write to "../../../etc/passwd" will be blocked.
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    # If the file path doesn’t exist yet, create its parent directory.
    # os.path.dirname() gets the parent directory of the file.
    if not os.path.exists(abs_file_path):
        parent_dir = os.path.dirname(abs_file_path)
        try:
            # os.makedirs() creates missing directories.
            # exist_ok=True means it won’t raise error if the folder already exists.
            os.makedirs(parent_dir, exist_ok=True)
        except Exception as e:
            # If directory creation fails, return an error with the reason.
            return f"could not create parent dir: {parent_dir} - {e}"
    
    # Check if the given path is actually a directory instead of a file.
    # We cannot write content to a directory.
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    # Try writing to the file safely with error handling.
    try:
        # Open the file in write mode, this will create or overwrite the file.
        with open(abs_file_path, "w") as f:
            f.write(content)
            
        # Return a success message along with how many characters were written.
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    # Catch any exception during file writing and return error details.
    except Exception as e:
        return f"failed to write the given line : {file_path} , {e}"
    


"""This is beyond my knowledge and directly taken from AI documentation used."""
schema_write_file = types.FunctionDeclaration(
    # Function name — must exactly match the function above for proper AI linkage.
    name="write_file",
    
    # Description — Tells the AI what this function actually does.
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    
    # Parameters — Defines what the AI can provide to this function.
    parameters=types.Schema(
        type=types.Type.OBJECT,
        
        # Each property is one of the function's arguments.
        properties={
            # file_path — The file to which content will be written.
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            
            # content — The actual text or data to be written.
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        
        # Required arguments that must be provided.
        required=["file_path", "content"],
    ),
)
