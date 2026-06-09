from downloads_cleaner.categorizer import (
    categorize,
    CategorizedFile,
    batch_categorize_files,
)
from downloads_cleaner.category import Category
from downloads_cleaner.scanner import scan_directory


def test_all_cases_are_categorized_correctly(sample_downloads):
    files = scan_directory(sample_downloads)
    by_name = {f.path.name: f for f in files}

    # TEMPORARY FILES
    assert categorize(by_name["download.crdownload"]) == Category.TEMPORARY
    assert categorize(by_name["temp.tmp"]) == Category.TEMPORARY
    assert categorize(by_name["partial.part"]) == Category.TEMPORARY

    # INSTALLERS
    assert categorize(by_name["setup.exe"]) == Category.INSTALLER
    assert categorize(by_name["old_installer.msi"]) == Category.INSTALLER
    assert categorize(by_name["game.pkg"]) == Category.INSTALLER

    # ARCHIVES
    assert categorize(by_name["backup.zip"]) == Category.ARCHIVE
    assert categorize(by_name["photos.rar"]) == Category.ARCHIVE
    assert categorize(by_name["data.7z"]) == Category.ARCHIVE

    # DOCUMENTS
    assert categorize(by_name["resume.pdf"]) == Category.DOCUMENT
    assert categorize(by_name["notes.docx"]) == Category.DOCUMENT
    assert categorize(by_name["todo.txt"]) == Category.DOCUMENT
    assert categorize(by_name["weird.file.name.txt"]) == Category.DOCUMENT

    # MEDIA
    assert categorize(by_name["image.jpg"]) == Category.MEDIA
    assert categorize(by_name["video.mp4"]) == Category.MEDIA
    assert categorize(by_name["song.mp3"]) == Category.MEDIA

    # EDGE CASES
    assert categorize(by_name["no_extension_file"]) == Category.UNKNOWN


def test_batch_categorize_wraps_all_files(sample_downloads):
    """
    Check that each FileInfo becomes a CategorizedFile object
    """
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    # Ensure all items are CategorizedFile objects
    assert all(isinstance(c, CategorizedFile) for c in categorized)
    # Each object has file and category attributes
    assert all(hasattr(c, "file") for c in categorized)
    assert all(hasattr(c, "category") for c in categorized)


def test_categorized_file_consistency(sample_downloads):
    """
    Checkthat CategorizedFile.category matches what categorize(file) would produce
    """
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    for c in categorized:
        assert c.category == categorize(c.file)


def test_no_files_lost_in_batch(sample_downloads):
    """
    Check that every file from scan_directory is represented in the batch wrapper
    """
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    original_paths = {f.path.name for f in files}
    categorized_paths = {c.file.path.name for c in categorized}

    assert original_paths == categorized_paths
