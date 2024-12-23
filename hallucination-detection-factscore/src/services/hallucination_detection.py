from typing import Dict, List
from ..models.open_ai import OpenAIModel
from ..prompts.all_prompts import CONTENT_FACT_CHECKER


def detect(source: str, atomic_facts: List[Dict]) -> Dict:
    # Go through atomic facts to see which are supported
    model = OpenAIModel(
        # model="fact_checker",
        name="gpt-3.5-turbo",
        prompts=CONTENT_FACT_CHECKER,
        fact_checker=True,
    )

    atomic_facts[0]["facts"].append("My dog went for a walk.")

    results = {}
    for item in atomic_facts:
        sentence = item["sentence"]
        facts = item["facts"]
        if sentence not in results:
            results[sentence] = {"facts": facts, "supported": []}

        for fact in facts:
            evidence_and_fact = {
                "evidence": source,
                "fact": fact,
            }

            response = model.model_predict(data=evidence_and_fact)
            supported = (
                response[0].to_dict()["choices"][0]["message"]["content"].lower()
            )

            fact_supported = True if "true" in supported else False
            if fact_supported:
                results[sentence]["supported"].append(True)
            else:
                results[sentence]["supported"].append(False)

    # LLM-based approach to hallucination detection
    # Fact score from:
    # FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long
    # Form Text Generation (Min, 2023)
    result_json = {"sentences": [], "scores": []}

    for sentence in results.keys():
        facts = results[sentence]["facts"]
        supported = results[sentence]["supported"]
        true = sum([1 for fact_supported in supported if fact_supported])
        total = len(facts)
        result_json["sentences"].append(sentence)

        score = int(true / total * 100)
        if score == 0:
            # score == 0 was doing something weird on the front end
            score = 1
        result_json["scores"].append(score)
    print()

    factscore = int(sum(result_json["scores"]) / len(result_json["scores"]))

    result_json["factscore"] = factscore
    return result_json
