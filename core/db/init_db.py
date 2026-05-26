from contextlib import contextmanager
from platformdirs import user_documents_path
import sqlite3
from core.models import MediaItem

db_path = user_documents_path() / "Picture Book" / "picture-book.sqlite3"


def init_db() -> None:
    if not db_path.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(db_path)
    db.execute(MediaItem.create_table())
    db.close()


@contextmanager
def db():
    with sqlite3.connect(db_path) as conn:
        yield conn
