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

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Custom CSS for centering elements
st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    .input-box {
        width: 60%;
        margin-bottom: 20px;
    }
    .response-box {
        width: 80%;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .history-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for input
st.sidebar.title("💬 Ask a Question")
st.sidebar.write("Get assistance on Thoughtful AI's automation solutions.")

# Main title and description
st.markdown("<h1 class='centered'>🤖 Thoughtful AI Support Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='centered'>Hello! I’m your AI assistant. Ask me anything about **Thoughtful AI's Agents** and their capabilities. I'm here to help! 💡</p>", unsafe_allow_html=True)

# Input from user in the center
# user_input = st.text_input("Enter your question here:", key="user_input", label_visibility="collapsed")
# user_input = st.text_input("Enter your question here:", key="user_input", label_visibility="visible")
user_input = st.text_input("Enter your question here", "",key="user_input")


# Input box styling
# st.markdown('<div class="centered"><input type="text" class="input-box" placeholder="Enter your question here..." value=""></div>', unsafe_allow_html=True)

# Response logic
if st.button("Ask"):
    if user_input:
        with st.spinner("Thinking..."):
            # Try to get a predefined response first
            answer = get_predefined_answer(user_input)
            
            # Fallback to LLM if no predefined answer
            if not answer:
                answer = get_llm_response(user_input)
        
        # Save question and answer to session state
        st.session_state.history.append((user_input, answer))
        
        # Display the answer with improved formatting
        st.markdown(f"<div class='centered'><div class='response-box'><strong>🔍 Your Question:</strong><br>{user_input}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='centered'><div class='response-box'><strong>🤖 AI Answer:</strong><br>{answer}</div></div>", unsafe_allow_html=True)
    else:
            st.warning("Please enter a query.")


# st.session_state["user_input"] = ""
# History Section
st.markdown("<h2 class='centered'>📝 Conversation History</h2>", unsafe_allow_html=True)
if st.session_state.history:
    for idx, (question, answer) in enumerate(st.session_state.history, 1):
        st.markdown(f"<div class='centered'><div class='history-box'><strong>Q{idx}:</strong> {question}<br><strong>A{idx}:</strong> {answer}</div></div>", unsafe_allow_html=True)
else:
    st.markdown("<p class='centered'>No conversation history yet.</p>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='centered'><p>Made with ❤️ by Thoughtful AI | <a href='https://www.thoughtful.ai' target='_blank'>Visit Us</a></p></div>", unsafe_allow_html=True)

# Additional explanation or help
st.sidebar.info("💡 Need more help? Feel free to contact support or explore our [documentation](https://www.thoughtful.ai/docs).")
