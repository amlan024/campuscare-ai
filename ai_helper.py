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

Answer the student's question using only the campus knowledge below.

Rules:
- Do not invent campus policies or contact details.
- If the knowledge is insufficient, clearly say so.
- Do not present sample guidance as verified official policy.
- Keep the answer helpful and concise.
- Identify the source used.

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
