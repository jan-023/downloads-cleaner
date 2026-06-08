from downloads_cleaner.scanner import scan_directory


def test_scan_directory_returns_files(sample_downloads):
    files = scan_directory(sample_downloads)

    assert isinstance(files, list)
    assert len(files) > 0
