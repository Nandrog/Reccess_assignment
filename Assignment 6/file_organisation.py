"""Professional file organization automation using object-oriented programming.

This script scans a selected folder and organizes files into category-based
subfolders such as Documents, Images, Videos, Audio, Archives, Code, and Others.
It can be used for a Downloads folder or any other directory.
"""

from __future__ import annotations

import argparse
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from tkinter import Tk, filedialog
from typing import Dict, List


class FileOrganizer(ABC):
    """Abstract base class for organizing files into categorized folders."""

    def __init__(self, source_dir: str | Path, destination_dir: str | Path | None = None) -> None:
        self.source_dir = Path(source_dir).expanduser().resolve()
        self.destination_dir = (
            Path(destination_dir).expanduser().resolve()
            if destination_dir is not None
            else self.source_dir
        )

        self.category_map: Dict[str, List[str]] = {
            "Documents": [
                ".pdf", ".doc", ".docx", ".txt", ".rtf", ".ppt", ".pptx",
                ".xls", ".xlsx", ".csv"
            ],
            "Images": [
                ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"
            ],
            "Videos": [
                ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"
            ],
            "Audio": [
                ".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"
            ],
            "Archives": [
                ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"
            ],
            "Code": [
                ".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs",
                ".html", ".css", ".json", ".xml", ".yaml", ".yml"
            ],
            "Executables": [
                ".exe", ".msi", ".apk", ".dmg", ".bat", ".sh"
            ],
        }
        self.organized_count = 0

    @abstractmethod
    def get_target_category(self, filepath: Path) -> str:
        """Return the target category for a file path."""
        pass

    def ensure_directory(self, directory_path: Path) -> Path:
        """Create a directory if it does not already exist."""
        directory_path.mkdir(parents=True, exist_ok=True)
        return directory_path

    def get_category(self, file_extension: str) -> str:
        """Return the category for a given file extension."""
        extension = file_extension.lower()
        for category, extensions in self.category_map.items():
            if extension in extensions:
                return category
        return "Others"

    def get_unique_path(self, destination_path: Path) -> Path:
        """Generate a non-conflicting file path if the target already exists."""
        if not destination_path.exists():
            return destination_path

        stem = destination_path.stem
        suffix = destination_path.suffix
        counter = 1
        while True:
            new_path = destination_path.with_name(f"{stem} ({counter}){suffix}")
            if not new_path.exists():
                return new_path
            counter += 1

    def organize(self, dry_run: bool = False) -> int:
        """Organize files from the source directory into categorized folders."""
        if not self.source_dir.exists():
            raise FileNotFoundError(f"The source directory does not exist: {self.source_dir}")
        if not self.source_dir.is_dir():
            raise NotADirectoryError(f"The source path is not a directory: {self.source_dir}")

        files = [item for item in self.source_dir.iterdir() if item.is_file()]
        if not files:
            print("No files found to organize.")
            return 0

        for file_path in files:
            category = self.get_target_category(file_path)
            target_folder = self.ensure_directory(self.destination_dir / category)
            target_path = self.get_unique_path(target_folder / file_path.name)

            if dry_run:
                print(f"[DRY RUN] {file_path.name} -> {target_folder.name}/{target_path.name}")
            else:
                shutil.move(str(file_path), str(target_path))
                print(f"Moved: {file_path.name} -> {target_folder.name}/{target_path.name}")
                self.organized_count += 1

        return self.organized_count


class DownloadFileOrganizer(FileOrganizer):
    """Concrete implementation that sorts files by extension."""

    def get_target_category(self, filepath: Path) -> str:
        return self.get_category(filepath.suffix)


def select_folder(default_path: str | Path | None = None) -> str:
    """Open a folder-selection dialog so the user can choose a directory."""
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        initial_dir = str(default_path) if default_path else str(Path.home())
        selected_path = filedialog.askdirectory(
            title="Select folder to organize",
            initialdir=initial_dir,
        )
        root.destroy()
        return selected_path or str(default_path or os.path.join(os.path.expanduser("~"), "Downloads"))
    except Exception:
        return str(default_path or os.path.join(os.path.expanduser("~"), "Downloads"))


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the script."""
    parser = argparse.ArgumentParser(
        description="Organize files in a folder into category-based subfolders."
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        default=None,
        help="Directory to organize. If omitted, you will be asked to select a folder.",
    )
    parser.add_argument(
        "--destination",
        "-d",
        default=None,
        help="Optional destination directory. Defaults to the source folder.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned actions without moving any files.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the file organizer from the command line."""
    args = parse_arguments()
    selected_folder = args.source_dir

    if not selected_folder:
        selected_folder = select_folder(os.path.join(os.path.expanduser("~"), "Downloads"))

    organizer = DownloadFileOrganizer(selected_folder, args.destination)

    print(f"Starting file organization in: {organizer.source_dir}")
    count = organizer.organize(dry_run=args.dry_run)

    if args.dry_run:
        print(f"Dry run completed. {count} items were identified for organizing.")
    else:
        print(f"Organization complete. {count} files were moved.")


if __name__ == "__main__":
    main()
