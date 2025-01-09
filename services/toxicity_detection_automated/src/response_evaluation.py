from services.model_wrappers.huggingface_model import HuggingFaceModel
from toxicity_detection import detect_toxicity
from text_generation import generate_text
from typing import List, Dict, Any
from utils.config import device
from system_prompt import PROMPT

import pandas as pd


def evaluate_zero_shot_questions(
    red_lm: Any, questions: List[Dict[str, str]], local: bool
) -> Dict[str, Any]:
    dataset_distribtuion = {}
    generated_answers = []
    for item in questions:
        # Track how many questions we get from each dataset
        dataset = item["dataset"]
        if dataset not in dataset_distribtuion:
            dataset_distribtuion[dataset] = 0
        dataset_distribtuion[dataset] += 1

        # Formulate prompt in format from Perez et al. (2022)
        question = item["text"]
        question_prompt = PROMPT + "\nUSER: " + question + "\nGOPHER:"

        if local:
            question_prompt = red_lm.tokenizer(question_prompt, return_tensors="pt").to(
                device
            )

        generated_text = generate_text(
            red_lm=red_lm,
            prompt=question_prompt,
            max_tokens=100,
            sample=True,
            top_p=0.8,
            top_k=0,
            local=local,
        )
        generated_answers.append(generated_text)

    ### Evaluate the toxicity of generated text and return in JSON format
    result = classify_toxicity(
        questions=questions, answers=generated_answers, name="zero"
    )
    return result


def evaluate_few_shot_questions(
    red_lm: HuggingFaceModel, questions: List[str]
) -> List[str]:
    """
    Helper function that generates questions and answers for the automated
    vulnerability discovery mode. This function handles few shot questions
    and answers.
    """

    ### Generate answers to few shot questions
    generated_answers = []
    for question in questions:
        question_prompt = PROMPT + "\nUSER: " + question + "\nGOPHER:"
        enc_question_prompt = red_lm.tokenizer(question_prompt, return_tensors="pt").to(
            device
        )
        generated_text = generate_text(
            red_lm=red_lm,
            prompt=enc_question_prompt,
            max_tokens=50,
            sample=True,
            top_p=0.8,
            top_k=0,
        )
        generated_answers.append(generated_text)

    ### Evaluate the toxicity of generated answers and store in CSV file
    result_json = classify_toxicity(
        questions=questions, answers=generated_answers, name="few"
    )
    return result_json


def classify_toxicity(questions: List[str], answers: List[str], name: str) -> None:
    """
    Helper function that classifies the toxicity of zero shot examples for the
    automated vulnerability discovery mode. This function handles zero shot
    questions and answers.
    """
    transformed_answers = []
    toxicity_scores = []
    for question, answer in zip(questions, answers):
        answer = answer.replace("\n", " ")
        toxicity_score = detect_toxicity(response=answer)[0]["probabilities_toxicity"]
        toxicity_scores.append(toxicity_score)
        transformed_answers.append(answer)

    df = pd.DataFrame()
    df["question"] = questions
    df["answer"] = transformed_answers
    df["toxicity_score"] = toxicity_scores
    result_json = df.to_json(orient="records")
    return result_json
