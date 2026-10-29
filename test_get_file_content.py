import os
from functions.get_file_content import get_file_content
from config import MAX_CHARS_READ

testCases=[
    ("calculator", "lorem.txt"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py"),
    ("calculator", "main.py"),]

def main():

    for working_directory, file_path in testCases:
        result = get_file_content(working_directory, file_path)
        print(f"{file_path} length: {len(result)}")
        print(f"{file_path} truncated: {'truncated' in result}")
        if len(result) < MAX_CHARS_READ:
            print(f"{file_path} content: {result}")
        print()

if __name__ == "__main__":
    main()