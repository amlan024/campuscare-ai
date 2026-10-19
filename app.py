
import streamlit as st
from database import create_table, save_feedback

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

st.write("Selected issue:", issue)

if st.button("Submit Feedback"):
    if feedback.strip():
        st.success("Your feedback has been submitted successfully!")

        st.write("Issue:", issue)
        st.write("Your feedback:", feedback)
    else:
        st.warning("Please describe your issue before submitting.")
