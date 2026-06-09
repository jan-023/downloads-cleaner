from datetime import datetime
from pathlib import Path

from downloads_cleaner.scanner import FileInfo

from downloads_cleaner.presenter_review import (
    group_by_category,
    group_by_extension,
    group_by_age,
    group_by_duplicates,
    build_review_tree,
)

def test_group_by_duplicates(downloads_sample_files):
    grouped = group_by_duplicates(downloads_sample_files)

    assert "duplicate.pdf" in grouped

    duplicate_names = {
        f.path.name
        for f in grouped["duplicate.pdf"]
    }

    assert duplicate_names == {
        "duplicate.pdf",
        "duplicate (1).pdf",
    }

def test_group_by_extension(downloads_sample_files):
    grouped = group_by_extension(downloads_sample_files)

    assert ".pdf" in grouped
    assert ".docx" in grouped
    assert ".txt" in grouped
    assert ".jpg" in grouped
    assert ".zip" in grouped
    assert len(grouped[".pdf"]) == 3

def test_group_by_category(downloads_sample_files):
    grouped = group_by_category(downloads_sample_files)

    assert "DOCUMENT" in grouped
    assert "MEDIA" in grouped
    assert "ARCHIVE" in grouped
    assert "INSTALLER" in grouped
    assert "TEMPORARY" in grouped

def test_group_by_age():
    files = [
        FileInfo(
            path=Path("recent.txt"),
            size=100,
            extension=".txt",
            modified=datetime.now(),
            age_days=10,
        ),
        FileInfo(
            path=Path("month_old.txt"),
            size=100,
            extension=".txt",
            modified=datetime.now(),
            age_days=45,
        ),
        FileInfo(
            path=Path("four_months.txt"),
            size=100,
            extension=".txt",
            modified=datetime.now(),
            age_days=120,
        ),
        FileInfo(
            path=Path("eight_months.txt"),
            size=100,
            extension=".txt",
            modified=datetime.now(),
            age_days=250,
        ),
        FileInfo(
            path=Path("old.txt"),
            size=100,
            extension=".txt",
            modified=datetime.now(),
            age_days=500,
        ),
    ]

    grouped = group_by_age(files)

    assert len(grouped["Last 30 Days"]) == 1
    assert len(grouped["30–90 Days"]) == 1
    assert len(grouped["90–180 Days"]) == 1
    assert len(grouped["6–12 Months"]) == 1
    assert len(grouped["Over 1 Year"]) == 1

def test_build_review_tree(downloads_sample_files):
    grouped = group_by_extension(downloads_sample_files)

    tree = build_review_tree(
        "Review Files",
        grouped,
    )

    assert tree is not None
