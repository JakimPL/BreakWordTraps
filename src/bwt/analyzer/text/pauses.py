from bwt.transcription.utility import Word, Words, get_words

MIN_CONFIDENCE = 0.6


class PausesAnalyzer:
    def __call__(self, transcription: Word) -> Words:
        words = get_words(transcription)
        pauses = self._get_pauses(words)
        return pauses

    @staticmethod
    def _get_pauses(words: Words) -> Words:
        pauses = []
        for i, word in enumerate(words):
            length = word["end"] - word["start"]
            confidence = word["confidence"]
            if i and length > 4 and confidence >= MIN_CONFIDENCE:
                pauses.append(word)

        return pauses
