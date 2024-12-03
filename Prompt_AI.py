import openai
import streamlit as st

# Set your OpenAI API Key
openai.api_key = "f0pOG3XNjhG5PLLYU4yLOoyPA9h8cDQEPbrHdSLbTjXYZDNu-E2M47FlErkAzSP7hINyuK-LPoT3BlbkFJrwuqI-xo154s1qxV9WXshMjrvGZ0CTIPJhhyeOFveLvlwSRtedvWXmmyoWFAYP_6qylPkoPkMA"  # Replace with your API key

# Define a function to interact with the API
def get_chat_response(prompt, chat_history=[]):
    try:
        # Add the conversation context (chat history) to the current prompt
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for chat in chat_history:
            messages.append({"role": "user", "content": chat["user"]})
            messages.append({"role": "assistant", "content": chat["assistant"]})
        messages.append({"role": "user", "content": prompt})
        
        # Send the request to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3",  # or "gpt-3.5-turbo"
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract and return the assistant's response
        assistant_message = response["choices"][0]["message"]["content"]
        return assistant_message
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App Layout
st.title("Custom ChatGPT Chatbot")
st.write("Type your prompt below and interact with a GPT-powered chatbot!")

# Chat history to maintain context
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You: ", placeholder="Ask me anything...")
if st.button("Send") and user_input:
    # Get the response
    response = get_chat_response(user_input, st.session_state.chat_history)
    
    # Save the conversation in the session state
    st.session_state.chat_history.append({"user": user_input, "assistant": response})

# Display the conversation
st.write("### Conversation History:")
for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['user']}")
    st.write(f"**Assistant:** {chat['assistant']}")
