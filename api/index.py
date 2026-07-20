import random
import sys
import os
from typing import Optional, List

# Allow importing data.py from the project root
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from data import all_items, items_by_id

app = FastAPI(title="AI vs Human Quiz API")

# Allow your future Django frontend (running on a different domain) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your Django domain once you deploy it
    allow_methods=["*"],
    allow_headers=["*"],
)


def strip_answer(item: dict) -> dict:
    """Return a copy of an item WITHOUT the source or explanation,
    so the player can't peek at the answer before guessing.

    Text items store their data in 'content'; image/video items store it in 'link'.
    We normalize both into a single 'value' field so the API response shape
    is consistent no matter the content_type.
    """
    value = item.get("content") if item["content_type"] == "text" else item.get("link")

    return {
        "id": item["id"],
        "value": value,
        "difficulty": item["difficulty"],
        "content_type": item["content_type"],
    }


def filter_items(difficulty: Optional[str] = None) -> List[dict]:
    """Filter the full item pile by difficulty.
    Leave difficulty out to mean 'any'."""
    if not difficulty:
        return all_items

    return [i for i in all_items if i["difficulty"] == difficulty.lower()]


@app.get("/")
def root():
    return {"message": "AI vs Human quiz API is running"}


@app.get("/quiz/random")
def get_random_question(
    difficulty: Optional[str] = Query(None, description="easy, medium, or hard"),
):
    """Return one random item, optionally filtered by difficulty.
    The source/explanation are hidden until the player guesses.
    """
    pool = filter_items(difficulty)

    if not pool:
        raise HTTPException(
            status_code=404,
            detail="No items match that difficulty.",
        )

    item = random.choice(pool)
    return strip_answer(item)


@app.get("/quiz/random/{count}")
def get_random_questions(
    count: int,
    difficulty: Optional[str] = Query(None, description="easy, medium, or hard"),
):
    """Return `count` random, non-duplicate items, optionally filtered by difficulty."""
    pool = filter_items(difficulty)

    if not pool:
        raise HTTPException(
            status_code=404,
            detail="No items match that difficulty.",
        )

    # Don't let someone ask for more cards than actually exist in the filtered pool
    count = min(count, len(pool))

    items = random.sample(pool, count)
    return [strip_answer(item) for item in items]


@app.get("/quiz/all")
def get_all_questions(
    difficulty: Optional[str] = Query(None, description="easy, medium, or hard"),
):
    """Return every item that matches the filter, WITHOUT the source."""
    pool = filter_items(difficulty)
    return [strip_answer(item) for item in pool]


@app.get("/quiz/answer")
def check_answer(id: str, guess: str):
    """Check a guess ('AI' or 'Human') against the real source for a given item id."""
    item = items_by_id.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    correct = item["source"].lower() == guess.lower()
    return {
        "correct": correct,
        "actual_source": item["source"],
        "explanation": item["explanation"],
    }


@app.get("/quiz/stats")
def get_stats():
    """Return a count of how many items exist per difficulty and content_type.
    Handy for checking your dataset is filled in evenly while you're building it out.
    """
    stats = {}
    for item in all_items:
        difficulty = item["difficulty"]
        content_type = item["content_type"]
        stats.setdefault(difficulty, {})
        stats[difficulty].setdefault(content_type, 0)
        stats[difficulty][content_type] += 1
    return stats
