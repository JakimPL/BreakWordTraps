import math
from typing import Any, Dict

from bwt.analyzer.text.text_analyzer import TextAnalyzer
from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import Words
from bwt.transcription.utility import get_sentences_with_words, join_sentence

MAX_SQUARE_MEAN_WORD_LENGTH = 6.0


class LongWordsAnalyzer(TextAnalyzer):
    name: str = "long_words"

    def __init__(self, max_square_mean_word_length: int = MAX_SQUARE_MEAN_WORD_LENGTH):
        self.max_square_mean_word_length = max_square_mean_word_length

        self.tokenizer = Tokenizer()

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Words]:
        sentences = get_sentences_with_words(transcription, self.tokenizer)

        sentences_with_long_words = []
        for sentence in sentences:
            if not sentence:
                continue

            words = [word["text"] for word in sentence]

            # square mean word length
            square_mean_word_length = math.sqrt(sum(
                len(word) ** 2 for word in words
            ) / len(words))

            if square_mean_word_length > self.max_square_mean_word_length:
                text = join_sentence(sentence)
                start = sentence[0]["start"]
                end = sentence[-1]["end"]
                sentences_with_long_words.append({
                    "text": text,
                    "start": start,
                    "end": end,
                    "square_mean_word_length": square_mean_word_length
                })

        return {self.name: sentences_with_long_words}
