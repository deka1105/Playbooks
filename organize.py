import os
import shutil
import argparse
from datetime import datetime

def organize_files_by_modified_date(source_dir):
    if not os.path.isdir(source_dir):
        print(f"Error: '{source_dir}' is not a valid directory.")
        return

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        # Skip directories
        if os.path.isdir(item_path):
            continue

        # Get last modified time
        mod_time = os.path.getmtime(item_path)
        date_obj = datetime.fromtimestamp(mod_time)

        # Format: ResumeYYYY-MMM (e.g., Resume2026-Apr)
        folder_name = f"Resume{date_obj.strftime('%Y-%b')}"
        folder_path = os.path.join(source_dir, folder_name)

        # Create folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        destination = os.path.join(folder_path, item)

        # Avoid overwriting
        if os.path.exists(destination):
            print(f"Skipped (exists): {item}")
            continue

        shutil.move(item_path, destination)
        print(f"Moved: {item} -> {folder_name}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files into ResumeYYYY-MMM folders based on modified date"
    )
    parser.add_argument(
        "path",
        help="Path to the directory containing files"
    )

    args = parser.parse_args()

    organize_files_by_modified_date(args.path)