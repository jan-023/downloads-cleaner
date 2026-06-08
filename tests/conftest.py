import shutil
from pathlib import Path
import pytest


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
