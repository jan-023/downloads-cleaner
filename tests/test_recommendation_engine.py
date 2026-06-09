from downloads_cleaner.scanner import scan_directory
from downloads_cleaner.categorizer import batch_categorize_files
from downloads_cleaner.recommendation_engine import (
    build_recommendations,
    ActionType
)
from downloads_cleaner.category import Category


def test_installers_are_recycled(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    recs = build_recommendations(categorized)

    installer = next(r for r in recs if r.category == Category.INSTALLER)

    assert installer.action == ActionType.RECYCLE


def test_temporary_is_recycled(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    recs = build_recommendations(categorized)

    temp = next(r for r in recs if r.category == Category.TEMPORARY)

    assert temp.action == ActionType.RECYCLE


def test_documents_require_review(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    recs = build_recommendations(categorized)

    doc = next(r for r in recs if r.category == Category.DOCUMENT)

    assert doc.action == ActionType.REVIEW

def test_one_recommendation_per_category(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    recs = build_recommendations(categorized)

    categories = [r.category for r in recs]

    assert len(categories) == len(set(categories))

def test_full_pipeline(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)

    recs = build_recommendations(categorized)

    assert recs
    assert all(r.files for r in recs)

