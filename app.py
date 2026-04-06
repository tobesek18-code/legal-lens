import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader

STRIPE_LINK = "https://buy.stripe.com/test_fZufZabMI0HH7fS6R7dEs00"

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page Config (The title in the browser tab)
st.set_page_config(page_title="LegalLens AI", page_icon="⚖️")

st.title("⚖️ LegalLens: Real Estate Analyzer")
st.subheader("Upload a lease to find red flags in seconds")

# File Uploader UI
uploaded_file = st.file_uploader("Choose a PDF lease file", type="pdf")

if uploaded_file is not None:
    # 1. Read the PDF
    with st.spinner("Reading document..."):
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # 2. Analyze Button
    st.sidebar.markdown(f"### 🚀 Ready to Analyze?")
    st.sidebar.write("To support the AI costs, we charge a small fee per analysis.")
    st.sidebar.link_button("Get Access Key ($9.99)", STRIPE_LINK)

    access_key = st.sidebar.text_input("Enter your Access Key from email:", type="password")

    if access_key == "ST-12345":  # You can manually email this to them for now
        if st.button("Analyze Lease"):
            with st.spinner("AI is hunting for red flags..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system",
                         "content": "You are a Real Estate Expert. List red flags in bullet points. Use bold text for high-risk items."},
                        {"role": "user", "content": text}
                    ]
                )
            report = response.choices[0].message.content

            st.success("Analysis Complete!")
            st.markdown(report)