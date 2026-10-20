
import streamlit as st

from database import save_feedback_public
from ai_helper import categorize_feedback, suggest_priority


st.set_page_config(
    page_title="CampusCare AI — Student Portal",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 CampusCare AI")
st.subheader("Student Feedback Portal")

st.write(
    "Share campus-related concerns with the appropriate support team. "
    "This public portal does not display feedback history or administrator "
    "dashboard statistics."
)

st.info(
    "Use sample, non-sensitive feedback while testing. "
    "Do not include student IDs, passwords, financial details, "
    "or other sensitive personal information."
)

with st.form("student_feedback_form"):
    issue = st.selectbox(
        "What issue are you experiencing?",
        [
            "Hostel Facilities",
            "Water Supply",
            "Internet",
            "Academic Support",
            "Other",
        ],
    )

    description = st.text_area(
        "Describe your issue",
        max_chars=1000,
        placeholder=(
            "Example: The internet connection in the hostel study "
            "area has been slow since yesterday."
        ),
    )

    confirm_submission = st.checkbox(
        "I confirm that my feedback contains no sensitive personal information."
    )

    submitted = st.form_submit_button(
        "Submit Feedback",
        disabled=(
            not description.strip()
            or not confirm_submission
        ),
    )
if submitted:
    if not description.strip():
        st.warning("Please describe your issue before submitting.")
    elif not confirm_submission:
        st.warning("Please confirm that your feedback contains no sensitive personal information.")
    else:
        try:
            category = categorize_feedback(description)
            priority = suggest_priority(description)

            save_feedback_public(
                issue,
                description.strip(),
                category,
                priority,
            )

            st.success("Thank you! Your feedback was submitted successfully.")
            st.caption(
                "Your feedback is recorded for administrator review. "
                "The suggested category and priority may not be accurate."
            )
        except Exception:
            st.error(
                "We could not submit your feedback. Please try again later. "
                "Do not include sensitive personal information."
            )

st.divider()
st.caption(
    "CampusCare AI prototype · For urgent safety issues, contact "
    "campus security or the appropriate emergency services directly."
)

