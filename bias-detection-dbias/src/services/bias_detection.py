from typing import List
from transformers import (
    TFAutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)


def detect_bias(response: List[str]):
    """
    Helper function to detect biased language in model reponse. The model is
    from:

    Raza, S., Reji, D.J. & Ding, C. Dbias: detecting biases and ensuring
    fairness in news articles. Int J Data Sci Anal 17, 39-59 (2024).
    https://doi.org/10.1007/s41060-022-00359-4.
    """

    PATH = "/scratch3/wal740/eval_models/bias-detection-model"
    tokenizer = AutoTokenizer.from_pretrained(PATH)
    model = TFAutoModelForSequenceClassification.from_pretrained(PATH)
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    classification_output = classifier(response)
    return {
        "evaluation_bias": classification_output,
    }
