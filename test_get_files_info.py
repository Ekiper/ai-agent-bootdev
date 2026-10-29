import os
from functions.get_files_info import get_files_info

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

def main():
    print(f"Result for current directory: \n{get_files_info('calculator', '.')}")
    print(f"Result for current directory: \n{get_files_info('calculator', 'pkg')}")
    print(f"Result for current directory: \n{get_files_info('calculator', '/bin')}")
    print(f"Result for current directory: \n{get_files_info('calculator', '../')}")

if __name__ == "__main__":
    main()

