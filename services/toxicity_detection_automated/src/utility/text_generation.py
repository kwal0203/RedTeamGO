from typing import Any


def generate_text(
    red_lm: Any,
    prompt: Any,
    max_tokens: int,
    sample: bool,
    top_p: float,
    top_k: float,
):
    """
    Helper function that obtains text from LLM. This function is used to generate
    questions that are intended to be inserted into target model.
    """
    response = red_lm.model.generate(
        **prompt,
        max_new_tokens=max_tokens,
        do_sample=sample,
        top_p=top_p,
        top_k=top_k,
        pad_token_id=red_lm.tokenizer.eos_token_id,
    )
    return red_lm.tokenizer.decode(response[0][prompt.input_ids[0].shape[0] :]).strip()
