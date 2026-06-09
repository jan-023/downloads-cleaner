from downloads_cleaner.scanner import scan_directory
from downloads_cleaner.categorizer import batch_categorize_files
from downloads_cleaner.recommendation_engine import build_recommendations, ActionType
from downloads_cleaner.presenter import render_report, ReviewViewMode
from downloads_cleaner.category import Category

def test_render_report_returns_output(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)
    recs = build_recommendations(categorized)

    output = render_report(recs)

    assert isinstance(output, str)
    assert len(output) > 0

def test_recycle_section_present(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)
    recs = build_recommendations(categorized)

    output = render_report(recs)

    assert "🧹 RECYCLE" in output

def test_review_section_present(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)
    recs = build_recommendations(categorized)

    output = render_report(recs)

    assert "👀 REVIEW" in output

def test_review_view_modes_change_output(sample_downloads):
    files = scan_directory(sample_downloads)
    categorized = batch_categorize_files(files)
    recs = build_recommendations(categorized)

    category_view = render_report(recs, ReviewViewMode.CATEGORY)
    ext_view = render_report(recs, ReviewViewMode.EXTENSION)
    age_view = render_report(recs, ReviewViewMode.AGE)

    assert category_view != ext_view
    assert ext_view != age_view


