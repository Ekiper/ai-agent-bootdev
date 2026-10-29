import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_path_workdir = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.exists(abs_path_workdir):
        return f"Error:The specified working directory '{abs_path_workdir}' does not exist."
        
    normalized_path = os.path.normpath(abs_path)
    valid_target_dir = os.path.commonpath([abs_path_workdir, normalized_path]) == abs_path_workdir
    
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
    if os.path.isdir(normalized_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
        
    try:
        with open(abs_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Writing to file "{file_path}": {str(e)}'