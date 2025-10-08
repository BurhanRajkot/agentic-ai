import os
from google.genai import types

def delete_file(working_directory: str, file_path: str):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot delete "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" does not exist'

    if os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file. Cannot delete directories.'

    try:
        os.remove(abs_file_path)
        return f'Successfully deleted "{file_path}"'
    except Exception as e:
        return f'Error: Failed to delete "{file_path}" - {e}'


schema_delete_file = types.FunctionDeclaration(
    name="delete_file",
    description="Deletes a specified file within the working directory. Safe deletion with security checks.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to delete, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
