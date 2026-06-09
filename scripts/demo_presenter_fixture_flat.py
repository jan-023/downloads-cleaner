import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from downloads_cleaner.scanner import scan_directory
from downloads_cleaner.categorizer import batch_categorize_files
from downloads_cleaner.recommendation_engine import build_recommendations
from downloads_cleaner.presenter import render_report, ReviewViewMode

DOWNLOADS_FIXTURE_PATH = "tests/fixtures/downloads_sample"


def main():
    # Step 1: Scan fixture dataset
    files = scan_directory(Path(DOWNLOADS_FIXTURE_PATH))

    # Step 2: Categorize
    categorized = batch_categorize_files(files)

    # Step 3: Build recommendations
    recommendations = build_recommendations(categorized)

    # Step 4: Print ALL views

    print("\n" + "=" * 70)
    print("DEFAULT VIEW (CATEGORY)")
    print("=" * 70)
    print(render_report(recommendations, ReviewViewMode.CATEGORY))

    print("\n" + "=" * 70)
    print("REVIEW VIEW (EXTENSION)")
    print("=" * 70)
    print(render_report(recommendations, ReviewViewMode.EXTENSION))

    print("\n" + "=" * 70)
    print("REVIEW VIEW (AGE)")
    print("=" * 70)
    print(render_report(recommendations, ReviewViewMode.AGE))


if __name__ == "__main__":
    main()
