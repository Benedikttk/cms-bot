#!/usr/bin/python3

import os
import argparse


# Function to get the absolute path of a file
def find_file_path(file):
    return os.path.realpath(file)


# Function to search for .py files in a given directory
def find_python_files(directory):
    """Searches for all .py files in a given directory"""
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


# Code quality checker
def CodeQualityChecks(python_files, cmsswbase, output_file):
    if python_files:
        with open(output_file, "w") as out_file:
            for file in python_files:
                # Find the full path of the file
                file_path = find_file_path(file)
                if not file_path:
                    print(f"File {file} not found.")
                    continue

                # Formatting the code
                format_command = f"ruff format {file_path}"
                codeformating = os.system(format_command)

                # Linting the code
                lint_command = f"ruff check --fix {file_path}"
                codelinting = os.system(lint_command)

                # Git diff of quality checked code online and offline
                gitdiff_command = (
                    f"pushd {cmsswbase} > /dev/null && git diff && popd > /dev/null"
                )
                gitdiff_output = os.popen(gitdiff_command).read()

                # Write results to the output file
                out_file.write(f"Git Diff:\n{gitdiff_output}\n")
                out_file.write("\n")


# Main function to parse arguments and call other functions
def main():
    parser = argparse.ArgumentParser(
        description="Linting and formatting Python files in directories or file paths."
    )
    parser.add_argument(
        "paths", nargs="+", help="List of directories or file paths to process"
    )
    parser.add_argument(
        "--outputfile",
        required=True,
        help="Path to the output file.",
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

    CodeQualityChecks(all_python_files, args.cmsswbase, args.outputfile)


# Entry point of the script
if __name__ == "__main__":
    main()
