
import streamlit as st

from database import (
    create_table,
    save_feedback,
    get_all_feedback,
    get_feedback_category_counts,
    get_feedback_priority_counts,
)

from ai_helper import categorize_feedback, suggest_priority

create_table()
st.set_page_config(
    page_title="CampusCare AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 CampusCare AI")

st.subheader("Your Student Support & Campus Guide")

st.write(
    "Helping students find guidance, share feedback, "
    "and report campus problems."
)

st.header("Student Feedback")

st.write("Share your campus-related concerns with us.")

issue = st.selectbox(
    "What issue are you experiencing?",
    ["Hostel Facilities", "Water Supply", "Internet", "Academic Support", "Other"]
)

feedback = st.text_area("Describe your issue")


if feedback.strip():
    suggested_category = categorize_feedback(feedback)
    suggested_priority = suggest_priority(feedback)

    st.info(f"Suggested category: {suggested_category}")
    st.write(f"Suggested priority: {suggested_priority}")
st.write("Selected issue:", issue)



if st.button("Submit Feedback"):
    if feedback.strip():
        suggested_category = categorize_feedback(feedback)
        suggested_priority = suggest_priority(feedback)

        save_feedback(
            issue,
            feedback,
            suggested_category,
            suggested_priority
        )

        st.success("Your feedback has been saved successfully!")

        st.write("Selected issue:", issue)
        st.write("AI-suggested category:", suggested_category)
        st.write("Suggested priority:", suggested_priority)
        st.write("Your feedback:", feedback)
    else:
        st.warning("Please describe your issue before submitting.")



st.header("Feedback History")

records = get_all_feedback()


if records:
    categories = sorted(
        set(record[3] for record in records)
    )

    selected_category = st.selectbox(
        "Filter feedback by AI-suggested category",
        ["All Categories"] + categories,
    )

    
    selected_priority = st.selectbox(
        "Filter feedback by priority",
        ["All Priorities", "High", "Normal"],
    )

    
    if selected_category != "All Categories":
        records = [
            record for record in records
            if record[3] == selected_category
        ]



    
    if selected_priority != "All Priorities":
        records = [
            record for record in records
            if record[4] == selected_priority
        ]



st.subheader("Feedback Summary")

total_feedback = len(records)

st.metric(
    label="Feedback Matching Filters",
    value=total_feedback
)



priority_counts = get_feedback_priority_counts()

priority_summary = {
    priority: count
    for priority, count in priority_counts
}


high_priority_count = priority_summary.get("High", 0)
normal_priority_count = priority_summary.get("Normal", 0)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="High Priority Feedback",
        value=high_priority_count
    )

with col2:
    st.metric(
        label="Normal Priority Feedback",
        value=normal_priority_count
    )



st.subheader("Priority Distribution")

priority_chart_data = {
    "Priority": ["High", "Normal"],
    "Number of Submissions": [
        high_priority_count,
        normal_priority_count,
    ],
}

st.bar_chart(
    priority_chart_data,
    x="Priority",
    y="Number of Submissions",
)



st.subheader("Feedback by Category")

category_counts = get_feedback_category_counts()

if category_counts:
    st.dataframe(
        [
            {
                "AI-suggested Category": category,
                "Number of Submissions": count,
            }
            for category, count in category_counts
        ],
        use_container_width=True,
    )



    
    st.subheader("Category Distribution")

    chart_data = {
        "Category": [category for category, count in category_counts],
        "Submissions": [count for category, count in category_counts],
    }

    st.bar_chart(
        chart_data,
        x="Category",
        y="Submissions",
    )

else:
    st.info("No feedback categories are available yet.")




def clear_feedback_search():
    st.session_state.feedback_search = ""

st.button(
    "Clear Search",
    on_click=clear_feedback_search,
)

feedback_search = st.text_input(
    "Search feedback descriptions",
    placeholder="Enter a keyword to search feedback",
    key="feedback_search",
)


