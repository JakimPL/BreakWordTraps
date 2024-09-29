from typing import Any, Dict

from bwt.analyzer.text.analyzer import TextAnalyzer
from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import Words
from bwt.transcription.utility import get_sentences_with_words, join_sentence

MAX_SENTENCE_LENGTH = 15


class LongSentencesAnalyzer(TextAnalyzer):
    name: str = "long_sentences"

    def __init__(self, max_sentence_length: int = MAX_SENTENCE_LENGTH):
        self.max_sentence_length = max_sentence_length

        self.tokenizer = Tokenizer()

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Words]:
        sentences = get_sentences_with_words(transcription, self.tokenizer)

        total_length = 0
        long_sentences = []
        for sentence in sentences:
            if not sentence:
                continue

            text = join_sentence(sentence)
            sentence_length = len(sentence)
            start = sentence[0]["start"]
            end = sentence[-1]["end"]
            total_length += sentence_length
            if sentence_length > self.max_sentence_length:
                long_sentences.append({
                    "text": text,
                    "start": start,
                    "end": end,
                    "sentence_length": sentence_length
                })

        return {self.name: long_sentences}
