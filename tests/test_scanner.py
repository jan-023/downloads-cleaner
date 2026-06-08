from downloads_cleaner.scanner import scan_directory


def test_scan_directory_returns_files(sample_downloads):
    files = scan_directory(sample_downloads)

    # basic sanity checks
    assert isinstance(files, list)
    assert len(files) == 19  # matches your fixture size

    # ensure structure is correct
    first = files[0]
    assert hasattr(first, "path")
    assert hasattr(first, "size")
    assert hasattr(first, "extension")
    assert hasattr(first, "modified")

def test_all_files_have_valid_structure(sample_downloads):
    files = scan_directory(sample_downloads)

    assert len(files) == 19

    for f in files:
        assert f.path.exists()
        assert isinstance(f.size, int)
        assert isinstance(f.extension, str)
        assert f.modified is not None

def test_edge_case_files_are_handled(sample_downloads):
    files = scan_directory(sample_downloads)

    paths = [f.path.name for f in files]

    assert "no_extension_file" in paths
    assert "weird.file.name.txt" in paths
    assert "download.crdownload" in paths

def test_extensions_are_parsed_correctly(sample_downloads):
    files = scan_directory(sample_downloads)

    by_name = {f.path.name: f for f in files}

    assert by_name["resume.pdf"].extension == ".pdf"
    assert by_name["image.jpg"].extension == ".jpg"
    assert by_name["no_extension_file"].extension == ""

def test_age_is_reasonably_computed(sample_downloads):
    files = scan_directory(sample_downloads)

    by_name = {f.path.name: f for f in files}

    assert by_name["setup.exe"].age_days >= 100
    assert by_name["resume.pdf"].age_days <= 10

def test_weird_filename_is_parsed_correctly(sample_downloads):
    files = scan_directory(sample_downloads)

    by_name = {f.path.name: f for f in files}

    weird = by_name["weird.file.name.txt"]

    # 1. Path is preserved correctly
    assert weird.path.name == "weird.file.name.txt"

    # 2. Extension should be last suffix only
    assert weird.extension == ".txt"

    # 3. File should exist on disk
    assert weird.path.exists()

    # 4. Age should be computed (approximate check)
    assert weird.age_days is not None
    assert 70 <= weird.age_days <= 80

    # 5. Size should be positive (from fixture content)
    assert weird.size > 0

