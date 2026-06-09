import uuid
from typing import List
from downloads_cleaner.recommendation_engine import Recommendation
from downloads_cleaner.actions.models import ActionIntent, PlannedAction, ActionType
import shutil
from downloads_cleaner.scanner import FileInfo
import platform
import subprocess
from pathlib import Path
from send2trash import send2trash

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
    Move file to Recycle Bin safely.
    - Works on WSL → Windows Recycle Bin
    - Works on Windows native
    """
    try:
        path = Path(file.path).resolve()

        # Detect WSL
        is_wsl = "microsoft" in platform.uname().release.lower()
        if is_wsl and str(path).startswith("/mnt/"):
            # Windows file accessed through WSL → use PowerShell

            drive_letter = path.parts[2].upper()

            win_path = (
                f"{drive_letter}:\\"
                + "\\".join(path.parts[3:])
            )

            ps_path = win_path.replace("'", "''")

            subprocess.run([
                "powershell.exe",
                "-NoProfile",
                "-Command",
                (
                    "Add-Type -AssemblyName Microsoft.VisualBasic; "
                    f"[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile("
                    f"'{ps_path}', "
                    "'OnlyErrorDialogs', "
                    "'SendToRecycleBin')"
                )
            ], check=True)

        else:
            # Sandbox files and normal Linux files
            send2trash(str(path))

        print(f"[Recycled] {file.path.name}")
        return True

    except Exception as e:
        print(f"[Error recycling {file.path.name}]: {e}")
        return False

"""
def move_to_recycle(file: FileInfo):
    '''
    Safely move a file to a sandbox recycle bin.
    '''
    try:
        # For sandbox safety, just rename with .recycled suffix
        recycle_path = file.path.with_suffix(file.path.suffix + ".recycled")
        shutil.move(str(file.path), str(recycle_path))
        return True
    except Exception as e:
        print(f"Failed to recycle {file.path}: {e}")
        return False
"""
