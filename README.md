# Downloads Cleaner

Downloads Cleaner is a Python CLI tool designed to help you safely organize and clean your Downloads folder. It scans files, categorizes them, identifies duplicates and temporary files, and recommends files that can be safely moved to the Recycle Bin, helping you keep your system tidy without accidentally deleting important files.

## Supported Operating Systems

- **Windows 10/11** (including WSL)
- **Linux** (tested on Ubuntu)
- **macOS**  

The tool automatically detects your operating system and uses the appropriate method to move files to the Recycle Bin safely. On unsupported systems, the recycle functionality will fallback to a safe operation using the `send2trash` Python package, which also ensures files are not permanently deleted.

## Usage

Run the program from the project root directory:

`uv run python3 review_demo.py`

The program will scan the configured Downloads folder and display a categorized tree view of the files it finds.

**Example:**
```
Review Files (Category)
├── TEMPORARY
│   ├── temp.tmp
│   ├── download.crdownload
│   └── partial.part
├── INSTALLER
│   ├── setup.exe
│   └── old_installer.msi
├── DOCUMENT
│   ├── resume.pdf
│   └── notes.docx
└── MEDIA
    ├── image.jpg
    └── video.mp4
```

### File Recommendations
After scanning and categorizing files, the tool analyzes them and recommends files that may be safe candidates for cleanup.

**Example:**
```
6 file(s) recommended for recycling:

 - temp.tmp
 - download.crdownload
 - partial.part
 - setup.exe
 - old_installer.msi
 - backup.zip
```

### Recycling Files
The tool will ask for confirmation before moving any files:
```
Move 6 recommended file(s) to Recycle Bin? (Yes/No):
```

Enter `Yes` to move the recommended files to the operating system's Recycle Bin. Else, enter `No` to leave all files unchanged.

Files are never permanently deleted by the tool.

### Reviewing Files via Different Sorting Options
After the recycling recommendation, the program allows files to be viewed using different grouping options:

```
Sort options:
 - category
 - age
 - extension
 - duplicates
```

**Category View**
Groups files by file type categories such as:

- Documents
- Media
- Installers
- Archives
- Temporary Files
- Unknown Files

**Age View**
Groups files by age ranges:

- Last 30 Days
- 30–90 Days
- 90–180 Days
- 6–12 Months
- Over 1 Year

**Extension View**
Groups files by file extension:

- .pdf
- .docx
- .zip
- .mp4

**Duplicates View**
Displays files with duplicate names together to help identify redundant files.

### Exiting the Program

When prompted for a sort option, enter `exit` to close the program.

## Safety Features
- Files are moved to the operating system's Recycle Bin instead of being permanently deleted.
- User confirmation is required before any files are recycled.
- A sandbox test dataset is available for safe development and testing.
- Duplicate files, installers, archives, and temporary files can be reviewed before any action is taken.
