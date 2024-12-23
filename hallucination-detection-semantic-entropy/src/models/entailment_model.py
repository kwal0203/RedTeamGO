from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
from env import device

import torch


class EntailmentDeberta:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/deberta-v2-xlarge-mnli"
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "microsoft/deberta-v2-xlarge-mnli"
        ).to(device)

    def check_implication(self, text1, text2, *args, **kwargs):
        # The model checks if text1 -> text2, i.e. if text2 follows from text1.
        inputs = self.tokenizer(text1, text2, return_tensors="pt").to(device)
        outputs = self.model(**inputs)
        logits = outputs.logits

        # Deberta-mnli returns `neutral` and `entailment` classes at indices 1 and 2.
        largest_index = torch.argmax(F.softmax(logits, dim=1))
        prediction = largest_index.cpu().item()
        return prediction
