"""Dump all files into one file.

Required arguments:
- whitespace-separated list of relative paths of files to dump

Returns
-------
- A string containing all files concatenated.
"""

import os
import sys


def _concatenate_files(file_paths: list[str], excluded_extensions: list[str]) -> str:
    """Concatenate the content of multiple files into a single string."""
    file_contents = []
    for file_path in file_paths:
        if not file_path.strip():
            continue

        if any(file_path.endswith(ext) for ext in excluded_extensions):
            print(f"Skipping file '{file_path}' because it has an excluded extension.")
            continue

        print(f"Processing file: {file_path}")

        if not file_path.startswith("./"):
            file_path = f"./{file_path}"

        if not os.path.exists(file_path):
            print(f"File '{file_path}' does not exist.")
            continue

        if os.path.isfile(file_path):
            try:
                with open(file_path, "r") as infile:
                    file_content = infile.read()
            except UnicodeDecodeError as e:
                print(f"Error reading file '{file_path}': {e}")
                continue

            file_contents.append(f"START FILE '{file_path}' >>>>>>>>>>>>>>>>\n")
            file_contents.append(file_content)
            file_contents.append(f"\n<<<<<<<<<<<<<<<< END FILE '{file_path}'")

    print(f"Got {len(file_contents)} lines..")
    return "\n\n".join(file_contents)


if __name__ == "__main__":
    file_paths = sys.argv[1].split(";") if ";" in sys.argv[1] else sys.argv[1].split()
    output_path = sys.argv[2]
    excluded_extensions = sys.argv[3].split(";") if len(sys.argv) > 3 else []

    print(f"Concatenating {file_paths=} with {excluded_extensions=}")
    concatenated_string = _concatenate_files(file_paths, excluded_extensions)

    with open(output_path, "w") as outfile:
        print(
            f"Writing concatenated content of length {len(concatenated_string)} to '{output_path}' .."
        )
        outfile.write(concatenated_string)
    print("Done.")
