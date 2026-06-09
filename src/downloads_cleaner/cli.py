from scanner import scan_directory
from categorizer import categorize_files
from recommendation_engine import generate_recommendations

from actions.planner import build_plans
from actions.executor import execute_recycle
from presenter_review import (
    group_by_category,
    group_by_extension,
    group_by_duplicates,
    group_by_age,
    render_tree,
)


def run(downloads_path):
    files = scan_directory(downloads_path)
    categorize_files(files)

    recommendations = generate_recommendations(files)
    plans = build_plans(recommendations)

    recycle_plans = [p for p in plans if p.intent.action_type.value == "recycle"]
    review_files = [
        f for p in plans if p.intent.action_type.value == "review"
        for f in p.intent.files
    ]

    # 1. RECYCLE approval
    if recycle_plans:
        print("\nRECYCLE CANDIDATES:")
        for p in recycle_plans:
            for f in p.intent.files:
                print(" •", f.name)

        confirm = input("\nProceed? Type YES or NO: ")

        if confirm == "YES":
            for p in recycle_plans:
                execute_recycle(p, downloads_path)

    # 2. REVIEW sorting
    print("\nREVIEW VIEW OPTIONS:")
    choice = input("1) Category 2) Age 3) Extension 4) Duplicates: ")

    if choice == "1":
        tree = render_tree("REVIEW (Category)", group_by_category(review_files))
    elif choice == "2":
        tree = render_tree("REVIEW (Age)", group_by_age(review_files))
    elif choice == "3":
        tree = render_tree("REVIEW (Extension)", group_by_extension(review_files))
    else:
        tree = render_tree("REVIEW (Duplicates)", group_by_duplicates(review_files))

    print(tree)
