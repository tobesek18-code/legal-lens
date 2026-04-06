import os
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader

# 1. Load our secret key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(pdf_path):
    """This function opens the PDF and turns it into text."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def analyze_lease(lease_text):
    """This function sends the text to the AI for analysis."""
    print("Analyzing lease for red flags... please wait.")

    response = client.chat.completions.create(
        model="gpt-4o",  # Using the latest 2026 model
        messages=[
            {"role": "system",
             "content": "You are a Real Estate Legal Assistant. Find 'red flags' in this lease, such as hidden costs, unfair rules, or termination penalties."},
            {"role": "user", "content": f"Analyze this lease text:\n\n{lease_text}"}
        ]
    )
    return response.choices[0].message.content


# --- START THE APP ---
if __name__ == "__main__":
    # For now, put a PDF in your project folder and name it 'lease.pdf'
    # Or we can test with a text input for the first run.
    file_path = "lease.pdf"

    if os.path.exists(file_path):
        content = extract_text_from_pdf(file_path)
        report = analyze_lease(content)
        print("\n--- AI ANALYSIS REPORT ---")
        print(report)
    else:
        print(f"Error: Please place a file named '{file_path}' in your folder.")