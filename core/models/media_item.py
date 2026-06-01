from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class MediaItem:
    path: str
    date_taken: datetime
    # thumbnail: str
    # tags: List[str]
    # location: Optional[str]

    @staticmethod
    def create_table() -> str:
        return """
            CREATE TABLE IF NOT EXISTS media_item (
                id TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                date_taken TIMESTAMP
            )
        """
