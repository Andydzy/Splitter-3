# Splitter 3

## Introduction

Welcome to Splitter 3, an advanced software tool designed for analyzing variable star observations. This tool excels in dividing observations into intervals, each containing precisely one extremum. This requirement appears due to the specifics of the MAVKA software, which approximates extrema and determines a set of their parameters, in particular, the coordinates of the moment of the extremum. 

## Prerequisites

1. **Download and Install Python:**
   - Download the latest version of Python from [python.org](https://www.python.org/downloads/).

2. **Open PowerShell:**
   - PowerShell is a command-line interface for executing commands on Windows. Open PowerShell as an administrator for the following operations.

3. **Install Required Libraries:**
   - Execute the following commands in PowerShell to install necessary libraries:
     ```powershell
     pip install tk
     pip install matplotlib
     pip install numpy
     pip install scipy
     ```

## Download and Run Splitter 3

1. **Download Splitter Software:**
   - Download the Splitter software from our GitHub page.

2. **Navigate to PowerShell:**
   - Open PowerShell and navigate to the folder containing the Splitter software using the `cd` command.

3. **Run Splitter:**
   - Execute the following command to open the Splitter software:
     ```powershell
     python C:\path\to\Splitter_main.py
     ```

![splitter_interface](https://github.com/NUAAR/Splitter/assets/157857913/7439fe12-f3ce-4244-82a5-c383dedf6e00)



## Algorithm Overview

The algorithm consists of three main parts: smoothing, separation, and verification.

1. **Smoothing:**
   - Eliminates noise and determines points for dividing the data into intervals. The original data is utilized to preserve the signal, avoiding distortions introduced by excessive smoothing.

2. **Separation:**
   - Identifies the coordinates of the beginning and end of each extremum, categorizing them as maxima or minima. The software adapts to varying data characteristics, making it robust in different observational scenarios.

3. **Verification:**
   - Checks the compliance of data within each interval against specific requirements. If intervals contain insufficient observations, noisy data, or other issues, corrective actions are taken, ensuring the reliability of extremum moments.

## Usage

### Upload Data

1. Click on "Open Light Curve File" to select a .tess file or input the file path in the textbox.

2. View the interactive light curve plot.

![splitter_lc_upload](https://github.com/NUAAR/Splitter/assets/157857913/449797b2-178c-4208-a198-326e9a4046ce)

### Period Estimation

1. Enter the estimated period, crucial for the algorithm to understand the data's periodicity.

### Data Processing

1. Click on "Process Data" to execute the algorithm and visualize results.

2. The graph displays each individual extremum in distinct colors.

![splitter_results](https://github.com/NUAAR/Splitter/assets/157857913/05d4c29e-98b5-4ca1-9e6e-e1b373ae6d32)


### Save Output

1. Press "Save Results" to save extremum coordinates in !DA format for future MAVKA software analysis.

### Clear

1. Press "Clear" to reset and clear all data.

Explore the capabilities of Splitter 3 to enhance your variable star observations and streamline the analysis process. For further assistance, consult the documentation or reach out to our support team.
