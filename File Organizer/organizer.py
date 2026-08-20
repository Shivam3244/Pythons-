import os
import shutil

FILE_CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff"
    },
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"
    },
    "Audio": {
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"
    },
    "Archives": {
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"
    },
    "Spreadsheets": {
        ".xls", ".xlsx", ".csv", ".ods"
    },
    "Presentations": {
        ".ppt", ".pptx", ".odp"
    }
}


def get_category(filename):
    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def unique_destination(destination):
    if not os.path.exists(destination):
        return destination

    directory, filename = os.path.split(destination)
    name, extension = os.path.splitext(filename)
    counter = 1

    while True:
        new_name = f"{name}_{counter}{extension}"
        new_destination = os.path.join(directory, new_name)

        if not os.path.exists(new_destination):
            return new_destination

        counter += 1


def organize_directory(directory):
    summary = {}

    for filename in os.listdir(directory):
        source = os.path.join(directory, filename)

        # Skip directories and hidden/system entries.
        if not os.path.isfile(source) or filename.startswith("."):
            continue

        category = get_category(filename)
        target_folder = os.path.join(directory, category)
        os.makedirs(target_folder, exist_ok=True)

        destination = os.path.join(target_folder, filename)
        destination = unique_destination(destination)

        shutil.move(source, destination)
        summary[category] = summary.get(category, 0) + 1

    return summary
