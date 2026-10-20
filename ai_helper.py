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

