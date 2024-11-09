import os
import streamlit as st
import pdfplumber
import docx2txt
import openai
import io
import csv

from openai import OpenAI


# Set OpenAI API key
os.environ["OPENAI_API_KEY"] =  "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"
client=OpenAI()

# Function to generate a summary
def generate_summary(extracted_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant trained to summarize documents."},
            {"role": "user", "content": extracted_text}
        ],
        temperature=0.4,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


# Function to generate a study plan
def generate_study_plan(extracted_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are a study planner trained to create personalized study plans. Analyze the document content "
                "and break it into digestible chunks, including the following: \n"
                "1. Key topics\n"
                "2. Estimated study time\n"
                "3. Suggested study order\n"
                "4. Study techniques (e.g., summarization, active recall)\n"
                "5. Include breaks and review sessions where needed."
            )},
            {"role": "user", "content": extracted_text}
        ],
        temperature=1,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


# Function to generate flashcards
def generate_flashcards(extracted_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "Create as many flashcards as possible. Each flashcard should contain a question or concept on one side "
                "and an answer on the other, focusing on key concepts, definitions, and examples from the document."
            )},
            {"role": "user", "content": extracted_text}
        ],
        temperature=1,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


# Read file functions
def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "".join(page.extract_text() or "" for page in pdf.pages)


def read_docx(file):
    return docx2txt.process(file)


def read_txt(file):
    return file.read().decode("utf-8")


# Streamlit UI

# Custom CSS Styling for Enhanced UI
st.markdown("""
    <style>
        /* Global page styling */
        body {
            background: linear-gradient(135deg, #f0f4f8, #e0e6ed);  /* Smooth gradient */
            font-family: 'Arial', sans-serif;
            color: #333;
            padding: 40px 20px;
            transition: background 0.4s ease;
        }

        /* Sidebar styling */
        .css-1d391kg {  
            background: linear-gradient(180deg, #4c9eff, #005f99); 
            border-radius: 20px;  
            padding: 20px;
            box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            min-width: 250px;
        }

        .stSidebar .sidebar-header {
            text-align: center;
            padding-bottom: 20px;
        }

        .stSidebar .sidebar-content {
            background-color: transparent;
        }

        .sidebar-title {
            color: white;
            font-size: 36px;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
            letter-spacing: 1.2px;
        }

        /* Sidebar button styles */
        .stRadio label {
            font-size: 22px;
            color: #ffffff;
            padding: 20px 0;
            border-radius: 8px;
            transition: background-color 0.3s ease;
            display: block;
            text-align: center;
            font-weight: 600;
        }

        .stRadio label:hover {
            background-color: #4c9eff;
            cursor: pointer;
        }

        /* Section header styling */
        h2 {
            color: #2a6fb9;
            font-size: 36px;
            margin-bottom: 20px;
            font-weight: bold;
            text-align: center;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        h3 {
            color: #666;
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 400;
        }

        /* Card styles */
        .card {
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15);
            padding: 30px;
            margin-bottom: 30px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e0e6ed;
        }

        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0px 12px 30px rgba(0, 0, 0, 0.2);
        }

        /* Button Styles */
        .stButton button {
            background-color: #3498db;
            color: white;
            padding: 18px 30px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: background-color 0.3s ease, transform 0.3s ease;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
        }

        .stButton button:hover {
            background-color: #2980b9;
            transform: scale(1.05);
        }

        /* File uploader styling */
        .file-uploader {
            padding: 20px;
            border-radius: 10px;
            border: 2px dashed #3498db;
            background-color: #f9f9f9;
            transition: background-color 0.3s ease;
        }

        .file-uploader:hover {
            background-color: #ecf0f1;
        }

        /* Text area styling */
        .stTextArea textarea {
            border-radius: 12px;
            border: 1px solid #e0e6ed;
            padding: 16px;
            font-size: 16px;
            background-color: #f0f4f8;
            color: #333;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Download button styling */
        .download-button {
            background-color: #2ecc71;
            color: white;
            padding: 18px 30px;
            border-radius: 12px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            margin-top: 25px;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        .download-button:hover {
            background-color: #27ae60;
            transform: scale(1.05);
        }

        /* Footer styling */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #7f8c8d;
            padding: 30px 0;
            background-color: #f7f9fc;
            border-radius: 15px;
            box-shadow: 0px -5px 12px rgba(0, 0, 0, 0.05);
        }

        /* Smooth transition for inputs */
        .stTextInput input, .stTextArea textarea {
            background-color: #f1f8fe;
            transition: background-color 0.3s ease;
        }

        /* Styling for the header */
        .header-title {
            color: #2a6fb9;
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        /* Styling for the divider */
        .divider {
            border: 1px solid #e0e6ed;
            margin: 40px 0;
        }

    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="header-title">Study Buddy</div>', unsafe_allow_html=True)

# Sidebar with a radio button to select application mode
st.sidebar.markdown('<div class="sidebar-title">Select Application</div>', unsafe_allow_html=True)
app_mode = st.sidebar.radio(
    "Choose an application",
    ("Summary", "Planner", "FlashCards"),
    index=0,
    label_visibility="collapsed"
)

# Content for the selected app mode
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if app_mode == "Summary":
    st.header("Generate Summary")
    file = st.file_uploader("Upload a file for summary", type=["pdf", "docx", "txt"])

    if file:
        text = read_pdf(file) if file.type == "application/pdf" else read_docx(file) if file.type.endswith(
            "docx") else read_txt(file)

        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = generate_summary(text)
                st.text_area("Summary", summary, height=300)

elif app_mode == "Planner":
    st.header("Generate Study Plan")
    file = st.file_uploader("Upload a file for study plan", type=["pdf", "docx", "txt"])

    if file:
        text = read_pdf(file) if file.type == "application/pdf" else read_docx(file) if file.type.endswith(
            "docx") else read_txt(file)

        if st.button("Generate Study Plan"):
            with st.spinner("Generating study plan..."):
                study_plan = generate_study_plan(text)
                st.text_area("Study Plan", study_plan, height=300)

elif app_mode == "FlashCards":
    st.header("Generate Flashcards")
    file = st.file_uploader("Upload a file for flashcards", type=["pdf", "docx", "txt"])

    if file:
        text = read_pdf(file) if file.type == "application/pdf" else read_docx(file) if file.type.endswith("docx") else read_txt(file)

        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                flashcards_text = generate_flashcards(text)
                flashcards = [
                    {"question": line.split(": ", 1)[0], "answer": line.split(": ", 1)[1]}
                    for line in flashcards_text.split("\n") if ": " in line
                ]

                # Create CSV in memory
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["Question", "Answer"])
                for flashcard in flashcards:
                    writer.writerow([flashcard["question"], flashcard["answer"]])

                st.download_button(
                    label="Download Flashcards as CSV",
                    data=output.getvalue(),
                    file_name="flashcards.csv",
                    mime="text/csv"
                )

# Footer
st.markdown('<div class="footer">© 2024 AI Study Helper | All Rights Reserved</div>', unsafe_allow_html=True)