from typing import Dict

from bwt.analyzer.text.analyzer import Analyzer
from bwt.transcription.utility import Word, Words
from bwt.transcription.utility import get_words

MIN_CONFIDENCE = 0.6
MIN_PAUSE_LENGTH = 3.5


class PausesAnalyzer(Analyzer):
    name: str = "pauses"

    def __init__(
            self,
            min_confidence: float = MIN_CONFIDENCE,
            min_pause_length: float = MIN_PAUSE_LENGTH
    ):
        self.min_confidence = min_confidence
        self.min_pause_length = min_pause_length

    def __call__(self, transcription: Word) -> Dict[str, Words]:
        words = get_words(transcription)
        pauses = self._get_pauses(words)
        return {self.name: pauses}

    def _get_pauses(self, words: Words) -> Words:
        pauses = []
        for i, word in enumerate(words):
            length = word["end"] - word["start"]
            confidence = word["confidence"]
            if i and length > self.min_pause_length and confidence >= self.min_confidence:
                pauses.append({
                    "text": word["text"],
                    "start": word["start"],
                    "end": word["end"]
                })

        return pauses
