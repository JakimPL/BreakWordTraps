from typing import Any, Dict

from bwt.transcription.utility import get_text, get_words
from bwt.transcription.utility import Words

MAX_SENTENCE_LENGTH = 35


class LongSentencesAnalyzer:
    def __init__(self, max_sentence_length: int = MAX_SENTENCE_LENGTH):
        self.max_sentence_length = max_sentence_length

    def __call__(self, transcription: Dict[str, Any]) -> Words:
        text = get_text(transcription)
        words = get_words(transcription)
        sentences = text.split('.')

        total_length = 0
        long_sentences = []
        for sentence in sentences:
            if not sentence:
                continue
            sentence = sentence.strip()
            sentence_words = sentence.split()
            sentence_length = len(sentence_words)
            start = words[total_length]["start"]
            end = words[total_length + sentence_length - 1]["end"]
            total_length += sentence_length
            if sentence_length > 15:
                long_sentences.append({
                    "sentence": sentence,
                    "length": sentence_length,
                    "start": start,
                    "end": end
                })

        return long_sentences
