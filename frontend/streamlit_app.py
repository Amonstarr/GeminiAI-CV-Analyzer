import streamlit as st
import requests
import re

# Flask API endpoint
FLASK_API_URL = "http://127.0.0.1:5000/analyze_resume"



st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Upload a resume PDF and get AI insights about your resume quality.")

# Upload resume
uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type="pdf")

# Check session state
if "response_data" in st.session_state:
    response_data = st.session_state.response_data
else:
    response_data = None


# Analyze Button
if st.button("Analyze Resume 🚀"):

    if uploaded_resume:

        with st.spinner("Analyzing resume with AI..."):

            files = {"fileUploaded": uploaded_resume}

            response = requests.post(FLASK_API_URL, files=files)

            if response.status_code == 200:

                response_data = response.json()
                st.session_state.response_data = response_data

                st.success("Resume analyzed successfully!")

            else:
                st.error("Error retrieving response from server.")

    else:
        st.warning("Please upload a resume PDF.")


# Show Results
if response_data:

    st.divider()

    selected_analysis = st.radio(
        "Select Analysis",
        [
            "Overall Score",
            "Summary",
            "Strengths",
            "Weaknesses",
            "Suggested Job Titles"
        ]
    )

    # =============================
    # OVERALL SCORE
    # =============================
    if selected_analysis == "Overall Score":

        st.subheader("📊 Resume Score")

        score_text = response_data.get("overall_score", "")

        match = re.search(r'\d+', score_text)

        if match:
            score = int(match.group())

            st.progress(score)

            st.metric("Resume Score", f"{score}/100")

            # ATS Style Feedback
            if score >= 80:
                st.success("✅ Excellent Resume – ATS Friendly")
            elif score >= 60:
                st.warning("⚠️ Good Resume – Some Improvements Recommended")
            else:
                st.error("❌ Resume Needs Improvement")

        st.write(score_text)

    # =============================
    # SUMMARY
    # =============================
    elif selected_analysis == "Summary":

        st.subheader("🧾 Resume Summary")
        st.write(response_data.get("summary", "No summary available."))

    # =============================
    # STRENGTHS
    # =============================
    elif selected_analysis == "Strengths":

        st.subheader("💪 Resume Strengths")
        st.write(response_data.get("strengths", "No strengths detected."))

    # =============================
    # WEAKNESSES
    # =============================
    elif selected_analysis == "Weaknesses":

        st.subheader("⚠️ Areas for Improvement")
        st.write(response_data.get("weaknesses", "No weaknesses detected."))

    # =============================
    # JOB TITLES
    # =============================
    elif selected_analysis == "Suggested Job Titles":

        st.subheader("💼 Suggested Job Roles")
        st.write(response_data.get("job_titles", "No job title suggestions available."))

else:
    st.info("Upload a resume and click **Analyze Resume** to begin.")