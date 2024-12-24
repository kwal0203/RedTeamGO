from src.utility.atomic_facts import get_atomic_facts
from src.services.hallucination_detection import detect

import nltk

from typing import Any


def service(args: Any) -> Any:
    # TODO: Convert to Google style comments

    ### FActScore
    # Summary
    # LLM-based approach to hallucination detection
    # Fact score from:
    # FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long
    # Form Text Generation (Min, 2023)
    generated_summary = args.summary

    # Split generation into sentences
    sentences = nltk.tokenize.sent_tokenize(generated_summary)

    # Get atomic facts
    # Note: they have alot of weird conditions like checking for sentences that start with "Sure"
    # Note: For each sentence want to see if that sentence makes a factual claim about genomics
    # Note: One issue is that some sentences are not atomic true/false statements
    #       - hallucination is different to off-topic i.e. when inserting comments about swimmingS
    atomic_facts = get_atomic_facts(sentences=sentences)
    result_json = detect(source=args.source, atomic_facts=atomic_facts)
    result_json["summary"] = generated_summary

    return result_json
