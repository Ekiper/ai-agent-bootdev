import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_path_workdir = os.path.abspath(working_directory)
    abs_path=os.path.abspath(os.path.join(working_directory, directory))
    if not os.path.exists(abs_path):
        return f"The specified directory '{abs_path}' does not exist."
    normalized_path = os.path.normpath(abs_path)
    valid_target_dir = os.path.commonpath([abs_path_workdir, normalized_path]) == abs_path_workdir
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'

    information=""
    for item in os.listdir(abs_path):
        #print(f"item: {item}")
        item_path = os.path.join(abs_path, item)
        information+=(f"- {item} : file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n")

    return information
