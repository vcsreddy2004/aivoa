# ---------------------------
# 1. IMPORTS & CONFIG
# ---------------------------
import os
import json
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from langgraph.graph import StateGraph

from app.tools import (
    log_interaction,
    edit_interaction,
    get_hcp_history,
    suggest_followup
)

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------
# 2. LLM CALL
# ---------------------------
def call_llm(text: str) -> Dict:
    prompt = f"""
    You are an AI assistant for a pharmaceutical CRM system. 
    Extract structured data from the interaction text.
    
    Rules: 
    HCP Name = main doctor/person being met 
    interaction_type = Meeting | Call | Visit
    date = given date in strict order dd-mm-yyyy 
    Attendees = all people mentioned 
    Materials = items like laptop, brochure, projector, samples 
    Convert time to HH:MM format 
    Sentiment = Positive, Neutral, or Negative 
    Return ONLY valid JSON:

    {{
      "hcp_name": "",
      "interaction_type": "",
      "date": "",
      "time": "",
      "attendees": [],
      "topics": "",
      "materials": "",
      "samples": "",
      "sentiment": "Positive | Neutral | Negative",
      "outcomes": "",
      "follow_up": ""
    }}

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content

    # Clean response
    if content:
        content = content.strip()
        content = content.replace("```json", "").replace("```", "")
        content = content.replace("\n", " ").strip()

    try:
        return json.loads(content)
    except:
        print("JSON Parse Failed:", content)
        return {}


# ---------------------------
# 3. HELPER FUNCTIONS
# ---------------------------
def call_llm_with_retry(text: str, retries: int = 2):
    for attempt in range(retries):
        data = call_llm(text)

        if isinstance(data, dict) and len(data) > 0:
            return data

        print(f"[Retry] Attempt {attempt+1} failed")

    return {}


def detect_intent(text: str) -> str:
    text = text.lower()

    if "edit" in text or "change" in text or "update" in text:
        return "edit"
    elif "history" in text or "previous" in text:
        return "history"
    elif "follow" in text or "suggest" in text:
        return "followup"
    else:
        return "log"

# ---------------------------
# 4. NODES
# ---------------------------

# Extract
def extract_node(state):
    text = state["text"]
    return {"text": text,"data": call_llm_with_retry(text)}


# Validate
def validate_node(state):
    data = state["data"]
    text = state["text"]

    defaults = {
        "hcp_name": None,
        "interaction_type": "Meeting",
        "date": "",
        "time": "",
        "attendees": [],
        "topics": "",
        "materials": "None",
        "samples": "None",
        "sentiment": "Neutral",
        "outcomes": "",
        "follow_up": "Follow up in 2 weeks"
    }

    for key, value in defaults.items():
        if key not in data or not data[key]:
            data[key] = value

    if data["sentiment"] not in ["Positive", "Neutral", "Negative"]:
        data["sentiment"] = "Neutral"

    if not data["date"]:
        data["date"] = datetime.now().strftime("%Y-%m-%d")

    if not data["time"]:
        data["time"] = datetime.now().strftime("%H:%M")

    return {"text": text,"data": data}


# Route
def route_node(state):
    return {
        "text": state["text"],
        "intent": detect_intent(state["text"]),
        "data": state["data"]
    }


# Tool Nodes
def log_node(state):
    return {"data": log_interaction(state["data"])["data"]}


def edit_node(state):
    return {"data": edit_interaction(state["data"])["data"]}


def history_node(state):
    return {"data": get_hcp_history(state["data"].get("hcp_name"))}


def followup_node(state):
    return {"data": suggest_followup(state["data"])}


# ---------------------------
# 5. GRAPH BUILD
# ---------------------------
graph = StateGraph(dict)

# Add nodes
graph.add_node("extract", extract_node)
graph.add_node("validate", validate_node)
graph.add_node("route", route_node)

graph.add_node("log", log_node)
graph.add_node("edit", edit_node)
graph.add_node("history", history_node)
graph.add_node("followup", followup_node)

# Entry
graph.set_entry_point("extract")

# Flow
graph.add_edge("extract", "validate")
graph.add_edge("validate", "route")

# Conditional routing
graph.add_conditional_edges(
    "route",
    lambda state: state["intent"],
    {
        "log": "log",
        "edit": "edit",
        "history": "history",
        "followup": "followup",
    }
)

app_graph = graph.compile()