import streamlit as st
import requests

st.set_page_config(page_title="🩺 Doctor Appointment System", layout="wide")
st.title("🩺 Doctor Appointment System")

with st.sidebar:
    st.header("User Details")
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
    user_id = st.text_input("Enter Your 7 or 8 Digit ID", value=st.session_state.user_id)
    st.session_state.user_id = user_id

API_URL = "http://127.0.0.1:8003/execute"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the entire chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get new user input
if user_input := st.chat_input("How can I help you today?"):
    if not st.session_state.user_id.isdigit() or not (7 <= len(st.session_state.user_id) <= 8):
        st.warning("Please enter a valid 7 or 8 digit Identification Number in the sidebar.")
    else:
        # Append and display the user's new message immediately
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Send the full history to the backend for context
        payload = {
            "messages": user_input,
            "id_number": int(st.session_state.user_id),
            "conversation_history": st.session_state.messages[:-1] 
        }

        try:
            with st.spinner('Thinking...'):
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                api_response = response.json()

                if "messages" in api_response and api_response["messages"]:
                    # Extract only the LAST message from the agent's full response
                    last_agent_message = api_response["messages"][-1]
                    assistant_response = last_agent_message.get("content", "Sorry, I could not parse the response.")
                    
                    # Append the new assistant response to our history and display it
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response)
                else:
                    # Handle cases where the backend returns an empty message list
                    assistant_response = "Sorry, the agent returned an empty response."
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response)

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: Could not connect to the agent. Details: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

