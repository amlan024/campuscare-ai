# CampusCare AI 🎓

An AI-powered student support platform for campus guidance, student feedback, and campus issue management.

## 🚀 Overview

CampusCare AI provides students with a public feedback portal and administrators with a separate private dashboard for reviewing feedback and exploring campus support resources.

The platform combines rule-based feedback categorization, priority suggestions, searchable campus guidance, and AI-generated answers grounded in a sample campus knowledge base.

**Project status:** Working prototype deployed using Streamlit Community Cloud and Supabase.

## ✨ Features

- **Student Feedback Portal:** Submit campus-related concerns through a separate public web application.
- **Automatic Categorization:** Suggest categories such as Academic Support, Internet, Hostel Facilities, and Water Supply.
- **Priority Suggestions:** Identify potentially urgent feedback using rule-based keywords.
- **Administrator Dashboard:** Review feedback history and view category and priority statistics.
- **Search and Filtering:** Find feedback using available keywords, categories, and priorities.
- **CSV Exports:** Export feedback and summary reports.
- **Student Guide and FAQs:** Explore common campus support information.
- **Campus Knowledge Assistant:** Retrieve relevant information from a sample campus knowledge base.
- **AI-Generated Answers:** Use Google Gemini to generate answers grounded in retrieved guidance, with fallback handling when the AI service is unavailable.
- **Separate Public and Private Applications:** Keep the student submission interface separate from the administrator dashboard.

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- Supabase (PostgreSQL database)
- Google Gemini API (`google-genai`)
- JSON-based campus knowledge

## 🏗️ Project Structure

- `app.py` — Administrator dashboard
- `student_app.py` — Public student feedback portal
- `database.py` — Database clients and feedback operations
- `ai_helper.py` — Feedback analysis and AI helper functions
- `campus_knowledge.json` — Sample campus knowledge base
- `requirements.txt` — Python dependencies
- `.gitignore` — Files excluded from version control

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/amlan024/campuscare-ai
cd YOUR_REPOSITORY_FOLDER
```

Replace the placeholders with your actual repository URL and folder name.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Streamlit secrets

Create a `.streamlit/secrets.toml` file in the project directory.

For the administrator dashboard, configure these keys using the corresponding values from your Supabase project and Gemini account:

```toml
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_KEY = "your_server_side_supabase_secret"
SUPABASE_ANON_KEY = "your_supabase_publishable_or_anon_key"
GEMINI_API_KEY = "your_gemini_api_key"
ADMIN_PASSWORD = "your_strong_admin_password"
```

For the student portal, configure only the following database connection keys in its Streamlit secrets:

```toml
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_ANON_KEY = "your_supabase_publishable_or_anon_key"
```

Use the exact key names expected by your application code. Never commit `.streamlit/secrets.toml` or expose server-side database secrets in public code.

### 4. Start the administrator dashboard

```bash
streamlit run app.py
```

### 5. Start the student portal

In another terminal, run:

```bash
streamlit run student_app.py
```

The two applications can run on separate local Streamlit ports.

## ☁️ Deployment

The project uses Streamlit Community Cloud for hosting and Supabase for database storage.

Deploy each application separately:

- **Administrator dashboard:** Set the main file path to `app.py`.
- **Student feedback portal:** Set the main file path to `student_app.py`.

Configure secrets separately for each deployed application. The public student portal should not receive the administrator's server-side database secret, administrator password, or Gemini API key unless its code explicitly requires them.

Add your actual deployed application URLs here:

- **Student Portal:** https://campuscare-ai-8airkmr3qobhqmxrsfhh6l.streamlit.app/
- **Administrator Dashboard:** https://campuscare-ai-nvbeqhupr3braoqkqjsctx.streamlit.app/

Replace both placeholders with the real URLs before publishing the project documentation.

## 🔐 Security, Privacy, and Limitations

- The student portal is intended for feedback submission; it does not provide public feedback history or administrator dashboard statistics.
- Supabase Row-Level Security is enabled on the feedback table. Anonymous access is restricted to the configured insertion policy, and public reading was tested and denied.
- Keep the administrator dashboard and its server-side credentials protected.
- Input validation includes checks for empty descriptions, description length, consent, and valid issue categories.
- Input validation alone does not prevent spam, automated abuse, or repeated submissions. Additional abuse prevention and rate limiting should be reviewed before real-world deployment.
- Do not submit passwords, student identification numbers, financial information, or other sensitive personal information during demonstrations.
- Campus guidance is sample content and should not be treated as verified official campus policy.
- Feedback categories and priority suggestions may be inaccurate and require human review.
- AI-generated answers depend on retrieved knowledge and the availability of the AI service.
- Protect secrets, review access controls, and establish appropriate privacy notices and data-retention practices before collecting real student feedback.

## 🎯 Project Goal

CampusCare AI demonstrates how Python, data analysis, information retrieval, database integration, and generative AI can be combined to build a practical student-support application.

## 👨‍💻 Author

**Amlan Mishra**  
Computer Science and Engineering Student  
Indian Institute of Information Technology, Design and Manufacturing, Jabalpur (IIITDMJ)
