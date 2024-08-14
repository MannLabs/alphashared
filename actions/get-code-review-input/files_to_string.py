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
        if os.path.exists(file_path):
            files_contents.append(f"START FILE '{file_path}' >>>>>>>>\n")
            with open(file_path, "r") as infile:
                files_contents.append(infile.read())
            files_contents.append(f"\n<<<<<<<< END FILE '{file_path}'")
        else:
            print(f"Warning: File not found - {file_path}")

    return "\n\n".join(files_contents)


if __name__ == "__main__":
    file_paths = sys.argv[1].split()
    print(_concatenate_files(file_paths))
