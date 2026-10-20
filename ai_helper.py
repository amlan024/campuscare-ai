def categorize_feedback(feedback):
    text = feedback.lower()

    if "water" in text:
        return "Water Supply"

    elif "wifi" in text or "internet" in text:
        return "Internet"

    elif "hostel" in text or "room" in text:
        return "Hostel Facilities"

    elif any(word in text for word in [
        "academic",
        "course",
        "study",
        "faculty",
        "advisor",
        "elective",
        "semester",
    ]):
        return "Academic Support"

    else:
        return "Other"




def suggest_priority(feedback):
    text = feedback.lower()

    high_priority_words = [
        "emergency",
        "urgent",
        "danger",
        "unsafe",
        "severe",
    ]

    for word in high_priority_words:
        if word in text:
            return "High"

    return "Normal"





import json
from pathlib import Path


def retrieve_campus_knowledge(question, limit=3):
    """Retrieve relevant campus knowledge entries for a question."""
    knowledge_path = Path(__file__).parent / "campus_knowledge.json"

    with knowledge_path.open("r", encoding="utf-8") as file:
        knowledge = json.load(file)

    question_words = set(question.lower().split())
    question_words = {
        word.strip(".,?!:;()[]{}")
        for word in question_words
        if len(word.strip(".,?!:;()[]{}")) > 2
    }

    results = []

    for item in knowledge:
        searchable_text = (
            item["topic"] + " "
            + item["question"] + " "
            + item["answer"]
        ).lower()

        searchable_words = set(searchable_text.split())
        searchable_words = {
            word.strip(".,?!:;()[]{}")
            for word in searchable_words
        }

        score = len(question_words & searchable_words)

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda result: result[0], reverse=True)

    return [
        item for score, item in results[:limit]
    ]
