import streamlit as st
from typing import Literal

def load_agent(hybrid_retrieve: bool):
    from agent.main_agent import CSLinkAja
    from agent.impartial_evaluator_agent import ImpartialEvaluator

    return CSLinkAja(hybrid_retrieve=hybrid_retrieve), ImpartialEvaluator()

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input(main_agent, evaluator_agent):
    if prompt := st.chat_input("What is up?"):
        display_user_message(prompt)
        response = get_agent_response(main_agent, prompt)
        display_agent_response(response.page_content)
        
        evaluation_results = get_evaluate_response(evaluator_agent, prompt, response)
        display_agent_response(evaluation_results, role='evaluator')
        
        update_chat_history(prompt, response.page_content, evaluation_results)

def display_user_message(prompt: str):
    with st.chat_message("user"):
        st.markdown(prompt)

def get_evaluate_response(agent, prompt, response):
    return agent.run(prompt, response)

def get_agent_response(agent, prompt: str):
    chat_history = [item for item in st.session_state.messages if item['role'] in ['user', 'assistant']][-6:]
    return agent.run(prompt, chat_history=chat_history)

def display_agent_response(response_text: str, role: Literal['assistant', 'evaluator'] = 'assistant'):
    with st.chat_message(role):
        st.markdown(response_text)

def update_chat_history(user_input: str, assistant_response: str, evaluation_results: str):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.session_state.messages.append({"role": "evaluator", "content": evaluation_results})

def main():
    with st.sidebar:
        st.header("Chat Settings")
        retrieve_mode = st.radio("Retrieval Mode", ["Single", "Multi"], horizontal=True)

    hybrid_retrieve = True if retrieve_mode == 'Multi' else False
    
    main_agent, evaluator_agent = load_agent(hybrid_retrieve=hybrid_retrieve)
    initialize_chat_history()
    display_chat_history()
    handle_user_input(main_agent, evaluator_agent)


if __name__ == "__main__":
    main()
