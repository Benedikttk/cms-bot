#!/usr/bin/python3

import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run Python formatting and linting.")
    parser.add_argument(
        "--inputfile",
        required=True,
        help="Path to the file containing the list of files to process.",
    )
    parser.add_argument(
        "--cmsswbase",
        required=True,
        help="Path to the CMSSW base directory.",
    )

    args = parser.parse_args()

    input_file = args.inputfile
    cmssw_base = args.cmsswbase

    if not os.path.isfile(input_file):
        print("Error: {} does not exist.".format(input_file))
        return

    try:
        with open(input_file, "r") as file:
            files_list = [
                os.path.join(cmssw_base, line.strip()) for line in file if line.strip()
            ]
    except IOError as e:
        print("Error reading {}: {}".format(input_file, e))
        return

    # Run Python code formatting
    pfa_command = (
        "python3 ../cms-bot/PFA.py "
        + " ".join(files_list)
        + " --cmsswbase {}".format(cmssw_base)
    )

    print("Command: ", pfa_command)
    os.system("echo $(pwd)")
    os.system("exit 0")
    result = os.system(pfa_command)

    if result == 0:
        print("Successfully formatted files.")
    else:
        print("An error occurred while running PFA.py. Exit code: {}".format(result))

    # Run linting with ruff
    with open("python-linting.txt", "w") as linting_output:
        for file in files_list:
            if os.path.isfile(file):
                linting_output.write("Checking {}\n".format(file))
                check_command = "ruff check {}".format(file)
                result = os.system(check_command)
                if result != 0:
                    linting_output.write("Error checking file {}: Exit code {}\n".format(file, result))

    print("Python linting completed. Check 'python-linting.txt' for details.")

if __name__ == "__main__":
    main()
