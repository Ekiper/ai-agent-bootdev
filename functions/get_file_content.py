import os
from config import MAX_CHARS_READ

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    abs_path_workdir = os.path.abspath(working_directory)
    abs_path=os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.exists(abs_path):
        return f"The specified file '{abs_path}' does not exist."
    normalized_path = os.path.normpath(abs_path)
    valid_target_dir = os.path.commonpath([abs_path_workdir, normalized_path]) == abs_path_workdir
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_path, 'r') as file:
            content = file.read(MAX_CHARS_READ)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS_READ} characters]'
        return content
    except Exception as e:
        return f'Error: Reading file "{file_path}": {str(e)}'