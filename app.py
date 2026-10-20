
import streamlit as st
import pandas as pd
from database import (
    create_table,
    save_feedback,
    get_all_feedback,
    get_feedback_category_counts,
    get_feedback_priority_counts,
)

from ai_helper import categorize_feedback, suggest_priority

create_table()
if "submission_processed" not in st.session_state:
    st.session_state.submission_processed = False

def reset_submission_state():
    st.session_state.submission_processed = False
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
    [
        "Hostel Facilities",
        "Water Supply",
        "Internet",
        "Academic Support",
        "Other",
    ],
    help="Choose the category that best describes your campus-related concern.",
)


feedback = st.text_area(
    "Describe your issue",
    max_chars=1000,
    help=(
        "Explain what happened, where the campus issue occurs, "
        "and what support is needed. Use up to 1,000 characters. "
        "Do not include sensitive personal information."
    ),
    placeholder=(
        "Example: The internet connection in the hostel study "
        "area has been slow since yesterday."
    ),
    key="feedback_input",
    on_change=reset_submission_state,
)
st.caption(
    f"Characters used: {len(feedback)} / 1000"
)


if feedback.strip():
    suggested_category = categorize_feedback(feedback)
    suggested_priority = suggest_priority(feedback)

    st.info(f"Suggested category: {suggested_category}")
    st.caption(
        "The suggested category is generated using predefined "
        "rules. Please review it because some descriptions may "
        "be categorized incorrectly."
    )
    st.write(f"Suggested priority: {suggested_priority}")
    st.caption(
        "Priority is a rule-based suggestion and may not always "
        "be accurate. For emergencies, contact campus emergency "
        "or safety personnel directly."
    )
st.write("Selected issue:", issue)



st.caption(
    "Please review your description before submitting. "
    "Use sample, non-sensitive feedback while testing."
)

st.warning(
    "Privacy reminder: Do not include passwords, student ID "
    "numbers, financial details, or other sensitive personal "
    "information. Use sample, non-sensitive feedback while "
    "testing this prototype."
)


confirm_submission = st.checkbox(
    "I confirm that my feedback is accurate and contains no sensitive personal information.",
    key="confirm_submission",
    help="Please review your description before submitting. Do not include passwords, student IDs, or financial details.",
)

if st.button(
    "Submit Feedback",
    disabled=(
        not feedback.strip()
        or not confirm_submission
        or st.session_state.submission_processed
    ),
):
    if feedback.strip():
        suggested_category = categorize_feedback(feedback)
        suggested_priority = suggest_priority(feedback)

        save_feedback(
            issue,
            feedback,
            suggested_category,
            suggested_priority
        )

        st.session_state.submission_processed = True
        
        
        st.success(
            "Thank you! Your feedback has been saved successfully."
        )
        st.info(
            "Your feedback is now included in the campus feedback "
            "records and relevant summary statistics."
        )
        st.caption(
            f"Submission time: {get_all_feedback()[0][5]}"
        )


        st.write("Selected issue:", issue)
        st.write("AI-suggested category:", suggested_category)
        st.write("Suggested priority:", suggested_priority)
    else:
        st.warning("Please describe your issue before submitting.")



def refresh_feedback_data():
    st.session_state["feedback_input"] = ""
    st.session_state["confirm_submission"] = False
    st.session_state["submission_processed"] = False


st.button(
    "Refresh Feedback Data",
    on_click=refresh_feedback_data,
)

st.header("Feedback History")
st.caption(
    "Review submitted campus feedback, explore categories and "
    "priorities, and search records using keywords."
)

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


st.subheader("Priority Summary")
st.caption(
    "These counts are based on rule-based priority suggestions. "
    "They are indicators for review, not verified assessments "
    "of risk or urgency."
)

priority_summary_table = [
    {
        "Priority": "High",
        "Number of Submissions": high_priority_count,
    },
    {
        "Priority": "Normal",
        "Number of Submissions": normal_priority_count,
    },
]

priority_summary_df = pd.DataFrame(priority_summary_table)

st.dataframe(
    priority_summary_df,
    use_container_width=True,
)

priority_csv = priority_summary_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Priority Summary as CSV",
    data=priority_csv,
    file_name="campuscare_priority_summary.csv",
    mime="text/csv",
)



st.subheader("Priority Distribution")
st.caption(
    "This chart shows the number of submitted feedback records "
    "assigned each rule-based priority level."
)

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
st.caption(
    "Categories are suggested by predefined rules. "
    "Review the original feedback before drawing conclusions "
    "about campus-wide problems."
)

category_counts = get_feedback_category_counts()

if category_counts:
    category_summary = [
        {
            "AI-suggested Category": category,
            "Number of Submissions": count,
        }
        for category, count in category_counts
    ]

    st.dataframe(
        category_summary,
        use_container_width=True,
    )

    category_summary_df = pd.DataFrame(category_summary)

    category_csv = category_summary_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Category Summary as CSV",
        data=category_csv,
        file_name="campuscare_category_summary.csv",
        mime="text/csv",
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

    feedback_df = pd.DataFrame(feedback_table)

    csv_data = feedback_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Feedback as CSV",
        data=csv_data,
        file_name="campuscare_feedback.csv",
        mime="text/csv",
    )


else:
    st.info(
        "No feedback matches your current filters or search. "
        "Try changing the category, priority, or search keyword."
    )








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
        "Urgent Safety Issue",
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

elif guide_topic == "Urgent Safety Issue":
    st.error(
        "URGENT SAFETY CONCERN: Contact campus security or "
        "the appropriate campus authority immediately. "
        "If someone is in immediate danger, move to a safe "
        "place and contact local emergency services. "
        "Do not rely on this app for emergency assistance."
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
    "Search frequently asked questions",
    placeholder="Try internet, academics, or campus support...",
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

support_df = pd.DataFrame(support_contacts)

st.dataframe(
    support_df,
    use_container_width=True,
)

support_csv = support_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Support Directory as CSV",
    data=support_csv,
    file_name="campuscare_support_directory.csv",
    mime="text/csv",
)






st.subheader("📊 Campus Issue Overview")
st.caption(
    "View aggregated feedback counts by category to identify "
    "common campus concerns. These counts represent submitted "
    "feedback, not verified incidents."
)

overview_counts = get_feedback_category_counts()

if overview_counts:
    st.write("Current feedback by campus issue category:")

    overview_table = [
        {
            "Category": category,
            "Number of Submissions": count,
        }
        for category, count in overview_counts
    ]

    for item in overview_table:
        st.write(
            f"- **{item['Category']}:** "
            f"{item['Number of Submissions']} submission(s)"
        )

    overview_df = pd.DataFrame(overview_table)

    overview_csv = overview_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Campus Issue Overview as CSV",
        data=overview_csv,
        file_name="campuscare_issue_overview.csv",
        mime="text/csv",
    )

else:
    st.info(
        "No feedback has been submitted yet. "
        "The issue overview will appear when feedback is available."
    )
