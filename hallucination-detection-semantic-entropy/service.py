from src.models.entailment_model import EntailmentDeberta
from src.services.semantic_ids import get_semantic_ids
from src.utility.misc import get_generations

from typing import Any


def service(args: Any) -> Any:
    # args.logprobs: Log probabilities for each token in summary

    ### SEMANTIC ENTROPY
    # Semantic similarity approach to hallucination
    #
    # SEMANTIC UNCERTAINTY: LINGUISTIC INVARIANCES FOR UNCERTAINTY ESTIMATION IN NATURAL LANGUAGE GENERATION (Kuhn, 2023)
    # Table 2: Incorrectly answered questions have more semantically distinct answers than correct ones.
    # On its own, this count is a reasonable uncertainty measure, though semantic entropy is better. ()
    # Proof of concept hallucination detection system using semantic entropy for document summarization.

    prompt = args.prompt

    # NOTE: Code currently broken:
    #   - Refactor code to remove session_state from the streamlit front end

    # Load entailment model
    if entailment_model == "deberta":
        entailment_model = EntailmentDeberta()

    semantic_ids = []
    generations = get_generations(
        session_state=args.session_state,
        prompt=prompt,
        num_generations=2,
        temperature=0.9,
    )

    responses = [response[0] for response in generations]
    semantic_ids = get_semantic_ids(strings_list=responses, model=entailment_model)
    semantic_id_score = -(len(set(semantic_ids)) / len(generations)) + 1
    semantic_id_score = int(semantic_id_score * 100)
    result_json = {"semantic_entropy": semantic_id_score}

    return result_json
