from pathlib import Path
from rich.console import Console
import platform
import subprocess

from downloads_cleaner.scanner import scan_directory
from downloads_cleaner.categorizer import batch_categorize_files
from downloads_cleaner.presenter_review import render_review_tree
from downloads_cleaner.recommendation_engine import build_recommendations
from downloads_cleaner.actions.planner import move_to_recycle


SORT_OPTIONS = ["age", "category", "extension", "duplicates", "exit"]


def get_sort_mode():
    print("\nSort options:")
    for opt in SORT_OPTIONS[:-1]:  # exclude 'exit' from display
        print(f" - {opt}")
    print(" - exit (quit program)")

    choice = input("\nEnter sort mode (default = category): ").strip().lower()
    if choice in ("", "default"):
        print("Using default: category")
        return "category"

    if choice not in SORT_OPTIONS:
        print("Invalid choice, using default: category")
        return "category"

    return choice


def confirm_recycle(count):
    answer = input(f"\nMove {count} recommended file(s) to Recycle Bin? (Yes/No): ").strip().lower()
    return answer in ("yes")


def flatten_recyclable(recommendations):
    """
    Extract ONLY files marked for recycle from Recommendation objects.
    """
    recyclable = []
    for r in recommendations:
        if r.action == "recycle":
            recyclable.extend(r.files)
    return recyclable

def get_windows_downloads_wsl() -> Path:
    """
    Returns the correct Windows Downloads folder from WSL.
    """
    # Ask Windows for the real user profile path
    result = subprocess.run(
        ["cmd.exe", "/c", "echo %USERPROFILE%"],
        capture_output=True,
        text=True
    )

    win_home = result.stdout.strip().replace("\\", "/")

    # Convert C:/Users/username → /mnt/c/Users/username
    if win_home.startswith("C:/"):
        win_home = "/mnt/" + win_home.replace("C:/", "c/")

    return Path(win_home) / "Downloads"

def get_downloads_path(mode: str) -> Path:
    if mode == "sandbox":
        return Path("tests/fixtures/downloads_sample")

    system = platform.system().lower()

    if system == "windows":
        return Path.home() / "Downloads"

    if "microsoft" in platform.uname().release.lower():
        return get_windows_downloads_wsl()

    return Path.home() / "Downloads"

def select_download_source():
    print("Select mode:")
    print(" 1) Sandbox (safe test data)")
    print(" 2) Real Downloads folder")

    choice = input("\nEnter choice (default = 1): ").strip()

    if choice == "2":
        print("\n⚠️ Real mode selected — using actual Downloads folder.")
        return "real"

    print("\nUsing sandbox mode.")
    return "sandbox"

def main():
    console = Console()

    mode = select_download_source()
    downloads_path = get_downloads_path(mode)

    print("\n==============================")
    print(" Downloads Cleaner CLI Demo")
    print("==============================\n")

    # 1. Scan
    print("Scanning files...")
    files = scan_directory(downloads_path)
    print(f"Found {len(files)} files")

    # 2. Categorize
    categorized_files = batch_categorize_files(files)

    # 3. Show ALL files by default (category view)
    print("\nBuilding review tree (default view = category)...\n")
    render_review_tree(console, files, view="category")

    # 4. Build recommendations
    print("\nAnalyzing recommendations...")
    recommendations = build_recommendations(categorized_files)
    recyclable_files = flatten_recyclable(recommendations)
    recyclable_file_infos = [cf.file for cf in recyclable_files]

    if recyclable_file_infos:
        print(f"\n{len(recyclable_file_infos)} file(s) recommended for recycling:")
        for f in recyclable_file_infos:
            print(f" - {f.path.name}")

        # 5. Ask user for approval
        if confirm_recycle(len(recyclable_file_infos)):
            print("\nMoving files to Recycle Bin (safe operation)...")
            for f in recyclable_file_infos:
                move_to_recycle(f)
            print("Recycle operation complete.")
        else:
            print("\nNo changes made. Exiting safely.")
    else:
        print("\nNo safe cleanup candidates found.")

    # 6. Let user explore files in a loop until exit
    while True:
        view = get_sort_mode()
        if view == "exit":
            print("\nExiting program. Goodbye!")
            break

        print(f"\nBuilding review tree (view = {view})...\n")
        render_review_tree(console, files, view=view)


if __name__ == "__main__":
    main()
