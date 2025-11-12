import os
from dotenv import load_dotenv
import google.generativeai as genai
from langgraph.graph import StateGraph, END
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(state):
    topic = state["topic"]

    prompt = f"""
    Generate a multiple-choice quiz question about the topic: {topic}.
    Only return a valid JSON (no markdown, no explanations).
    Example:
    {{
        "question": "...",
        "correct_answer": "...",
        "distractors": ["...", "...", "..."]
    }}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print("Gemini returned invalid JSON:", text)
        return state

    state["question"] = data.get("question")
    state["correct_answer"] = data.get("correct_answer")
    state["distractors"] = data.get("distractors")
    return state

graph = StateGraph(dict)
graph.add_node("quiz", generate_quiz)
graph.set_entry_point("quiz")
graph.add_edge("quiz", END)

app = graph.compile()

def get_quiz(topic: str):
    result = app.invoke({"topic": topic})
    return {
        "question": result["question"],
        "correct_answer": result["correct_answer"],
        "distractors": result["distractors"]
    }
