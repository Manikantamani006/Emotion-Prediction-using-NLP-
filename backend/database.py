import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent / "history.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database with the analysis history schema."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                predicted_emotion TEXT NOT NULL,
                confidence REAL NOT NULL,
                probabilities TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def add_history_entry(text: str, predicted_emotion: str, confidence: float, probabilities: Dict[str, float]) -> Dict[str, Any]:
    """Adds a newly analyzed text record to SQLite database."""
    now_iso = datetime.now(timezone.utc).isoformat()
    probs_json = json.dumps(probabilities)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_history (text, predicted_emotion, confidence, probabilities, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (text, predicted_emotion, confidence, probs_json, now_iso))
        conn.commit()
        record_id = cursor.lastrowid

    return {
        "id": record_id,
        "text": text,
        "predicted_emotion": predicted_emotion,
        "confidence": confidence,
        "probabilities": probabilities,
        "created_at": now_iso
    }

def get_history(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Returns stored history records in reverse chronological order."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, text, predicted_emotion, confidence, probabilities, created_at
            FROM analysis_history
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        rows = cursor.fetchall()

    history = []
    for row in rows:
        try:
            probs = json.loads(row["probabilities"])
        except Exception:
            probs = {}
        history.append({
            "id": row["id"],
            "text": row["text"],
            "predicted_emotion": row["predicted_emotion"],
            "confidence": row["confidence"],
            "probabilities": probs,
            "created_at": row["created_at"]
        })
    return history

def clear_history() -> int:
    """Clears all analysis history records from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM analysis_history")
        count = cursor.fetchone()[0]
        cursor.execute("DELETE FROM analysis_history")
        conn.commit()
    return count

def get_stats() -> Dict[str, Any]:
    """Returns summary statistics for the history dashboard."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(confidence) FROM analysis_history")
        total, avg_conf = cursor.fetchone()

        cursor.execute("""
            SELECT predicted_emotion, COUNT(*) as count
            FROM analysis_history
            GROUP BY predicted_emotion
            ORDER BY count DESC
            LIMIT 1
        """)
        top_emo_row = cursor.fetchone()
        dominant_emotion = top_emo_row[0] if top_emo_row else "None"
        dominant_count = top_emo_row[1] if top_emo_row else 0

    return {
        "total_records": total or 0,
        "avg_confidence": round(avg_conf, 4) if avg_conf else 0.0,
        "dominant_emotion": dominant_emotion,
        "dominant_count": dominant_count
    }
