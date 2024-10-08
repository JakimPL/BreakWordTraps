from typing import Any, Dict, List

from bwt.analyzer.text.text_analyzer import TextAnalyzer
from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import Word
from bwt.transcription.utility import get_sentences_with_words, join_sentence

MIN_NUMERALS_IN_SENTENCE = 3


class NumeralsAnalyzer(TextAnalyzer):
    name: str = "numerals"

    def __init__(self, min_numerals_in_sentence: int = MIN_NUMERALS_IN_SENTENCE):
        self.min_numerals_in_sentence = min_numerals_in_sentence

        self.tokenizer = Tokenizer()

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Any]:
        sentences = get_sentences_with_words(transcription, self.tokenizer)
        sentence_with_numerals = []
        numerals_count = []
        for sentence in sentences:
            numerals = self._get_numerals(sentence)
            numerals_count.append(len(numerals))
            if len(numerals) >= self.min_numerals_in_sentence:
                sentence_with_numerals.append({
                    "text": join_sentence(sentence),
                    "start": sentence[0]["start"],
                    "end": sentence[-1]["end"],
                    "numerals": numerals
                })

        return {
            self.name: sentence_with_numerals,
            "numerals_count": numerals_count
        }

    @staticmethod
    def _get_numerals(sentence: List[Word]) -> List[str]:
        numerals = []
        for word in sentence:
            text = word["text"]
            if any(char.isdigit() for char in text):
                numerals.append(text)

        return numerals
