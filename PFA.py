#!/usr/bin/python3

import os
import argparse

def find_file_path(file):
    return os.path.realpath(file)

def find_python_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def CodeQualityChecks(python_files):
    if python_files:
        for file in python_files:
            file_path = find_file_path(file)
            if not file_path:
                print(f"File {file} not found.")
                continue

            # Formatting the code
            format_command = f"ruff format {file_path}"
            #print(f"Executing command: {format_command}")
            os.system(format_command)

            # Linting the code
            lint_command = f"ruff check --fix {file_path}"
            #print(f"Executing command: {lint_command}")
            os.system(lint_command)


def main():
    parser = argparse.ArgumentParser(
        description="Linting and formatting Python files in directories or file paths."
    )
    parser.add_argument(
        "paths", nargs="+", help="List of directories or file paths to process"
    )
    parser.add_argument(
        "--cmsswbase", required=True, help="Path for the CMSSW base directory."
    )
    args = parser.parse_args()

    all_python_files = []
    for path in args.paths:
        if os.path.isdir(path):
            all_python_files.extend(find_python_files(path))
        elif os.path.isfile(path):
            all_python_files.append(path)
        else:
            print(f"Error: {path} is not a valid file or directory.")
            return

    CodeQualityChecks(all_python_files)

if __name__ == "__main__":
    main()
