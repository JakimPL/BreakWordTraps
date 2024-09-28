from typing import Any, Dict, List

from bwt.analyzer.text.analyzer import Analyzer
from bwt.transcription.utility import Word, Words
from bwt.transcription.utility import get_sentences_with_words, join_sentence

MIN_NUMERALS_IN_SENTENCE = 3


class NumeralsAnalyzer(Analyzer):
    name: str = "numerals"

    def __init__(self, min_numerals_in_sentence: int = MIN_NUMERALS_IN_SENTENCE):
        self.min_numerals_in_sentence = min_numerals_in_sentence

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Words]:
        sentences = get_sentences_with_words(transcription)
        sentence_with_numerals = []
        for sentence in sentences:
            numerals = self._get_numerals(sentence)
            if len(numerals) >= self.min_numerals_in_sentence:
                sentence_with_numerals.append({
                    "text": join_sentence(sentence),
                    "start": sentence[0]["start"],
                    "end": sentence[-1]["end"],
                    "numerals": numerals
                })

        return {self.name: sentence_with_numerals}

    @staticmethod
    def _get_numerals(sentence: List[Word]) -> List[str]:
        numerals = []
        for word in sentence:
            text = word["text"]
            if any(char.isdigit() for char in text):
                numerals.append(text)

        return numerals
