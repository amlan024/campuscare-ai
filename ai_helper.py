
import json
from pathlib import Path


def categorize_feedback(feedback):
    text = feedback.lower()

    if "water" in text:
        return "Water Supply"
    elif "wifi" in text or "internet" in text:
        return "Internet"
    elif "hostel" in text or "room" in text:
        return "Hostel Facilities"
    elif any(word in text for word in [
        "academic", "course", "study", "faculty",
        "advisor", "elective", "semester",
    ]):
        return "Academic Support"
    else:
        return "Other"


def suggest_priority(feedback):
    text = feedback.lower()
    high_priority_words = [
        "emergency", "urgent", "danger", "unsafe", "severe",
    ]

    for word in high_priority_words:
        if word in text:
            return "High"

    return "Normal"


def retrieve_campus_knowledge(question, limit=3):
    """Retrieve campus knowledge using keyword relevance."""
    knowledge_path = Path(__file__).parent / "campus_knowledge.json"

    with knowledge_path.open("r", encoding="utf-8") as file:
        knowledge = json.load(file)

    question_words = {
        word.strip(".,?!:;()[]{}").lower()
        for word in question.split()
    }
    question_words = {
        word for word in question_words if len(word) > 2
    }

    topic_keywords = {
        "Academic Support": {
            "academic", "course", "study", "faculty",
            "advisor", "advising", "elective", "semester",
        },
        "Internet": {
            "wifi", "internet", "network", "connection",
        },
        "Hostel Facilities": {
            "hostel", "room", "warden",
        },
        "Water Supply": {
            "water", "supply", "tap",
        },
    }

    results = []

    for item in knowledge:
        searchable_text = (
            item["topic"] + " "
            + item["question"] + " "
            + item["answer"]
        ).lower()

        searchable_words = {
            word.strip(".,?!:;()[]{}")
            for word in searchable_text.split()
        }

        score = len(question_words & searchable_words)

        keywords = topic_keywords.get(item["topic"], set())
        if question_words & keywords:
            score += 5

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda result: result[0], reverse=True)

    return [item for score, item in results[:limit]]


def generate_campus_answer(question, knowledge_entries, api_key):
    """Generate an answer grounded in retrieved campus knowledge."""
    from google import genai

    client = genai.Client(api_key=api_key)

    context_parts = []

    for entry in knowledge_entries:
        context_parts.append(
            f"Topic: {entry['topic']}\n"
            f"Question: {entry['question']}\n"
            f"Answer: {entry['answer']}\n"
            f"Source: {entry['source']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are CampusCare AI, a student campus guidance assistant.

Answer using only the campus knowledge provided.
Do not invent campus policies or contact details.
If the information is insufficient, say so.
Do not present sample guidance as verified official policy.
Keep the answer concise and identify the source.

CAMPUS KNOWLEDGE:
{context}

STUDENT QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )

    answer = response.text

    if not answer:
        return "I couldn't generate an answer. Please try again."

    return answer