if feedback_search.strip():
    records = [
        record for record in records
        if feedback_search.strip().lower()
        in (record[1] + " " + record[2]).lower()
    ]


st.caption(f"Matching feedback records: {len(records)}")





if records:
    feedback_table = [
        {
            "Feedback ID": record[0],
            "Issue": record[1],
            "Description": record[2],
            "AI-suggested Category": record[3],
            "Suggested Priority": record[4],
            "Submitted At": str(record[5]),
        }
        for record in records
    ]

    st.dataframe(
        feedback_table,
        use_container_width=True,
    )

else:
    st.info("No feedback matches the selected filters or search.")









st.header("🎓 Student Guide")

st.write(
    "Find helpful guidance for common campus-related questions."
)

guide_topic = st.selectbox(
    "Choose a guidance topic",
    [
        "Hostel Facilities",
        "Water Supply",
        "Internet",
        "Academic Support",
        "General Campus Guidance",
    ],
)

if guide_topic == "Hostel Facilities":
    st.info(
        "For hostel-related concerns, contact your hostel "
        "warden or the appropriate campus office."
    )

elif guide_topic == "Water Supply":
    st.info(
        "For water supply problems, report the issue to "
        "the responsible campus maintenance team."
    )

elif guide_topic == "Internet":
    st.info(
        "For internet connectivity problems, contact your "
        "campus IT support team."
    )

elif guide_topic == "Academic Support":
    st.info(
        "For academic guidance, contact your faculty advisor "
        "or the appropriate academic office."
    )

else:
    st.info(
        "For general campus guidance, consult your institute's "
        "official website or student support office."
    )






st.subheader("❓ Frequently Asked Questions")

faq_items = {
    "How do I report a campus problem?":
        "Use the Student Feedback section to describe your campus-related concern and submit it.",

    "How can I get academic guidance?":
        "Select Academic Support in the Student Guide and contact your faculty advisor or the appropriate academic office.",

    "What should I do about an urgent safety issue?":
        "Contact the appropriate campus emergency or safety personnel immediately. Do not rely on this prototype as an emergency response service.",

    "How do I get help with internet problems?":
        "Select Internet in the Student Guide and contact your campus IT support team.",
}

faq_search = st.text_input(
    "Search FAQs",
    placeholder="Type a keyword, e.g. internet or academic",
)

matching_faqs = {
    question: answer
    for question, answer in faq_items.items()
    if faq_search.strip().lower() in (
        question + " " + answer
    ).lower()
}

if matching_faqs:
    for question, answer in matching_faqs.items():
        with st.expander(question):
            st.write(answer)
else:
    st.info("No matching FAQs found. Try another keyword.")






st.subheader("📞 Campus Support Directory")

support_contacts = [
    {
        "Support Area": "Hostel Facilities",
        "Contact": "Hostel Warden",
        "Purpose": "Hostel-related concerns",
    },
    {
        "Support Area": "Internet",
        "Contact": "Campus IT Support",
        "Purpose": "Internet and network issues",
    },
    {
        "Support Area": "Academic Support",
        "Contact": "Faculty Advisor",
        "Purpose": "Academic guidance",
    },
    {
        "Support Area": "Water Supply",
        "Contact": "Campus Maintenance Team",
        "Purpose": "Water and maintenance issues",
    },
    {
        "Support Area": "General Guidance",
        "Contact": "Student Support Office",
        "Purpose": "General campus assistance",
    },
]

st.dataframe(
    support_contacts,
    use_container_width=True,
)






st.subheader("📊 Campus Issue Overview")

overview_counts = get_feedback_category_counts()

if overview_counts:
    st.write("Current feedback by campus issue category:")

    for category, count in overview_counts:
        st.write(f"- **{category}:** {count} submission(s)")
else:
    st.info(
        "No feedback has been submitted yet. "
        "The issue overview will appear when feedback is available."
    )
