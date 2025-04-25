import streamlit as st

def load_agent():
    from agent.main_agent import CSLinkAja
    return CSLinkAja(hybrid_retrieve=True)

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(agent):
    if prompt := st.chat_input("What is up?"):
        display_user_message(prompt)
        response = get_agent_response(agent, prompt)
        display_agent_response(response.page_content)
        update_chat_history(prompt, response.page_content)

def display_user_message(prompt: str):
    with st.chat_message("user"):
        st.markdown(prompt)

def get_agent_response(agent, prompt: str):
    return agent.run(prompt, chat_history=st.session_state.messages)

def display_agent_response(response_text: str):
    with st.chat_message("assistant"):
        st.markdown(response_text)

def update_chat_history(user_input: str, assistant_response: str):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Main function
def main():
    agent = load_agent()
    initialize_chat_history()
    display_chat_history()
    handle_user_input(agent)

if __name__ == "__main__":
    main()
