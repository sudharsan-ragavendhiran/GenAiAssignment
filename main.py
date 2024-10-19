import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Predefined dataset
predefined_data = {
    "questions": [
        {
            "question": "What does the eligibility verification agent (EVA) do?",
            "answer": "EVA automates the process of verifying a patient’s eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
        },
        {
            "question": "What does the claims processing agent (CAM) do?",
            "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
        },
        {
            "question": "How does the payment posting agent (PHIL) work?",
            "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
        },
        {
            "question": "Tell me about Thoughtful AI's Agents.",
            "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
        },
        {
            "question": "What are the benefits of using Thoughtful AI's agents?",
            "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
        }
    ]
}

# Function to check predefined responses
def get_predefined_answer(question):
    for qa in predefined_data["questions"]:
        if qa["question"].lower() in question.lower():
            return qa["answer"]
    return None

# Function to get fallback response from OpenAI (generic LLM)
def get_llm_response(question):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Updated to use gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit UI Enhancements
st.set_page_config(page_title="Thoughtful AI Support", page_icon="🤖", layout="centered")

# Sidebar for input
st.sidebar.title("💬 Ask a Question")
st.sidebar.write("Get assistance on Thoughtful AI's automation solutions.")

# Input from user in the sidebar
user_input = st.sidebar.text_input("Enter your question:")

# Main title and description
st.title("🤖 Thoughtful AI Support Agent")
st.write("Hello! I’m your AI assistant. Ask me anything about **Thoughtful AI's Agents** and their capabilities. I'm here to help! 💡")

# Response logic
if user_input:
    with st.spinner("Thinking..."):
        # Try to get a predefined response first
        answer = get_predefined_answer(user_input)
        
        # Fallback to LLM if no predefined answer
        if not answer:
            answer = get_llm_response(user_input)
    
    # Display the answer with improved formatting
    st.markdown(f"### 🔍 **Your Question:**")
    st.write(f"{user_input}")
    st.markdown(f"### 🤖 **AI Answer:**")
    st.write(f"{answer}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Thoughtful AI | [Visit Us](https://www.thoughtful.ai)")

# Additional explanation or help
st.sidebar.info("💡 Need more help? Feel free to contact support or explore our [documentation](https://www.thoughtful.ai/docs).")