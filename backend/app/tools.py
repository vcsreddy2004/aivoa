# app/tools.py
from typing import Dict
from app.db import get_connection
import json


# ---------------------------
# LOG INTERACTION (INSERT)
# ---------------------------
def log_interaction(data: Dict):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO interactions 
        (hcp_name, interaction_type, date, time, attendees, topics, materials, samples, sentiment, outcomes, follow_up)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data.get("hcp_name"),
        data.get("interaction_type"),
        data.get("date"),
        data.get("time"),
        json.dumps(data.get("attendees", [])),
        data.get("topics"),
        data.get("materials"),
        data.get("samples"),
        data.get("sentiment"),
        data.get("outcomes"),
        data.get("follow_up"),
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "saved", "data": data}


# ---------------------------
# EDIT INTERACTION (UPDATE)
# ---------------------------
def edit_interaction(data: Dict):
    conn = get_connection()
    cursor = conn.cursor()

    query = 'UPDATE interactions SET sentiment=%s, outcomes=%s, follow_up=%s WHERE hcp_name=%s ORDER BY id DESC LIMIT 1'

    cursor.execute(query, (
        data.get("sentiment"),
        data.get("outcomes"),
        data.get("follow_up"),
        data.get("hcp_name"),
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "updated", "data": data}


# ---------------------------
# GET HCP HISTORY
# ---------------------------
def get_hcp_history(name: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if name:
        cursor.execute(
            "SELECT * FROM interactions WHERE hcp_name=%s ORDER BY created_at DESC",
            (name,)
        )
    else:
        cursor.execute(
            "SELECT * FROM interactions ORDER BY created_at DESC"
        )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"history": results}


# ---------------------------
# FOLLOW-UP SUGGESTION
# ---------------------------
def suggest_followup(data: Dict):
    sentiment = data.get("sentiment")
    topics = (data.get("topics") or "").lower()
    outcomes = (data.get("outcomes") or "").lower()

    if sentiment == "Positive":
        if "interested" in outcomes:
            return {"suggestion": "Send product samples and schedule demo in 3 days"}
        return {"suggestion": "Schedule follow-up in 1 week"}

    elif sentiment == "Negative":
        return {"suggestion": "Re-engage with different strategy or senior doctor visit"}

    else:
        if "price" in topics:
            return {"suggestion": "Share pricing details and follow up in 3 days"}
        return {"suggestion": "Follow up in 2 weeks"}


# ---------------------------
# SUMMARIZE
# ---------------------------
def summarize_interaction(text: str):
    return {"summary": text[:100]}