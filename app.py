import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from io import StringIO

# --- Load and configure API key ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")  # Update based on list_models if needed

# --- Streamlit page settings ---
st.set_page_config(page_title="AI Study Abroad Assistant", layout="centered")
st.title("🌍 AI Study Abroad Assistant")

# --- SOP Generator Section ---
st.subheader("✍️ SOP Generator")
background = st.text_area("Describe your academic background, goals, and why you want to study abroad")

sop_text = ""
if st.button("Generate SOP"):
    if background.strip() == "":
        st.warning("Please enter your background details.")
    else:
        with st.spinner("Generating your SOP..."):
            prompt = f"Write a professional and well-structured SOP based on this information:\n{background}"
            response = model.generate_content(prompt)
            sop_text = response.text
            st.success("✅ Here's your SOP:")
            st.write(sop_text)

            # Download Button
            sop_file = StringIO(sop_text)
            st.download_button(
                label="📥 Download SOP as .txt",
                data=sop_file,
                file_name="My_SOP.txt",
                mime="text/plain"
            )

# --- Quick Prompts Section ---
st.subheader("⚡ Quick Help")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎓 Top Universities"):
        with st.spinner("Fetching top universities..."):
            response = model.generate_content("List top universities in Germany for MS in Data Science.")
            st.info(response.text)

with col2:
    if st.button("✅ Visa Checklist"):
        with st.spinner("Getting visa checklist..."):
            response = model.generate_content("What documents are required for a student visa to Germany?")
            st.info(response.text)

with col3:
    if st.button("💰 Scholarships"):
        with st.spinner("Finding scholarships..."):
            response = model.generate_content("List popular scholarships available for international students in Germany.")
            st.info(response.text)

# --- Chat-style Q&A Section ---
st.subheader("💬 Ask Anything")

user_question = st.text_input("Type your custom question about studying abroad:")

if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            response = model.generate_content(user_question)
            st.success("Here's the answer:")
            st.write(response.text)

# --- Footer ---
st.markdown("---")
st.caption("🤖 Powered by Google Gemini | Built with ❤️ using Streamlit")
