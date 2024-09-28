import re

from bwt.transcription.utility import Word, Words
from bwt.transcription.utility import get_sentences_with_words, join_sentence

MIN_CONFIDENCE = 0.6
MIN_SPEED = 6.15
MAX_DURATION = 3.5


class FastSpeakingAnalyzer:
    def __init__(
            self,
            min_confidence: float = MIN_CONFIDENCE,
            max_duration: float = MAX_DURATION,
            min_speed: float = MIN_SPEED
    ):
        self.min_confidence = min_confidence
        self.max_duration = max_duration
        self.min_speed = min_speed

    def __call__(self, transcription: Word) -> Words:
        sentences = get_sentences_with_words(transcription)
        fast_sentences = []
        for sentence in sentences:
            speed = self._process_sentence(sentence)
            text = join_sentence(sentence)
            if speed > self.min_speed:
                fast_sentences.append({
                    "text": text,
                    "speed": speed,
                    "start": sentence[0]["start"],
                    "end": sentence[-1]["end"],
                })

        return fast_sentences

    def _process_sentence(self, sentence_words: Words) -> float:
        # Filter out words with low confidence and too long duration
        words = self._get_fast_words(sentence_words)
        if not words:
            return 0.0

        total_syllabes = 0
        total_length = 0.0
        for word in words:
            syllabes = self._count_syllables(word["text"])
            total_syllabes += syllabes
            length = word["end"] - word["start"]
            total_length += length

        return total_syllabes / total_length

    def _get_fast_words(self, words: Words) -> Words:
        fast_words = []
        for i, word in enumerate(words):
            length = word["end"] - word["start"]
            confidence = word["confidence"]
            if length < self.max_duration and confidence >= self.min_confidence:
                fast_words.append(word)

        return fast_words

    @staticmethod
    def _count_syllables(word: str) -> int:
        pattern = r'([aąeęiouyó]+(?:[łńćźż]+)?|[łńćźż]*?[aąeęiouyó]{1})'
        syllables = re.findall(pattern, word, re.IGNORECASE)
        return len(syllables)
