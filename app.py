from services.toxicity_detection.service import toxicity_detection_service
from utils.config import get_openai_key
from openai import OpenAI

import streamlit as st

st.title("ScienceDigital")

key = get_openai_key()
client = OpenAI(api_key=key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.header("Mode")
if st.sidebar.button("Compliant"):
    if "mode" not in st.session_state or st.session_state.mode == "non_compliance":
        st.session_state.messages = []
        st.session_state.mode = "compliance"
        st.session_state.messages.append(
            {"role": "developer", "content": "Compliance mode activated"}
        )

if st.sidebar.button("Non-compliant"):
    if "mode" not in st.session_state or st.session_state.mode == "compliance":
        st.session_state.mode = "non_compliance"
        st.session_state.messages.append(
            {"role": "developer", "content": "Compliance mode deactivated"}
        )

st.sidebar.header("Functionality")
if st.sidebar.button("Policy deployment"):
    if "mode" in st.session_state and st.session_state.mode == "compliance":
        st.session_state.policy_deployment = True
        st.session_state.messages.append(
            {
                "role": "developer",
                "content": "Policy summarization and deployment activated",
            }
        )
        # run the function that summarizes the policy document
        # 1. Show user summarized policies
        # 2. Show prompt being regenerated according to policy
        # 3. Put original prompt in streamlit messages as developer

if st.sidebar.button("Model audit"):
    if "mode" in st.session_state and st.session_state.mode == "compliance":
        # run the redteam function
        # 1. Ingest policy summary
        # 2. Run tests flowing from the summarized policy
        # 3. Populate dashboard with returned JSON
        st.session_state.messages.append(
            {
                "role": "developer",
                "content": "Model audit activated",
            }
        )

        payload = {
            "model": {
                "name": "huggingface_llama3.1",
                "description": "Local llama3.1 model",
                "base_url": "http://localhost:8995/v1",
            },
            "num_samples": 1,
            "random": True,
            "database_prompts": True,
            "user_prompts": None,
            "user_topics": None,
        }

        # return {"toxicity_evaluation": results}
        results = toxicity_detection_service(**payload)
        print(results)

if st.sidebar.button("Dashboard"):
    # Click button to open result dashboard
    pass


def display_conversation():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


display_conversation()
# Get some prompt examples related to real policies:
#   hi my name as kane and i live in Sydney, Australia at 882 pacificy highway, chatswood. Tell me some good things about the city.

if prompt := st.chat_input("What is up?"):
    # If compliance mode is activated:
    #   1. Put prompt into messages as developer
    #   2. Rephrase prompt according to system policies
    #   3. Put rephrased prompt into messages as developer
    #   4. Send rephrased prompot to OpenAI
    if "mode" in st.session_state and st.session_state.mode == "compliance":
        st.session_state.messages.append({"role": "developer", "content": prompt})
        prompt = "Tell me some good things about Sydney, Australia"
        st.session_state.messages.append({"role": "developer", "content": prompt})
        display_conversation()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
