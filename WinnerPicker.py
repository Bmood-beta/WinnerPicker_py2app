import pandas as pd
import openpyxl
import os
from datetime import datetime
import argparse
import sys
from tkinter import Tk, filedialog

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="?", help="Name of the Excel file")
args = parser.parse_args()

# Prompt for the input file name if not provided as a command-line argument
if args.filename is None:
    root = Tk()
    root.withdraw()
    args.filename = filedialog.askopenfilename(title="Select Excel file")

    if not args.filename:
        sys.exit("No input file selected. Exiting...")

print("Selected Input File:", args.filename)

# Reading the dataframe object
df = pd.read_excel(args.filename, dtype=str)

# Debugger 0.001
# Removing unnamed columns from the dataframe
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Choosing a winner
winner = df.sample(n=10)

# Getting time, user, and file information
timestamp = str(datetime.now())
username = os.environ.get("USER")
filename = args.filename

# Adding winner, file, and user information to the chosen winner
winner["USER_NAME"] = username
winner["TIMESTAMP"] = timestamp
winner["FILENAME"] = filename

# Generating the output file name with both date and time
date_time_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Extract the input file directory and filename
input_directory, input_filename = os.path.split(args.filename)

# Construct the output file path
output_file = os.path.join(input_directory, f"output_{date_time_string}.xlsx")

# Creating the output Excel file with combined information
if not os.path.isfile(output_file):
    winner.to_excel(output_file, index=False)
else:
    existing_winner = pd.read_excel(output_file)
    existing_winner = existing_winner.append(winner)
    existing_winner.to_excel(output_file, index=False)

# Removing the winner from the original file
res = df[df['SBL_ID'].isin(winner['SBL_ID']) == False]

# Writing the modified original file back without the winner
res.to_excel(args.filename, index=False)
