import uuid
from typing import List
from downloads_cleaner.recommendation_engine import Recommendation
from downloads_cleaner.actions.models import ActionIntent, PlannedAction, ActionType
import shutil
from downloads_cleaner.scanner import FileInfo


def build_plans(recommendations: List[Recommendation]) -> List[PlannedAction]:
    plans = []

    for rec in recommendations:
        intent = ActionIntent(
            action_type=rec.action,
            files=rec.files,
            reason=rec.reason,
            category=rec.category,
        )

        plans.append(
            PlannedAction(
                id=str(uuid.uuid4()),
                intent=intent
            )
        )

    return plans

def move_to_recycle(file: FileInfo):
    """
    Safely move a file to a sandbox recycle bin.
    """
    try:
        # For sandbox safety, just rename with .recycled suffix
        recycle_path = file.path.with_suffix(file.path.suffix + ".recycled")
        shutil.move(str(file.path), str(recycle_path))
        return True
    except Exception as e:
        print(f"Failed to recycle {file.path}: {e}")
        return False
