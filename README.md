Automated Pin Configuration Verification Tool
This project provides a set of Python scripts designed to automate pin configuration verification for RH850 F1K MCUs using WinIDEA and the isystem.connect API.
The scripts support processing input data from spreadsheet files (CSV by default) and validating MCU Special Function Registers (SFRs) against expected configurations derived from the hardware manual.

Overview
The workflow is designed to operate on an input file (CSV by default), extract the relevant pin configuration data, connect to an active WinIDEA debug session, and verify that each pin is correctly configured at the register level.
Although this project currently uses .csv files, libraries for handling .xls and .xlsx files can be installed and used if needed.

Scripts Description
1️⃣ PinExtractFromCsvFile.py

Extracts only the required information from the provided input file.
Filters and restructures the data to generate a simplified Results.csv file used by the verification script.
This script is the first step in the workflow.


2️⃣ ReadFromWinIDEA.py

Connects to an active WinIDEA session using the isystem.connect API.
Reads SFR values directly from the MCU.
Provides low‑level access used by the pin verification tool to read hardware registers.


3️⃣ PinCheck.py
Automated pin configuration verification tool for RH850 F1K MCUs.
Functionality:

Reads a pin list from Results.csv containing:

Pin name
Pin number
Pin function
Expected Alternative Function (AF) mode


Connects to a live, halted MCU session in WinIDEA.
Reads the following 7 SFRs per pin:

P
PM
PFC
PFCE
PFCAE
PFCEAE
PMC


For pins configured in alternative function mode (PMC = 1):

Validates the actual register values
Compares them against the expected bit patterns defined in Table 2.20 of the RH850 F1K Hardware Manual (AF1–AF16, Input/Output)


Produces a PASS / FAIL result for each pin.

Output:

Verification results are written to:

SFR_Comparison_Results.csv




Workflow Summary

Provide a pin configuration file (.csv)
Run PinExtractFromCsvFile.py to extract and prepare input data
Ensure WinIDEA is open and connected to the target MCU
Run PinCheck.py to validate pin configurations
Review results in SFR_Comparison_Results.csv


Requirements

WinIDEA installed and running
Active and halted MCU debug session
Python 3
isystem.connect Python API available
RH850 F1K Hardware Manual (for reference)


Notes

The scripts interact directly with live hardware registers, so ensure the target state is stable.
Additional spreadsheet formats (.xls, .xlsx) can be supported by installing the appropriate Python libraries.
Intended for verification and validation use, not for modifying register values.
