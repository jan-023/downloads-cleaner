from enum import Enum

class Category(Enum):
    INSTALLER = "installer"
    ARCHIVE = "archive"
    DOCUMENT = "document"
    MEDIA = "media"
    TEMPORARY = "temporary"
    UNKNOWN = "unknown"

