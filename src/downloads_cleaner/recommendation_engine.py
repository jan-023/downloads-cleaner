from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from downloads_cleaner.category import Category
from downloads_cleaner.categorizer import CategorizedFile


class ActionType:
    RECYCLE = "recycle"
    REVIEW = "review"

@dataclass(slots=True)
class Recommendation:
    category: Category
    action: ActionType
    reason: str
    files: list[CategorizedFile]

def build_recommendations(files: list[CategorizedFile]) -> list[Recommendation]:
    grouped = defaultdict(list)

    # group by category ONLY (internal logic)
    for f in files:
        grouped[f.category].append(f)

    recommendations = []

    for category, items in grouped.items():
        recommendations.append(_apply_rules(category, items))

    return recommendations


def _apply_rules(category: Category, files: list[CategorizedFile]) -> Recommendation:

    if category == Category.INSTALLER:
        return Recommendation(
            category=category,
            action=ActionType.RECYCLE,
            reason="Installer files are candidates for cleanup after use",
            files=files
        )

    if category == Category.ARCHIVE:
        return Recommendation(
            category=category,
            action=ActionType.RECYCLE,
            reason="Old archive files can be safely cleaned up",
            files=files,
        )

    if category == Category.TEMPORARY:
        return Recommendation(
            category=category,
            action=ActionType.RECYCLE,
            reason="Temporary files are safe to recycle",
            files=files,
        )

    if category == Category.MEDIA:
        return Recommendation(
            category=category,
            action=ActionType.REVIEW,
            reason="Media files require manual review",
            files=files,
        )

    if category == Category.DOCUMENT:
        return Recommendation(
            category=category,
            action=ActionType.REVIEW,
            reason="Documents require manual review",
            files=files,
        )

    return Recommendation(
        category=Category.UNKNOWN,
        action=ActionType.REVIEW,
        reason="Unknown files require manual review",
        files=files,
    )
