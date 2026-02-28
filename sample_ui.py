import streamlit as st
import requests

agent_endpoint = "https://127.000.8000/chat/agent"
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

# Main Chat Area
st.title("Travloop Assistant Demo")

# Display chat messages from history on app rerun
for chat_message in st.session_state.chat_messages:
    with st.chat_message(chat_message["role"]):
        st.markdown(chat_message["content"])
    

# Accept user input
if question := st.chat_input("Input your next move"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(question)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("I am thinking..."):
            try:
                MAX_MESSAGES = 5
                
                response = requests.get(agent_endpoint, params = {"messages": st.session_state.chat_message})
                messages = response["messages"]
                ai_response = messages[-1].content
               
                # Add user message to chat history
                st.session_state.chat_messages.append(
                    {"role": "user", "content": question}
                )
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": ai_response}
                )

                message_placeholder.markdown(ai_response)

            except Exception as e:
                st.error(e)
