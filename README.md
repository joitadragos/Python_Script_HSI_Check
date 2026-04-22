# RH850 F1K MCUs Documentation

## Overview
The RH850 F1K MCUs are designed for automotive applications with high-performance requirements.

### Key Features
- High-speed operation
- Low power consumption
- Advanced safety features

## WinIDEA Integration
WinIDEA provides a powerful environment for developing and debugging applications for the RH850 F1K MCUs. It supports:
- Real-time debugging
- Code profiling
- Performance analysis

## Scripts
### Automation Scripts
Scripts can be used to automate various tasks:
- Building projects
- Running tests
- Collecting logs

### Script Examples
1. **Build Script**: Automate the building of your project.
2. **Test Script**: Run specific tests to verify your code.

## Verification Process
To ensure the proper functioning of the RH850 F1K MCUs, follow these steps:
1. **Initialization**: Set up your environment and tools.
2. **Execution**: Run your scripts to verify functionality.
3. **Documentation**: Record your findings and any issues encountered.

## Conclusion
For further assistance and detailed information, refer to the settings and configurations within the WinIDEA documentation.

## Scripts Description
1️⃣ **PinExtractFromCsvFile.py**

 - Extracts only the required information from the provided input file.
 - Filters and restructures the data to generate a simplified Results.csv file used by the verification script.
 - This script is the first step in the workflow.


2️⃣ **ReadFromWinIDEA.py**

 - Connects to an active WinIDEA session using the isystem.connect API.
 - Reads SFR values directly from the MCU.
 - Provides low‑level access used by the pin verification tool to read hardware registers.


3️⃣ **PinCheck.py**
Automated pin configuration verification tool for RH850 F1K MCUs.
Functionality:

Reads a pin list from Results.csv containing:

 - Pin name
 - Pin number
 - Pin function
 - Expected Alternative Function (AF) mode


Connects to a live, halted MCU session in WinIDEA.
Reads the following 7 SFRs per pin:

 - P
 - PM
 - PFC
 - PFCE
 - PFCAE
 - PFCEAE
 - PMC
