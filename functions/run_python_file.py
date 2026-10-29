import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_workdir = os.path.abspath(working_directory)
        abs_filepath = os.path.abspath(os.path.join(working_directory, file_path))
        normalized_filepath = os.path.normpath(abs_filepath)

        # 4. Check if outside working directory
        if os.path.commonpath([abs_workdir, normalized_filepath]) != abs_workdir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 7. Check if it exists and is a regular file
        if not os.path.isfile(abs_filepath):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # 10. Check if it ends with .py
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # 13 & 14. Build command
        command = ["python", abs_filepath]
        
        # 16. Add args if any
        if args:
            command.extend(args)

        # 17. Run subprocess
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 18. Build output string
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr.strip()}")

        # 19. Return output string
        return "\n\n".join(output_parts).strip()

    except Exception as e:
        # 20 & 21. Catch exceptions
        return f"Error: executing Python file: {e}"