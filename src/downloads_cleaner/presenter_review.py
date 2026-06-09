from collections import defaultdict
from datetime import datetime
from rich.tree import Tree
from downloads_cleaner.categorizer import batch_categorize_files
import re

DUPLICATE_PATTERN = re.compile(r"^(.*?)\s\((\d+)\)(\.[^.]+)?$")

def group_by_category(files):
    groups = defaultdict(list)
    for f in files:
        categorized = batch_categorize_files([f])
        category = categorized[0].category
        groups[category.value.upper()].append(f)
    return groups

def group_by_extension(files):
    groups = defaultdict(list)
    for f in files:
        groups[f.extension].append(f)
    return groups

def normalize_filename(name: str) -> str:
    match = DUPLICATE_PATTERN.match(name)
    if match:
        base = match.group(1)
        ext = match.group(3) or ""
        return base + ext
    return name

def group_by_duplicates(files):
    groups = defaultdict(list)
    temp = defaultdict(list)

    for file in files:
        base_name = normalize_filename(file.path.name)
        temp[base_name].append(file)

    for base_name, group in temp.items():
        if len(group) > 1:
            groups[base_name] = group

    return groups

def group_by_age(files, now=None):
    buckets = {
        "Last 30 Days": [],
        "30–90 Days": [],
        "90–180 Days": [],
        "6–12 Months": [],
        "Over 1 Year": [],
    }

    for f in files:
        age_days = f.age_days
        if age_days is None:
            continue

        if age_days < 30:
            buckets["Last 30 Days"].append(f)
        elif age_days < 90:
            buckets["30–90 Days"].append(f)
        elif age_days < 180:
            buckets["90–180 Days"].append(f)
        elif age_days < 365:
            buckets["6–12 Months"].append(f)
        else:
            buckets["Over 1 Year"].append(f)

    return buckets


def build_review_tree(title, grouped_files):
    tree = Tree(title)

    for group_name, files in grouped_files.items():
        branch = tree.add(str(group_name))
        for file in files:
            branch.add(file.path.name)

    return tree

def render_review_tree(console, review_files, view):
    if view == "category":
        grouped = group_by_category(review_files)

    elif view == "age":
        grouped = group_by_age(review_files)

    elif view == "extension":
        grouped = group_by_extension(review_files)

    elif view == "duplicates":
        grouped = group_by_duplicates(review_files)

    else:
        raise ValueError(f"Unknown view: {view}")

    tree = build_review_tree(
        f"Review Files ({view.title()})",
        grouped,
    )

    console.print(tree)

