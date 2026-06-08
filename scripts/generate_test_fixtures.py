from pathlib import Path
import shutil # standard Python library module for copying, moving, and deleting fies and directories safely ("shell utilities")
import os
import time

BASE_DIR = Path("tests/fixtures/downloads_sample")

# (filename, content, days_old)
FILES = [
    # Installers (older files → should trigger cleanup rules later)
    ("setup.exe", "installer binary v1.2.3", 120),
    ("old_installer.msi", "legacy installer package", 200),
    ("game.pkg", "game installation package", 30),

    # Archives
    ("backup.zip", "compressed backup data", 150),
    ("photos.rar", "compressed photo archive", 10),
    ("data.7z", "7zip compressed dataset", 365),

    # Documents
    ("resume.pdf", "John Doe resume content", 5),
    ("notes.docx", "meeting notes and ideas", 90),
    ("todo.txt", "task list", 1),

    # Media
    ("image.jpg", "fake image data", 60),
    ("video.mp4", "fake video data", 300),
    ("song.mp3", "fake audio data", 20),

    # Temporary files (always “recent junk”)
    ("download.crdownload", "partial download", 0),
    ("temp.tmp", "temporary file", 0),
    ("partial.part", "incomplete download", 2),

    # Duplicates
    ("duplicate.pdf", "same content file", 45),
    ("duplicate (1).pdf", "same content file", 45),

    # Edge cases
    ("no_extension_file", "unknown type content", 180),
    ("weird.file.name.txt", "strange filename format", 75),
]

def clear_existing():
    """
    Removes any previously generated test fixture so you always start from a clean slate."
    """
    if BASE_DIR.exists():
        shutil.rmtree(BASE_DIR) # recursively deletes a directory and everything inside of it

def apply_timestamp(file_path: Path, days_old: int):
    """
    Set file modified time to simulate age.
    """
    now = time.time()
    past_time = now - (days_old * 86400)  # 86400 seconds per day

    os.utime(file_path, (past_time, past_time))

def create_files():
    """
    Rebuildsthe fake Downloads folder from scratch using a predefined dataset
    """
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    for filename, content, days_old in FILES:
        file_path = BASE_DIR / filename

        # create file
        file_path.write_text(content, encoding="utf-8")

        # apply fake "age"
        apply_timestamp(file_path, days_old)


def main():
    print("Generating test Downloads fixture...")

    clear_existing()
    create_files()

    print(f"Created fixture at: {BASE_DIR.resolve()}")
    print(f"Total files: {len(FILES)}")


if __name__ == "__main__":
    main()
