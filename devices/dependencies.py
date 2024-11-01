from database import get_session


def get_db():
    db = next(get_session())
    try:
        yield db
    finally:
        db.close()
