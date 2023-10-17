#!/usr/bin/env python
import random
import subprocess
from moviepy.editor import VideoFileClip
import os


def extract_last_frame(video_path, output_folder=None):
    clip = VideoFileClip(video_path)

    # Determine the time of the last frame
    last_frame_time = clip.duration - (1 / clip.fps)  # Subtracting one frame duration

    # Determine the output path for the image
    if not output_folder:
        output_folder = os.path.dirname(video_path)
    base_name = os.path.basename(video_path).rsplit('.', 1)[0]
    image_path = os.path.join(output_folder, f"{base_name}_last_frame.png")

    # Save the last frame as an image
    clip.save_frame(image_path, t=last_frame_time)

    return image_path


def split_video_chunks_with_frame_extraction(video_path, start_chunk, num_chunks, min_duration=1.5, max_duration=2.5,
                                             output_folder="/Users/ellioe03/Downloads/Free Palestine Video Clips and Images/Output/"):
    clip = VideoFileClip(video_path).without_audio()
    total_duration = clip.duration

    # Calculate average chunk duration
    avg_duration = (min_duration + max_duration) / 2
    start_time = start_chunk * avg_duration

    # List to store file names of the chunks and the last frame images
    output_files = []
    output_images = []

    for i in range(num_chunks):
        # Get random duration for next chunk
        chunk_duration = random.uniform(min_duration, max_duration)
        end_time = start_time + chunk_duration

        # Ensure the chunk doesn't exceed the video's total duration
        if end_time > total_duration:
            end_time = total_duration

        # Extract chunk from video
        chunk = clip.subclip(start_time, end_time)

        # Save chunk to file
        output_file = f"{output_folder}chunk_{int(start_time)}_{int(end_time)}.mp4"
        chunk.write_videofile(output_file, codec="libx264", audio_codec="aac",
                              logger=None)  # Disable logger for cleaner output

        # Extract and save the last frame of the chunk as an image
        last_frame_time = chunk.duration - (1 / chunk.fps)
        image_path = output_file.rsplit('.', 1)[0] + "_last_frame.png"
        chunk.save_frame(image_path, t=last_frame_time)

        # Add file and image paths to the lists
        output_files.append(output_file)
        output_images.append(image_path)

        # Update start time for next chunk
        start_time = end_time

        # Break if end of video is reached
        if end_time == total_duration:
            break

    return output_files, output_images


# Split the next 5 chunks and extract the last frame for each chunk
input_folder = "/Users/ellioe03/Downloads/Free Palestine Video Clips and Images/video"

# List all files in the given directory
all_files = os.listdir(input_folder)

# Filter out only the MP4 files
mp4_files = [f for f in all_files if f.endswith('.mp4')]

for mp4_file in mp4_files:
    # Construct the full path to the MP4 file
    full_mp4_path = os.path.join(input_folder, mp4_file)

    output_files_mp4, output_images = split_video_chunks_with_frame_extraction(full_mp4_path,
                                                                                     start_chunk=2, num_chunks=50)

print('')
print(f'output_files_mp4: {output_files_mp4}')
print(f'output_images: {output_images}')



