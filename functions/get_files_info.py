import os  # Import OS module for file system operations
from google.genai import types  # Imports the functions needed for the google ai 

def get_files_info(working_directory:str , directory ="."):
    """
    get_files_info = This function lists all files and folders in a directory
    It shows what's inside a folder - like when you do 'ls' in terminal.
    
    working_directory = The base directory we can't go outside this
    
    Returns a string with all files/folders, their sizes, and whether they're directories or singular files help in the process of that.
    """
    
    # abs_working_directory = Convert to absolute path to get full location for the full path expands on the working directory.
    # This also acts a security purpose as we cannot go outside and just scan a folder named password and get its contents thats bonkers
    
    abs_working_directory = os.path.abspath(working_directory)
    
    abs_directory = ""
    
    # Check if directory parameter is None
    if directory is None:
        # If None just use the working dir like if we cannot get to the absolute directory.
        directory = os.path.abspath(working_directory)
    else:
        # If directory is there , combine it with working dir
        
        # This just joins the normal and absolute path as 1
        abs_directory = os.path.abspath(os.path.join(working_directory , directory))
        
    # .startswith() checks if abs_directory begins with abs_working_directory
    if not abs_directory.startswith(abs_working_directory):
        
        # If trying to escape the normal file it , return error
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # This will contain all the information about file and folders.
    final_response_ai = ""
    
    # os.listdir() gets a list of everything in the current directory
    # This ONLY gives names, not full paths or details just the names of the files.
    contents = os.listdir(abs_directory)
    
    #This is the mane loop which runs for iterations of files and folders there.
    for item in contents:  
        
        # Create full path by joining directory path + item name
        contents_for_path = os.path.join(abs_directory, item)
        
        # Check if this item is a directory (folder) or a file
        # os.path.isdir() returns True if it's a folder, False if it's a file
        is_dir = os.path.isdir(contents_for_path)
        
        # Get the size of the file/folder in bytes
        size = os.path.getsize(contents_for_path) 
        
        # Build a formatted string with all the info and add it to our response
        # This just adds everything and gives us the detail of the files including everything.
        final_response_ai += f" -{contents_for_path} : file_size={size} bytes , is_dir = {is_dir}\n"

    return final_response_ai  


"""This is beyond my knowledge and i cannot fully understand this
this is directly taken from the ai docs used"""
schema_get_files_info = types.FunctionDeclaration(
    # Function name - must match the Python function name exactly as this works only on python file and not on thers
    name="get_files_info",
    
    # Description tells the AI what this function does
    # AI reads this to decide when to use this function
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    
    parameters=types.Schema(
        # Parameters are structured as an OBJECT (by the direction from ChatGpt)
        type=types.Type.OBJECT,
        
        properties={
            "directory": types.Schema(
                # This parameter is a STRING 
                type=types.Type.STRING,
                
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        # NOTE: "directory" is NOT in required=[] because it has a default value (".")
    ),
)