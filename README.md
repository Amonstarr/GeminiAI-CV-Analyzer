# 📄 Gemini AI CV Analyzer

AI Resume Analyzer is a web application that analyzes resumes using **Google Gemini AI**.
Users can upload a resume in **PDF format**, and the system will generate insights such as a professional summary, strengths, weaknesses, suggested job roles, and an overall resume score.

The application uses a **Flask backend** for AI processing and a **Streamlit frontend** for the user interface.

---

# 🛠 Tech Stack

### Backend

* Python
* Flask
* Flask-CORS
* PyPDF2
* Google Gemini API

### Frontend

* Streamlit

### AI Model

* Gemini 2.5 Flash

---

# 📂 Project Structure

```
ai-resume-analyzer
│
├── backend
│   ├── app.py              # Flask API server
│   ├── config.py           # Gemini API key configuration
│
├── frontend
│   └── streamlit_app.py    # Streamlit UI
│
├── requirements.txt        # Python dependencies
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/GeminiAI-CV-Analyzer.git
cd GeminiAI-CV-Analyzer
```

---

## 2. Create a virtual environment (recommended)

```
python -m venv venv
```

Activate it:

**Windows**

```
venv\Scripts\activate
```

**Mac / Linux**

```
source venv/bin/activate
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 4. Add Gemini API Key

Create a file called **config.py** inside the backend folder.

```
backend/config.py
```

Example:

```
API_KEY = "YOUR_GEMINI_API_KEY"
```

You can obtain a Gemini API key from:

https://ai.google.dev

---

# ▶️ Running the Application

## Start the Flask Backend

```
python backend/app.py
```

The backend server will run on:

```
http://127.0.0.1:5000
```

---

## Start the Streamlit Frontend

Open another terminal and run:

```
streamlit run frontend/streamlit_app.py
```

Streamlit will open the web interface automatically.

---

# 📊 How It Works

1. User uploads a resume (PDF)
2. Backend extracts the text using **PyPDF2**
3. The resume text is sent to **Gemini AI**
4. Gemini analyzes the resume and generates insights
5. Results are displayed in the **Streamlit interface**

Available analysis:

* Overall Resume Score
* Resume Summary
* Resume Strengths
* Resume Weaknesses
* Suggested Job Titles

---

# 📸 Example Workflow

Upload Resume → AI Analysis → View Results

The system allows users to interactively explore different types of resume insights.
