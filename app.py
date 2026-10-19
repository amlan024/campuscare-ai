
import streamlit as st

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
