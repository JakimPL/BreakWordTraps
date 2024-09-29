import math
from typing import Any, Dict, List

from bwt.analyzer.text.analyzer import TextAnalyzer
from bwt.tokenizer.syllablizer import Syllablizer
from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import Words, get_sentences
from bwt.transcription.utility import get_words

MIN_HARD_WORDS_SYLLABLES = 4


class GunningFogIndex(TextAnalyzer):
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
        interpretation = self._get_interpretation(fog)
        return {
            "gunning_fog": fog,
            "gunning_fog_interpretation": interpretation
        }

    def _get_hard_words(self, words: Words) -> List[str]:
        hard_words = []
        for word in words:
            text = word["text"]
            syllables = self.syllablizer(text)
            if len(syllables) >= self.min_hard_words_syllables:
                hard_words.append(text)

        return hard_words

    @staticmethod
    def _get_interpretation(fog: float) -> str:
        fog_rounded = math.ceil(fog)
        if fog_rounded <= 6:
            return "Język bardzo prosty, zrozumiały już dla uczniów szkoły podstawowej."
        elif fog_rounded <= 9:
            return "Język prosty, zrozumiały już dla uczniów gimnazjum."
        elif fog_rounded <= 12:
            return "Język dość prosty, zrozumiały już dla uczniów liceum."
        elif fog_rounded <= 15:
            return "Język dość trudny, zrozumiały dla studentów studiów licencjackich."
        elif fog_rounded <= 17:
            return "język trudny, zrozumiały dla studentów studiów magisterskich."
        else:
            return "Język bardzo trudny, zrozumiały dla magistrów i osób z wyższym wykształceniem."
