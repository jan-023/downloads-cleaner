from enum import Enum

# Public API imports
from collections import defaultdict
from downloads_cleaner.recommendation_engine import Recommendation, ActionType
from datetime import datetime
import os

# Collapsible modules UX display
from rich.console import Console
from rich.tree import Tree
from rich.text import Text

INDENT_ACTION = ""
INDENT_CATEGORY = "    "
INDENT_FILE = "        "

class ReviewViewMode(Enum):
    CATEGORY = "category"
    EXTENSION = "extension"
    AGE = "age"

console = Console()

def render_report_collapsible(recommendations: list[Recommendation]) -> None:
    """
    Interactive tree view for CLI inspection (NOT for tests).
    """
    action_groups = defaultdict(list)
    total_files = 0

    for r in recommendations:
        action_groups[r.action].append(r)
        total_files += len(r.files)

    console.print(Text(f"Total files: {total_files}", style="bold green"))
    console.print()

    tree = Tree("📂 Downloads Cleaner", guide_style="bold cyan")

    for action, recs in action_groups.items():
        action_count = sum(len(r.files) for r in recs)

        # SAFE: assume action is already ActionType
        action_label = action.name if hasattr(action, "name") else str(action).upper()

        action_node = tree.add(
            f"[bold red]{action_label}[/] ([bold]{action_count} files[/])"
        )

        category_groups = defaultdict(list)

        for r in recs:
            category_groups[r.category].append(r)

        for category, cat_recs in category_groups.items():
            cat_node = action_node.add(f"[yellow]{category.name}[/]")

            for r in cat_recs:
                for f in r.files:
                    cat_node.add(f"{f.file.path.name}")

    console.print(tree)

def render_report(
    recommendations: list[Recommendation],
    review_view: ReviewViewMode = ReviewViewMode.CATEGORY
    ) -> str:
    """Render a full CLI report for recommendations."""

    # Group by action type first
    grouped = defaultdict(list)
    for r in recommendations:
            grouped[r.action].append(r)

    output = []

    # RECYCLE section
    if grouped.get(ActionType.RECYCLE):
        output.append(_render_recycle(grouped[ActionType.RECYCLE]))

    # REVIEW section (flexible)
    if grouped.get(ActionType.REVIEW):
        output.append(_render_review(grouped[ActionType.REVIEW], review_view))

    return "\n\n".join(output)

def _render_recycle(recommendations):
    lines = ["🧹 RECYCLE"]

    for r in recommendations:
        lines.append(f"{INDENT_CATEGORY}📦 {r.category.name}")

        for f in r.files:
            lines.append(f"{INDENT_FILE}- {f.file.path.name}")

    return "\n".join(lines)

def _render_review(recommendations, mode):
    if mode == ReviewViewMode.CATEGORY:
        return _render_review_by_category(recommendations)
    elif mode == ReviewViewMode.EXTENSION:
        return _render_review_by_extension(recommendations)
    elif mode == ReviewViewMode.AGE:
        return _render_review_by_age(recommendations)
    else:
        raise ValueError(f"Unknown review view mode: {mode}")

def _render_review_by_category(recommendations):
    grouped = defaultdict(list)

    for r in recommendations:
        grouped[r.category].extend(r.files)

    lines = ["👀 REVIEW (by category)"]

    for category, files in grouped.items():
        lines.append(f"{INDENT_CATEGORY}📄 {category.name}")

        for f in files:
            lines.append(f"{INDENT_FILE}- {f.file.path.name}")

    return "\n".join(lines)

def _render_review_by_extension(recommendations):
    grouped = defaultdict(list)

    for r in recommendations:
        for f in r.files:
            ext = os.path.splitext(f.file.path.name)[1].lower() or "no-extension"
            grouped[ext].append(f)

    lines = ["👀 REVIEW (by extension)"]

    for ext, files in grouped.items():
        lines.append(f"{INDENT_CATEGORY}📎 {ext}")

        for f in files:
            lines.append(f"{INDENT_FILE}- {f.file.path.name}")

    return "\n".join(lines)

def _render_review_by_age(recommendations):
    grouped = {
        "0-30 days": [],
        "30-180 days": [],
        "180+ days": [],
    }

    now = datetime.now()

    for r in recommendations:
        for f in r.files:
            age_days = (now - f.file.modified).days

            if age_days <= 30:
                grouped["0-30 days"].append(f)
            elif age_days <= 180:
                grouped["30-180 days"].append(f)
            else:
                grouped["180+ days"].append(f)

    lines = ["👀 REVIEW (by age)"]

    for bucket, files in grouped.items():
        lines.append(f"{INDENT_CATEGORY}⏳ {bucket}")

        for f in files:
            lines.append(f"{INDENT_FILE}- {f.file.path.name}")

    return "\n".join(lines)

