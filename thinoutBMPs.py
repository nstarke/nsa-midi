#!/usr/bin/env python3

import os
import sys

def usage():
    print(f"Usage: {sys.argv[0]} [-y] <dir_path> <keep>")
    print("  -y: optional flag to skip confirmation prompt")
    print("  dir_path: directory containing BMP files to thin out")
    print("  keep: number of largest files to keep (must be a positive integer)")
    sys.exit(1)

def confirm_deletion(files_to_delete):
    print(f"We're about to delete those {len(files_to_delete)} files:")
    for f, _ in files_to_delete:
        print(f"  {f}")
    
    response = input(f"\nOK to delete those {len(files_to_delete)} files? [N/y] ").strip().lower()
    return response in ['y', 'yes']

# Parse command line arguments
auto_confirm = False
args = [arg for arg in sys.argv[1:] if arg != "-y"]

if "-y" in sys.argv:
    auto_confirm = True

if len(args) != 2:
    usage()

dir_path = args[0]
keep_str = args[1]

# Validate directory exists
if not os.path.exists(dir_path):
    print(f"Error: Directory '{dir_path}' does not exist")
    sys.exit(1)

if not os.path.isdir(dir_path):
    print(f"Error: '{dir_path}' is not a directory")
    sys.exit(1)

# Validate keep parameter is a positive integer
try:
    keep = int(keep_str)
    if keep <= 0:
        raise ValueError()
except ValueError:
    print(f"Error: '{keep_str}' is not a valid positive integer")
    sys.exit(1)

# Collect only BMP files with their sizes
files = []
for f in os.listdir(dir_path):
    full_path = os.path.join(dir_path, f)
    if os.path.isfile(full_path) and f.lower().endswith(('.bmp')):
        files.append((f, os.path.getsize(full_path)))

if len(files) == 0:
    print(f"No BMP files found in directory '{dir_path}'")
    sys.exit(0)

# Sort by size (descending)
files.sort(key=lambda x: x[1], reverse=True)

# Determine files to delete
files_to_delete = files[keep:]

if len(files_to_delete) == 0:
    print(f"No files to delete. Found {len(files)} BMP files, keeping {keep}")
    sys.exit(0)

# Confirm deletion unless -y flag is used
if not auto_confirm:
    if not confirm_deletion(files_to_delete):
        print("Deletion cancelled")
        sys.exit(0)

# Delete the files
deleted_count = 0
for f, size in files_to_delete:
    try:
        os.remove(os.path.join(dir_path, f))
        deleted_count += 1
        print(f"Deleted: {f}")
    except OSError as e:
        print(f"Error deleting {f}: {e}")

print(f"\nDeleted {deleted_count} files, kept {len(files) - deleted_count} largest BMP files")

