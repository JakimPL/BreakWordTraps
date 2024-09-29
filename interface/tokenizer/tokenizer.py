from typing import List

import spacy

NLP_MODEL = "pl_core_news_sm"


class Tokenizer:
    def __init__(self, nlp_model: str = NLP_MODEL):
        self.nlp = spacy.load(nlp_model)

    def __call__(self, item: str, sentences: bool = False) -> List[str]:
        if sentences:
            return list(map(str, self.nlp(item).sents))

        return list(map(str, self.nlp(item)))
