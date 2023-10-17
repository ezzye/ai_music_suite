#!/usr/bin/env python

import subprocess
import os


def convert_mp4_to_mp3(directory):
    # List all files in the given directory
    all_files = os.listdir(directory)

    # Filter out only the MP4 files
    mp4_files = [f for f in all_files if f.endswith('.mp4')]

    for mp4_file in mp4_files:
        # Construct the full path to the MP4 file
        full_mp4_path = os.path.join(directory, mp4_file)

        # Construct the output file name by replacing .mp4 with .mp3
        mp3_file = mp4_file.replace('.mp4', '.mp3')
        full_mp3_path = os.path.join(directory, mp3_file)

        # Command to convert MP4 to MP3
        command = [
            "ffmpeg",
            "-i", full_mp4_path,
            "-q:a", "0",
            "-map", "a",
            full_mp3_path
        ]

        # Execute the command
        subprocess.run(command)

    print("Conversion completed!")


# Example usage
directory = input("Enter the path to the directory containing MP4 files: ")
convert_mp4_to_mp3(directory)
