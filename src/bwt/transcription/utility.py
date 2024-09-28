from typing import Any, Dict, List

from bwt.tokenizer.tokenizer import Tokenizer

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


def get_sentences(transcription: Dict[str, Any], tokenizer: Tokenizer) -> List[str]:
    sentences = tokenizer(get_text(transcription), sentences=True)
    return sentences


def get_sentence_map(transcription: Dict[str, Any], tokenizer: Tokenizer) -> Dict[int, int]:
    words = get_words(transcription)
    sentences = get_sentences(transcription, tokenizer)

    sentence_map = {}
    sentence_id = 0
    sentence = str(sentences[0])
    for i, word in enumerate(words):
        text = word["text"]
        while True:
            start = str(sentence).find(text)
            if start < 0:
                sentence_id += 1
                sentence = str(sentences[sentence_id])
            else:
                break

        sentence = sentence[start:]
        sentence_map[i] = sentence_id

    return sentence_map


def get_sentences_with_words(transcription: Dict[str, Any], tokenizer: Tokenizer) -> List[Words]:
    words = get_words(transcription)
    sentence_map = get_sentence_map(transcription, tokenizer)
    sentences = [[] for _ in set(sentence_map.values())]
    for word_id, sequence_id in sentence_map.items():
        sentences[sequence_id].append(words[word_id])

    return sentences


def join_sentence(sentence: Words) -> str:
    return " ".join([word["text"] for word in sentence])


def find_sublist_indices(suplist: List[str], sublist: List[str]):
    sublist_len = len(sublist)
    for i in range(len(suplist) - sublist_len + 1):
        if suplist[i:i + sublist_len] == sublist:
            return i, i + sublist_len - 1
