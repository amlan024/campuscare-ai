```python
import time

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

# Basic per-session cooldown; not a substitute for server-side rate limiting.
COOLDOWN_SECONDS = 30

if "last_successful_submission" not in st.session_state:
    st.session_state.last_successful_submission = 0.0

remaining = max(
    0,
    int(
        COOLDOWN_SECONDS
        - (
            time.time()
            - st.session_state.last_successful_submission
        )
    ),
)

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

if remaining > 0:
    st.warning(
        f"Please wait {remaining} seconds before submitting again."
    )

submitted = st.button(
    "Submit Feedback",
    disabled=(
        not description.strip()
        or not confirm_submission
        or remaining > 0
    ),
)

if submitted:
    clean_description = description.strip()

    # Recheck the cooldown and validate inputs before processing.
    elapsed = (
        time.time()
        - st.session_state.last_successful_submission
    )

    if elapsed < COOLDOWN_SECONDS:
        st.warning("Please wait before submitting again.")

    elif not clean_description:
        st.warning("Please describe your issue before submitting.")

    elif len(clean_description) > 1000:
        st.warning("Your description must be 1,000 characters or fewer.")

    elif not confirm_submission:
        st.warning(
            "Please confirm that your feedback contains no sensitive "
            "personal information."
        )

    elif issue not in [
        "Hostel Facilities",
        "Water Supply",
        "Internet",
        "Academic Support",
        "Other",
    ]:
        st.warning("Please select a valid issue category.")

    else:
        try:
            category = categorize_feedback(clean_description)
            priority = suggest_priority(clean_description)

            save_feedback_public(
                issue,
                clean_description,
                category,
                priority,
            )

            st.session_state.last_successful_submission = time.time()

            st.success(
                "Thank you! Your feedback was submitted successfully."
            )
            st.caption(
                "Your feedback is recorded for administrator review. "
                "The suggested category and priority may not be accurate."
            )

            st.rerun()

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
```
