from typing import Any, Dict, List, Tuple
from annotated_text import annotated_text

from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import get_words
from bwt.transcription.utility import Words

COLOR_MAP = {
    "pauses": "#fae73c",
    "passive_voice": "#fbbd1e",
    "fast_speaking": "#ff6513",
    "long_sentences": "#a6ddff",
    "repetitions": "#a6ddff",
    "foreign_words": "#1632b0",
    "topic_change": "#8c4eb1",
    "jargon": "#7f153b",
    "long_words": "#ff823f",
}

SHORTCUT_MAP = {
    "pauses": "pauza",
    "passive_voice": "strona bierna",
    "fast_speaking": "szybka mowa",
    "long_sentences": "długie zdanie",
    "repetitions": "powtórzenie",
    "foreign_words": "język obcy",
    "topic_change": "zmiana tematu",
    "jargon": "żargon",
    "long_words": "długie słowa",
}


class TranscriptionProcessor:
    def __init__(self, result: Dict[str, Any], transcription_box: Any):
        self.tokenizer = Tokenizer()
        self.result = result
        self.transcription_box = transcription_box
        self.ranges = self.prepare_ranges()

    @staticmethod
    def find_word(words: Words, index: int, start: bool = True):
        field = "start" if start else "end"
        item = [word for word in words if word[field] == index][0]
        return words.index(item)

    def fill_transcription(self) -> None:
        transcription = self.result.get("transcription", {}).get("text", "").strip()
        words = self.tokenizer(transcription)

        # Create a list for annotated text
        annotated_words = []
        i = 0
        while i < len(words):
            for start, end, color, label in self.ranges:
                if start <= i < end:
                    group = " ".join(words[start:end])
                    annotated_words.append((group, label, color))
                    i = end
                    break
            else:
                annotated_words.append(f"{words[i]} ")
                i += 1

        with self.transcription_box:
            annotated_text(*annotated_words)

    def get_ranges(self, group: Words, words: Words, color: str, label: str) -> List[Tuple[int, int, str, str]]:
        ranges = []
        for sentence in group:
            start = sentence["start"]
            end = sentence["end"]
            try:
                start_word = self.find_word(words, start, start=True)
                end_word = self.find_word(words, end, start=False)
            except IndexError:
                continue
            ranges.append((start_word, end_word, color, label))

        return ranges

    def prepare_ranges(self) -> List[Tuple[int, int, str, str]]:
        transcription = self.result.get("transcription", {})
        analysis = self.result.get("analysis", {})
        words = get_words(transcription)
        ranges = []

        for key in COLOR_MAP.keys():
            group = analysis.get(key, [])
            ranges.extend(self.get_ranges(
                group, words, COLOR_MAP[key], SHORTCUT_MAP[key]
            ))

        return ranges
