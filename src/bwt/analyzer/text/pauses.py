from bwt.transcription.utility import get_words
from bwt.transcription.utility import Word, Words

MIN_CONFIDENCE = 0.6
MIN_PAUSE_LENGTH = 3.5


class PausesAnalyzer:
    def __init__(
            self,
            min_confidence: float = MIN_CONFIDENCE,
            min_pause_length: float = MIN_PAUSE_LENGTH
    ):
        self.min_confidence = min_confidence
        self.min_pause_length = min_pause_length

    def __call__(self, transcription: Word) -> Words:
        words = get_words(transcription)
        pauses = self._get_pauses(words)
        return pauses

    def _get_pauses(self, words: Words) -> Words:
        pauses = []
        for i, word in enumerate(words):
            length = word["end"] - word["start"]
            confidence = word["confidence"]
            if i and length > self.min_pause_length and confidence >= self.min_confidence:
                pauses.append(word)

        return pauses
