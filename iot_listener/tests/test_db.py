from app.db.mongodb import MongoDB

def test_mongodb_save():
    db = MongoDB("mongodb://localhost:27017", "test_db")
    result = db.save({"test": "data"})
    assert result.inserted_id is not None