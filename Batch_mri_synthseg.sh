#!/bin/bash

# Bash options for robustness
set -euo pipefail
IFS=$'\n\t'

# Directory containing the subjects
Nifti_directory="/mnt/d/PhD_Data/MSBRAIN/Nifti"

# Output directory for segmentation
Brain_Segmentation_directory="/mnt/d/PhD_Data/MSBRAIN/Brain_Segmentation"

# Check if the Nifti directory exists and is a directory
if [ ! -d "$Nifti_directory" ]; then
    echo "Error: Nifti directory does not exist or is not a directory."
    exit 1
fi

# Ensure output directory exists
mkdir -p "$Brain_Segmentation_directory"

# Iterate over each subject in the directory
for subject in "$Nifti_directory"/*; do
    # Check if subject file exists
    if [ ! -e "$subject" ]; then
        echo "Warning: Subject file '$subject' does not exist. Skipping."
        continue
    fi

    # Extract the base name of the subject
    subject_name=$(basename "$subject")

    # Define the output file path
    output_file="$Brain_Segmentation_directory/$subject_name"

    echo "Processing Subject: $subject_name"
    # Processing command
    mri_synthseg --i "$subject" --o "$output_file" --thread 32 --robust
done
