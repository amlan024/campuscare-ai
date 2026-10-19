
import streamlit as st

from database import (
    create_table,
    save_feedback,
    get_all_feedback,
    get_feedback_category_counts,
)

from ai_helper import categorize_feedback

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
    st.info(f"Suggested category: {suggested_category}")
st.write("Selected issue:", issue)


if st.button("Submit Feedback"):
    if feedback.strip():
        suggested_category = categorize_feedback(feedback)

        save_feedback(issue, feedback, suggested_category)

        st.success("Your feedback has been saved successfully!")

        st.write("Selected issue:", issue)
        st.write("AI-suggested category:", suggested_category)
        st.write("Your feedback:", feedback)
    else:
        st.warning("Please describe your issue before submitting.")


st.header("Feedback History")

records = get_all_feedback()

st.subheader("Feedback Summary")

total_feedback = len(records)

st.metric(
    label="Total Feedback Submissions",
    value=total_feedback
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
else:
    st.info("No feedback categories are available yet.")


if records:
    st.dataframe(
        [
            {
                "Feedback ID": record[0],
                "Issue": record[1],
                "Description": record[2],
                "AI-suggested Category": record[3],
                "Submitted At": record[4],
            }
            for record in records
        ],
        use_container_width=True,
    )

else:
    st.info("No feedback has been submitted yet.")
