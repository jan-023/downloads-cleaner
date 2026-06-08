from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass
class FileInfo:
    path: Path
    size: int
    extension: str
    modified: datetime
    age_days: int | None = None

def scan_directory(directory: Path) -> list[FileInfo]:
    files: list[FileInfo] = []

    for item in directory.iterdir():
        if not item.is_file():
            continue

        stat = item.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)

        files.append(
            FileInfo(
                path=item,
                size=stat.st_size,
                extension=item.suffix.lower(),
                modified=modified,
                age_days=get_age_days(modified)
            )
        )

    return files

def get_age_days(modified: datetime) -> int:
    now = datetime.now()
    return (now - modified).days
