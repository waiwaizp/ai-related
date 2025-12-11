import os
from pathlib import Path
base_dir = Path(f"{os.path.dirname(__file__)}/test")

def list_files() -> list[str]:
    """
    List all files in the given directory.

    :param directory: Path to the directory
    :return: List of file names
    """
    try:
        return [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    except FileNotFoundError:
        print(f"Error: Directory '{base_dir}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to access '{base_dir}'.")
        return []

def rename_file(old_name, new_name):
    """
    Rename a file from old_name to new_name.

    :param old_name: Current file name
    :param new_name: New file name
    """
    try:
        os.rename(base_dir / old_name, base_dir / new_name)
        return f"File renamed from '{old_name}' to '{new_name}'."
    except FileNotFoundError:
        return f"Error: File '{old_name}' not found."
    except FileExistsError:
        return f"Error: File '{new_name}' already exists."
    except PermissionError:
        return f"Error: Permission denied to rename '{old_name}'."

def read_file(name) -> str:
    """
    Read the contents of a file.

    :param file_path: Path to the file
    :return: Contents of the file as a string
    """
    try:
        with open(base_dir / name, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{name}' not found.")
        return ""
    except PermissionError:
        print(f"Error: Permission denied to read '{name}'.")
        return ""
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{name}'.")
        return ""