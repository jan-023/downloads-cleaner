import uuid
from typing import List
from recommendation_engine import Recommendation
from actions.models import ActionIntent, PlannedAction, ActionType


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
