from typing import Any, Dict, List

import spacy

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


def get_sentences(transcription: Dict[str, Any]) -> List[str]:
    nlp = spacy.load("pl_core_news_sm")
    sentences = list(map(str, nlp(get_text(transcription)).sents))
    return sentences


def get_sentence_map(transcription: Dict[str, Any]):
    words = get_words(transcription)
    sentences = get_sentences(transcription)

    sentence_map = {}
    sentence_id = 0
    sentence = str(sentences[0])
    for i, word in enumerate(words):
        text = word["text"]
        start = str(sentence).find(text)
        sentence = sentence[start:]
        if not any(x.isalpha() for x in sentence):
            sentence_id += 1
            sentence = str(sentences[sentence_id])

        sentence_map[i] = sentence_id

    return sentence_map


def get_sentences_with_words(transcription: Dict[str, Any]) -> List[Words]:
    words = get_words(transcription)
    sentence_map = get_sentence_map(transcription)
    sentences = [[] for _ in set(sentence_map.values())]
    for word_id, sequence_id in sentence_map.items():
        sentences[sequence_id].append(words[word_id])

    return sentences


def join_sentence(sentence: Words) -> str:
    return " ".join([word["text"] for word in sentence])
