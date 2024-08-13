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
        print("Error reading {1}: {2}".format(input_file, e))
        return

    # Run PFA.py for linting and formatting
    pfa_command = (
        "python ../../cms-bot/PFA.py "
        + " ".join(files_list)
        + " --cmsswbase {}".format(cmssw_base)
    )
    result = os.system(pfa_command)

    if result == 0:
        print("Successfully processed files.")
    else:
        print("An error occurred while running PFA.py. Exit code: {}".format(result))

if __name__ == "__main__":
    main()
