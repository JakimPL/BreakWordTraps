from typing import Any, Dict, List

Word = Dict[str, Any]
Words = List[Word]


def get_words(transcription: Dict[str, Any]) -> List[Word]:
    words = []
    for segment in transcription["segments"]:
        words.extend(segment["words"])

    return words


def get_segments(transcription: Dict[str, Any]) -> List[str]:
    segments = []
    for segment in transcription["segments"]:
        segments.append(segment["text"].strip())

    return segments


def get_text(transcription: Dict[str, Any]) -> str:
    return transcription["text"].strip()
