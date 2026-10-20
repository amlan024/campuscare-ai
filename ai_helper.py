
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
    """Retrieve campus guidance relevant to the question."""
    import json
    from pathlib import Path

    knowledge_path = Path(__file__).parent / "campus_knowledge.json"

    with knowledge_path.open("r", encoding="utf-8") as file:
        knowledge = json.load(file)

    text = question.lower()

    topic_keywords = {
        "Academic Support": [
            "academic", "guidance", "advisor", "faculty",
            "course", "study", "elective", "semester",
        ],
        "Internet": [
            "wifi", "wi-fi", "internet", "network", "connectivity",
        ],
        "Hostel Facilities": [
            "hostel", "warden", "dormitory", "room",
        ],
        "Water Supply": [
            "water", "supply", "tap", "drinking water",
        ],
    }

    matching_topics = [
        topic for topic, keywords in topic_keywords.items()
        if any(keyword in text for keyword in keywords)
    ]

    results = []

    for item in knowledge:
        topic = item.get("topic", "")

        if matching_topics:
            if topic in matching_topics:
                results.append((10, item))
            continue

        searchable_text = (
            item.get("question", "") + " "
            + item.get("answer", "") + " "
            + topic
        ).lower()

        words = {
            word.strip(".,?!:;()[]{}")
            for word in text.split()
            if len(word.strip(".,?!:;()[]{}")) > 3
        }

        score = sum(
            1 for word in words if word in searchable_text
        )

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
