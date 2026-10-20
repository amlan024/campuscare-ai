# CampusCare AI 🎓

An AI-powered student support platform for campus guidance, student feedback, and campus problem tracking.

## 🚀 Overview

CampusCare AI helps students find campus guidance, submit feedback, track common campus issues, and explore support resources through an interactive web application.

It combines rule-based feedback analysis with AI-generated answers grounded in a sample campus knowledge base.

## ✨ Features

- **Student Feedback:** Submit campus feedback through an interactive form.
- **Automatic Categorization:** Classify feedback into categories such as Academic Support, Internet, Hostel Facilities, and Water Supply.
- **Priority Suggestions:** Identify potentially urgent feedback using rule-based keywords.
- **Feedback Dashboard:** View feedback history, category summaries, and priority statistics.
- **Search and Filtering:** Find feedback by keyword, category, and priority.
- **CSV Exports:** Export feedback and summary reports.
- **Student Guide and FAQs:** Search guidance and browse common campus support information.
- **Campus Knowledge Assistant:** Retrieve relevant sample campus guidance.
- **AI-Generated Answers:** Use Google Gemini to generate concise answers based on retrieved guidance, with a fallback when the AI service is unavailable.

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- SQLite
- Google Gemini API (`google-genai`)
- JSON-based campus knowledge

## ⚙️ Run Locally

1. Clone this repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   cd YOUR_REPOSITORY_FOLDER
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.streamlit/secrets.toml` file and add your Gemini API key:

   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

Replace the repository URL and folder name with your actual GitHub details. Keep your API key private and never commit `secrets.toml` to GitHub.

## 🔐 Privacy and Limitations

- The campus knowledge included in this project is sample guidance and is not verified official campus policy.
- Feedback categorization and priority suggestions use simple rules and may not always be accurate.
- Gemini-generated answers depend on the retrieved knowledge and AI service availability.
- SQLite data stored on an ephemeral hosting filesystem may not persist across restarts or redeployments.
- Use fictional or non-sensitive feedback for demonstrations. A production deployment would need appropriate privacy safeguards, durable storage, access controls, and human review.

## 🎯 Project Goal

The goal of CampusCare AI is to demonstrate how Python, data analysis, information retrieval, and generative AI can be combined to build a practical student-support application.

## 👨‍💻 Author

Amlan Mishra  
Computer Science and Engineering Student, IIITDM Jabalpur
