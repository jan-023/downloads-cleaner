import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from downloads_cleaner.scanner import scan_directory
from downloads_cleaner.categorizer import batch_categorize_files
from downloads_cleaner.recommendation_engine import build_recommendations
from downloads_cleaner.presenter import render_report_collapsible

# Path to fixture
DOWNLOADS_FIXTURE_PATH = Path(__file__).resolve().parent.parent / "tests/fixtures/downloads_sample"

def main():
    # Step 1: Scan fixture folder
    files = scan_directory(DOWNLOADS_FIXTURE_PATH)

    # Step 2: Categorize files
    categorized = batch_categorize_files(files)

    # Step 3: Generate recommendations
    recommendations = build_recommendations(categorized)

    # Step 4: Render collapsible interactive tree
    render_report_collapsible(recommendations)

if __name__ == "__main__":
    main()
