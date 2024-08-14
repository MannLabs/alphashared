"""Dump all files into one file.

Required arguments:
- whitespace-separated list of relative paths of files to dump

Returns
-------
- A string containing all files concatenated.
"""

import os
import sys


def _concatenate_files(file_paths: list[str]) -> str:
    """Concatenate the content of multiple files into a single string."""
    files_contents = []
    for file_path in file_paths:
        if not file_path.startswith("./"):
            file_path = f"./{file_path}"

        if not os.path.exists(file_path):
            print(f"File '{file_path}' does not exist.")
            continue

        if os.path.isfile(file_path):
            files_contents.append(f"START FILE '{file_path}' >>>>>>>>\n")
            with open(file_path, "r") as infile:
                files_contents.append(infile.read())
            files_contents.append(f"\n<<<<<<<< END FILE '{file_path}'")
        else:
            print(f"File '{file_path}' not a file.")

    return "\n\n".join(files_contents)


if __name__ == "__main__":
    file_paths = sys.argv[1].split()
    print(f"Concatenating files: {file_paths}")
    print(_concatenate_files(file_paths))
