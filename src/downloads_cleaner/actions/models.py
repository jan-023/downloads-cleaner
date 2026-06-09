from dataclasses import dataclass
from enum import Enum
from typing import List
from scanner import FileInfo


class ActionType(Enum):
    RECYCLE = "recycle"
    REVIEW = "review"


@dataclass
class ActionIntent:
    action_type: ActionType
    files: List[FileInfo]
    reason: str
    category: str


@dataclass
class PlannedAction:
    id: str
    intent: ActionIntent
