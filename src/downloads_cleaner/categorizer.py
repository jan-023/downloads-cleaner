from dataclasses import dataclass
from downloads_cleaner.category import Category
from downloads_cleaner.scanner import FileInfo

@dataclass
class CategorizedFile:
    file: FileInfo
    category: Category

INSTALLER_EXT = {".exe", ".msi", ".pkg", ".dmg", ".deb", ".rpm"}
ARCHIVE_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".tar.gz"}
DOCUMENT_EXT = {".pdf", ".docx", ".txt", ".md", ".pptx", ".xlsx"}
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp",
             ".mp4", ".mov", ".avi",
             ".mp3", ".wav", ".flac"}
TEMP_EXT = {".crdownload", ".part", ".tmp", ".download"}


def categorize(file: FileInfo) -> Category:
    """
    Determine the category of a single FileInfo object based on its file extension.

    Args:
        file (FileInfo): The file to categorize.

    Returns:
        Category: The determined category (INSTALLER, ARCHIVE, DOCUMENT, MEDIA, TEMPORARY, UNKNOWN).
    """

    ext = file.extension.lower()

    if ext in TEMP_EXT:
        return Category.TEMPORARY

    if ext in INSTALLER_EXT:
        return Category.INSTALLER

    if ext in ARCHIVE_EXT:
        return Category.ARCHIVE

    if ext in DOCUMENT_EXT:
        return Category.DOCUMENT

    if ext in MEDIA_EXT:
        return Category.MEDIA

    return Category.UNKNOWN


def batch_categorize_files(files: list[FileInfo]) -> list[CategorizedFile]:
    """
    Categorize a list of FileInfo objects and wrap them in CategorizedFile dataclasses.

    Args:
        files (list[FileInfo]): List of FileInfo objects to categorize.

    Returns:
        list[CategorizedFile]: Each FileInfo object paired with its determined Category.
    """
    return [CategorizedFile(file=f, category=categorize(f)) for f in files]
