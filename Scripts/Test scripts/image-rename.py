import os
import random
import string
import zlib
import time

# Directory containing the files
directory = r'C:\Path\to\your\wallpapers'

"""
This script renames files in a specified directory to random 6-character alphanumeric filenames consisting
of uppercase letters and digits. It includes the following features:

1. Skips renaming files that already have a 6-character long name.
2. Ensures that no two files will be renamed to the same filename by checking for existing filenames
   and generating new ones until a unique name is found.
3. Generates CRC checksums for each file to check for duplicate contents and deletes duplicates.
4. Prints a message for each file it renames, indicates when it skips a file, and deletes duplicates.
5. Provides a summary at the end of the script, indicating how many files it scanned, skipped, renamed, deleted,
   and the count of each file type.
6. Displays the total time the script took to run.
"""

# Function to generate a random filename
def generate_random_filename(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to calculate the CRC checksum of a file
def calculate_crc(file_path):
    prev = 0
    for eachLine in open(file_path, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X" % (prev & 0xFFFFFFFF)

# Function to rename files in the directory
def rename_files(directory):
    start_time = time.time()
    scanned_count = 0
    skipped_count = 0
    renamed_count = 0
    duplicate_count = 0
    file_type_counts = {}
    crc_dict = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            scanned_count += 1
            file_name, file_extension = os.path.splitext(filename)

            # Count file types
            file_extension = file_extension.lower()
            if file_extension not in file_type_counts:
                file_type_counts[file_extension] = 0
            file_type_counts[file_extension] += 1

            # Calculate CRC checksum
            file_crc = calculate_crc(file_path)

            if file_crc in crc_dict:
                duplicate_count += 1
                os.remove(file_path)
                print(f'Deleting "{filename}" (duplicate content found)')
                continue
            crc_dict[file_crc] = filename

            if len(file_name) == 6:
                skipped_count += 1
                print(f'Skipping "{filename}" (already 6 characters long) CRC: {file_crc}')
                continue

            # Generate a unique filename
            new_filename = generate_random_filename() + file_extension
            new_file_path = os.path.join(directory, new_filename)
            while os.path.exists(new_file_path):
                new_filename = generate_random_filename() + file_extension
                new_file_path = os.path.join(directory, new_filename)
            
            os.rename(file_path, new_file_path)
            renamed_count += 1
            print(f'Renaming "{filename}" to "{new_filename}"')

    end_time = time.time()
    total_time = end_time - start_time

    # Summary
    print("\nSummary:")
    print(f"Total files scanned: {scanned_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"Files renamed: {renamed_count}")
    print(f"Duplicates deleted: {duplicate_count}")
    for file_type, count in file_type_counts.items():
        print(f"{file_type.upper()} files scanned: {count}")
    print(f"Total time taken: {total_time:.2f} seconds")

# Run the renaming process
rename_files(directory)

# Pause at the end
input("Press Enter to exit...")
