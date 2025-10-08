import os  # Import OS module for file system operations
from config import MAX_CHARS  # Import the maximum character limit for file reading it acts as a base for programs that are infinite it stops helps.
from google.genai import types  # Imports the functions needed for the google ai 

def get_file_content(working_directory, file_path): 
    """
    get_file_content = This is the function created to get the content of the file content not the dir but the content present inside.
    Reads and returns the content of the working directory.
    working_directory =  The base directory
    file_path = The path to the file to read of the working or other directory.
    if MAX_CHAR are used and more then it gives error by try and catch method
    """
    
    # abs_working_directory = Convert working_directory to an absolute path for insertion in the file 
    # Abs helps us to get the full file path which helps to locate the file
    abs_working_directory = os.path.abspath(working_directory)
    
    # Combining the os.path with the working dir to get the absolute path fir we get that then here we join it.
    # os.path.join() = Helps to combine it with keeping in mind the slashes used in linux/win/mac all these structures.
    # Example = burhan + burhan/rajkot/clg.apk = burhan/rajkot/pkg.apk/files
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Checks if it is a working_directory
    # Example attack: file_path = "../etc/passwd" would try to escape the working directory as this is sensitive file
    # .startswith() checks if abs_file_path begins with abs_working_directory as normal directory cannot be accepted
    if not abs_file_path.startswith(abs_working_directory):
        # If the file is outside the working directory, it will not accept and return an error
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory and thus cannot be accessed'
    
    # Check if the path actually points to a FILE not a directory as there can be a folder with many files but this is used as its important to point out a file and use that.
    # os.path.isfile() returns True if it's a file, and not correct if it is a directory this is for file_path for files only.
    if not os.path.isfile(abs_file_path):
        # If it's not a file give an error
        return f'Error: "{file_path}" is not a file dumbass'

    # Initialize an empty string helps to store the content
    file_content_string = ""
    
    # STEP 6: Try to read the file (wrapped in try-except for error handling)
    try:
        # Open the file in read mode ("r" means read-only, text mode)
        # "with" ensures the file is automatically closed even if an error occurs
        with open(abs_file_path, "r") as f:
            # Read up to MAX_CHARS characters from the file
            # .read(MAX_CHARS) reads the specified number of characters and stops
            # This prevents reading gigantic files that could crash the program
            file_content_string = f.read(MAX_CHARS)
            
            # Check if we hit the character limit (file might be longer than MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                # Add a message to indicate the file was truncated
                # This tells the AI that there's more content it didn't see
                file_content_string += (f'[...File "{file_path}" truncated to 10000 char ]')
        
        # If everything worked, return the file content
        return file_content_string 
    
    # Catch any exceptions
    # file does not exist, permission denied, disk error, encoding issues they might occur so this helps in that case
    except Exception as e:
        # Return an error message 
        return f"Exception reading file : {e}"
    
    

# SCHEMA DEFINITION used from the docs this is directly given and used
# This is like a document for the ai which it can understand 

"""This is beyond my knowledge and i cannot fully understand this
this is derectly taken from the ai docs used"""
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    
    # Description is what the ai uses to read the file and then it uses its own knowledge on when what to use
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    
    parameters=types.Schema(
        type=types.Type.OBJECT,
        
        # Define each parameter detail
        properties={
            # Define the "file_path" 
            "file_path": types.Schema(
                type=types.Type.STRING,
                
                # The AI uses this to know what value to pass
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        
        required=["file_path"],
    ),
)