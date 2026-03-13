from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("Starting Flask Resume Analyzer Backend...")

# Configure Gemini API
genai.configure(api_key=config.API_KEY)

generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)

app = Flask(__name__)
CORS(app)


# Function to interact with Gemini AI
def gemini_generate_response(prompt):

    print("Sending prompt to Gemini...")

    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [prompt]}]
    )

    response = chat_session.send_message(prompt)

    print("Gemini response received")

    return response.text


# 1. Parse PDF
def parse_pdf(file):

    print("Parsing PDF...")

    reader = PdfReader(file)
    text = ""

    for page_number, page in enumerate(reader.pages):

        extracted = page.extract_text()

        if extracted:
            print(f"Page {page_number+1} extracted")
            text += extracted

    print("PDF parsing completed")

    return text


# 2. Split text into chunks
def split_text_into_chunks(text):

    print("Splitting resume text into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
        length_function=len
    )

    chunks = splitter.split_text(text)

    print(f"Total chunks created: {len(chunks)}")

    return chunks


# 3. Resume Summary
def resume_summary(chunks):

    print("Generating resume summary...")

    prompt = f"""
Provide a professional summary of the following resume.

Resume:
{chunks}
"""

    return gemini_generate_response(prompt)


# 4. Resume Strengths
def resume_strength(chunks):

    print("Analyzing resume strengths...")

    prompt = f"""
Analyze the strengths of the following resume.

Focus on:
- Skills
- Experience
- Education
- Achievements

Resume:
{chunks}
"""

    return gemini_generate_response(prompt)


# 5. Resume Weaknesses
def resume_weakness(chunks):

    print("Analyzing resume weaknesses...")

    prompt = f"""
Analyze weaknesses in the following resume.

Provide suggestions to improve it.

Resume:
{chunks}
"""

    return gemini_generate_response(prompt)


# 6. Job Title Suggestions
def job_title_suggestion(chunks):

    print("Generating job title suggestions...")

    prompt = f"""
Based on the resume below, suggest suitable job roles.

Resume:
{chunks}
"""

    return gemini_generate_response(prompt)


# 7. Overall Resume Score
def resume_score(chunks):

    print("Calculating resume score...")

    prompt = f"""
Evaluate the resume below and give an overall score from 0 to 100.

Consider:
- Resume structure
- Skills relevance
- Work experience
- ATS friendliness
- Professional clarity

Return result in this format:

Score: <number>/100
Explanation: <short explanation>

Resume:
{chunks}
"""

    return gemini_generate_response(prompt)


# Flask API Endpoint
@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():

    print("\n===== New Resume Analysis Request =====")

    if 'fileUploaded' not in request.files:

        print("ERROR: No file uploaded")

        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files["fileUploaded"]

    print(f"File received: {file.filename}")

    try:

        # Extract text from PDF
        resume_text = parse_pdf(file)

        if not resume_text:
            print("ERROR: No text extracted from PDF")

        # Split into chunks
        chunks = split_text_into_chunks(resume_text)

        # Run AI analysis
        summary = resume_summary(chunks)
        strengths = resume_strength(chunks)
        weaknesses = resume_weakness(chunks)
        job_titles = job_title_suggestion(chunks)
        overall_score = resume_score(chunks)

        response = {
            "summary": summary,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "job_titles": job_titles,
            "overall_score": overall_score
        }

        print("Resume analysis completed successfully")

        return jsonify(response)

    except Exception as e:

        print("ERROR OCCURRED:", str(e))

        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("Flask server starting...")
    app.run(debug=True)