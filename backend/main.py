from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from backend.database import (
    SessionLocal,
    SearchHistory
)


# -----------------------------
# CREATE FASTAPI APP
# -----------------------------

app = FastAPI(
    title="RAG Chatbot History API"
)


# -----------------------------
# REQUEST MODEL
# -----------------------------

class SearchRequest(BaseModel):

    query: str


# -----------------------------
# TEST ENDPOINT
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "RAG History Backend is running"
    }

# -----------------------------
# ADD SEARCH HISTORY (NO DUPLICATES)
# -----------------------------
@app.post("/history")
def add_history(request: SearchRequest):

    db = SessionLocal()

    clean_query = request.query.strip()

    # Check if query already exists in history
    existing = (
        db.query(SearchHistory)
        .filter(SearchHistory.query == clean_query)
        .first()
    )

    if existing:
        # Update timestamp to bring it to top without creating a duplicate
        existing.timestamp = datetime.now()
        db.commit()
        db.refresh(existing)
        db.close()

        return {
            "message": "Search updated",
            "id": existing.id,
            "query": existing.query,
            "timestamp": existing.timestamp
        }

    # If new, insert into database
    history = SearchHistory(
        query=clean_query
    )

    db.add(history)
    db.commit()
    db.refresh(history)
    db.close()

    return {
        "message": "Search saved",
        "id": history.id,
        "query": history.query,
        "timestamp": history.timestamp
    }


# -----------------------------
# GET RECENT SEARCHES
# -----------------------------

@app.get("/history")
def get_history():

    db = SessionLocal()

    history = (
        db.query(SearchHistory)
        .order_by(
            SearchHistory.timestamp.desc()
        )
        .limit(10)
        .all()
    )

    db.close()

    return [
        {
            "id": item.id,
            "query": item.query,
            "timestamp": item.timestamp
        }
        for item in history
    ]


# -----------------------------
# DELETE SINGLE SEARCH
# -----------------------------

@app.delete("/history/{item_id}")
def delete_single_history(item_id: int):

    db = SessionLocal()

    item = (
        db.query(SearchHistory)
        .filter(SearchHistory.id == item_id)
        .first()
    )

    if item:
        db.delete(item)
        db.commit()

    db.close()

    return {
        "message": f"Deleted history item {item_id}"
    }


# -----------------------------
# CLEAR ALL SEARCH HISTORY
# -----------------------------

@app.delete("/history")
def clear_all_history():

    db = SessionLocal()

    db.query(SearchHistory).delete()

    db.commit()

    db.close()

    return {
        "message": "All search history cleared"
    }