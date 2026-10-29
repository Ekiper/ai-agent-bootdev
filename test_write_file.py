import os
from functions.write_file import write_file

testCases=[
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),]

def main():

    for working_directory, file_path, content in testCases:
        result = write_file(working_directory, file_path, content)
        print(result)
        print()

if __name__ == "__main__":
    main()