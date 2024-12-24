from typing import Any

import math


def service(args: Any) -> Any:
    # Token level model confidence approach to hallucination
    # Seq-logprobs from:
    # Looking for a Needle in a Haystack: A Comprehensive Study of
    # Hallucinations in Neural Machine Translation (Guerreiro, 2023)
    # Proof of concept hallucination detection system using model confidence method for document summarization.

    ### Model confidence
    logprobs = args.logprobs
    avg_logprobs = sum([log_prob["logprob"] for log_prob in logprobs]) / len(logprobs)
    seq_logprob = int(math.exp(avg_logprobs) * 100)
    result_json = {"model_confidence": seq_logprob}

    return result_json
