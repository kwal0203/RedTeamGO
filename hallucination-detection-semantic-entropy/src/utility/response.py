from typing import Any
import streamlit as st
import random


def response_generator(model_name: str, prompt: str) -> Any:
    """
    This function enters input prompts into the selected model and obtains the generated responses.

    Args:
        prompt (str): TODO.
    """

    # NOTE: Code currently broken:
    #   - Refactor code to remove session_state from the streamlit front end

    if model_name != "llama3-instruct":
        print("A")
        stream = session_state.model_client.chat.completions.create(
            model=session_state.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            logprobs=True,
        )
    elif session_state.model_name == "gpt-3.5-turbo" and session_state.one_shot == True:
        print("B")
        stream = session_state.model_client.chat.completions.create(
            model=session_state.model_name,
            messages=[
                {"role": "user", "content": random.choice(session_state.prompts)}
            ],
            stream=True,
        )
    elif (
        session_state.model_name == "llama3-instruct" and session_state.one_shot == True
    ):
        # Is this for the batch process?
        print("C")
        stream = session_state.model_client.model_predict(
            data=random.choice(session_state.prompts)
        )
    elif (
        session_state.model_name == "llama3-instruct"
        and session_state.one_shot == False
    ):
        print("D")
        # Is this for the batch process?
        stream = session_state.model_client.model_predict(data=[prompt])
    else:
        print("E")
        stream = session_state.model_client.chat.completions.create(
            model=session_state.model_name,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in session_state.messages
            ],
            stream=True,
        )

    return stream
