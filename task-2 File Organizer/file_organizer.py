import os
import shutil
import logging
import argparse


# File categories based on extension
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css"],
}


# Create log file
logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_category(filename):
    """Return the category for a file based on its extension."""

    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def organize_files(folder_path):
    """Organize files in the selected folder."""

    if not os.path.exists(folder_path):
        print("Error: The specified folder does not exist.")
        logging.error("Folder does not exist: %s", folder_path)
        return

    if not os.path.isdir(folder_path):
        print("Error: The specified path is not a folder.")
        logging.error("Path is not a folder: %s", folder_path)
        return

    moved_count = 0
    category_counts = {}

    try:
        for filename in os.listdir(folder_path):

            source_path = os.path.join(folder_path, filename)

            # Ignore folders
            if os.path.isdir(source_path):
                continue

            category = get_category(filename)
            destination_folder = os.path.join(folder_path, category)

            # Create category folder if needed
            os.makedirs(destination_folder, exist_ok=True)

            destination_path = os.path.join(
                destination_folder,
                filename
            )

            # Avoid overwriting an existing file
            if os.path.exists(destination_path):
                name, extension = os.path.splitext(filename)
                counter = 1

                while os.path.exists(destination_path):
                    new_filename = f"{name}_{counter}{extension}"
                    destination_path = os.path.join(
                        destination_folder,
                        new_filename
                    )
                    counter += 1

            shutil.move(source_path, destination_path)

            moved_count += 1
            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

            logging.info(
                "Moved '%s' to '%s'",
                filename,
                category
            )

        print("\nFile organization completed successfully!")
        print(f"Total files organized: {moved_count}")

        if category_counts:
            print("\nSummary:")

            for category, count in category_counts.items():
                print(f"  {category}: {count} file(s)")

        logging.info(
            "Organization completed. Total files moved: %d",
            moved_count
        )

    except PermissionError:
        print("Error: Permission denied while accessing a file or folder.")
        logging.error("Permission denied while organizing: %s", folder_path)

    except OSError as error:
        print(f"Error while organizing files: {error}")
        logging.error("OS error: %s", error)

    except Exception as error:
        print(f"Unexpected error: {error}")
        logging.exception("Unexpected error occurred.")


def main():

    parser = argparse.ArgumentParser(
        description="Automatically organize files by file type."
    )

    parser.add_argument(
        "folder",
        help="Path of the folder whose files should be organized"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("             AUTOMATED FILE ORGANIZER")
    print("=" * 60)

    print(f"\nTarget folder: {args.folder}")

    organize_files(args.folder)


if __name__ == "__main__":
    main()