#!/bin/bash

input_dir="/mnt/c/Users/nadim/OneDrive - University of Pittsburgh/Postdoctoral_Research/Enlarged_perivascular_space/Data/MS-BRAIN"
output_dir="/mnt/d/PhD_Data/MSBRAIN/Converted"

# Loop through each subject
for subject_dir in "$input_dir"/*; do
    if [ -d "$subject_dir" ]; then
        subject=$(basename "$subject_dir")
        echo "Processing Subject: $subject"

        # Create subject's output directory
        mkdir -p "$output_dir/$subject"

        # Loop through each sequence
        for sequence_dir in "$subject_dir"/*; do
            if [ -d "$sequence_dir" ]; then
                sequence=$(basename "$sequence_dir")
                echo "  Converting Sequence: $sequence"

                # Convert DICOM to NIfTI and name according to sequence
                dcm2niix -z y -f "$sequence" -o "$output_dir/$subject" "$sequence_dir"
            fi
        done
    fi
done
