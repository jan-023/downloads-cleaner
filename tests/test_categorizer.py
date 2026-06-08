from downloads_cleaner.categorizer import categorize, Category
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
