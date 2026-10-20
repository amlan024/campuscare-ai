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






def retrieve_campus_knowledge(question, limit=3):
    """Retrieve campus knowledge using keyword relevance."""
    import json
    from pathlib import Path

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
        "Internet": {"wifi", "internet", "network", "connection"},
        "Hostel Facilities": {"hostel", "room", "warden"},
        "Water Supply": {"water", "supply", "tap"},
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
