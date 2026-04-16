import os
import shutil
import argparse
from datetime import datetime

def organize(source_dir, prefix, mode):
    if not os.path.isdir(source_dir):
        print(f"Error: '{source_dir}' is not a valid directory.")
        return

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        # Skip directories
        if os.path.isdir(item_path):
            continue

        if mode == "date":
            mod_time = os.path.getmtime(item_path)
            date_obj = datetime.fromtimestamp(mod_time)
            folder_name = f"{prefix}{date_obj.strftime('%Y-%b')}"

        elif mode == "type":
            ext = os.path.splitext(item)[1].lower().replace(".", "")
            ext = ext if ext else "noext"
            folder_name = f"{prefix}_{ext}"

        else:
            print("Invalid mode. Use 'date' or 'type'.")
            return

        folder_path = os.path.join(source_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        destination = os.path.join(folder_path, item)

        # Avoid overwrite
        if os.path.exists(destination):
            print(f"Skipped (exists): {item}")
            continue

        shutil.move(item_path, destination)
        print(f"Moved: {item} -> {folder_name}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files by modified date or file type"
    )

    parser.add_argument(
        "path",
        help="Target directory path"
    )

    parser.add_argument(
        "--prefix",
        default="Resume",
        help="Prefix for folder names (default: Resume)"
    )

    parser.add_argument(
        "--mode",
        choices=["date", "type"],
        default="date",
        help="Organize by 'date' (YYYY-MMM) or 'type' (file extension)"
    )

    args = parser.parse_args()

    organize(args.path, args.prefix, args.mode)