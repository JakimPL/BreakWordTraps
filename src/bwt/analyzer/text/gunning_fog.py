import math
from typing import Any, Dict, List

from bwt.analyzer.text.analyzer import Analyzer
from bwt.tokenizer.syllablizer import Syllablizer
from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import Words, get_sentences
from bwt.transcription.utility import get_words

MIN_HARD_WORDS_SYLLABLES = 4


class GunningFogIndex(Analyzer):
    name: str = "gunning_fog"

    def __init__(self, min_hard_words_syllables: int = MIN_HARD_WORDS_SYLLABLES):
        self.min_hard_words_syllables = min_hard_words_syllables

        self.tokenizer = Tokenizer()
        self.syllablizer = Syllablizer()

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, float]:
        words = get_words(transcription)
        word_count = len(words)
        sentence_count = len(get_sentences(transcription, self.tokenizer))
        hard_word_count = len(self._get_hard_words(words))

        fog = 0.4 * (word_count / sentence_count + 100 * hard_word_count / word_count)
        return {self.name: fog}

    def _get_hard_words(self, words: Words) -> List[str]:
        hard_words = []
        for word in words:
            text = word["text"]
            syllables = self.syllablizer(text)
            if len(syllables) >= self.min_hard_words_syllables:
                hard_words.append(text)

        return hard_words
