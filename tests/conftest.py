import shutil
from pathlib import Path
import pytest
from downloads_cleaner.scanner import scan_directory
from downloads_cleaner.categorizer import batch_categorize_files

@pytest.fixture
def sample_downloads(tmp_path):
    """
    Creates an isolated copy of the fixture downloads folder
    for each test run under path 'tmp_path/downloads/'
    """

    source = Path(__file__).parent / "fixtures" / "downloads_sample"
    target = tmp_path / "downloads"

    shutil.copytree(source, target)

    return target

@pytest.fixture
def downloads_sample_files(tmp_path):
    """
    Full pipeline fixture:
    - copies test files
    - scans into FileInfo objects
    - applies categorization
    """
    source = Path(__file__).parent / "fixtures" / "downloads_sample"
    target = tmp_path / "downloads"

    shutil.copytree(source, target)

    files = scan_directory(target)
    batch_categorize_files(files)

    return files

