from statistics import mean
from typing import Any, Dict

import streamlit as st

from tokenizer.tokenizer import Tokenizer
from transcription.utility import get_words, get_sentences


class Statistics:
    def __init__(self, result: Dict[str, Any]):
        self.analysis = result["analysis"]
        self.transcription = result["transcription"]
        self.words = get_words(self.transcription)
        self.sentences = get_sentences(self.transcription, Tokenizer())

    def get_statistics(self):
        square_mean_word_length = mean(self.analysis["square_mean_word_lengths"])
        numerals_count = mean(self.analysis["numerals_count"])
        sentence_lengths = self.analysis["sentence_lengths"]
        word_count = len(self.words)
        sentence_count = len(self.sentences)
        gunning_fog = self.analysis["gunning_fog"]

        total_sentences = len(self.sentences)
        repetitions = self.analysis["repetitions"]
        topic_changes = self.analysis["topic_change"]
        jargon_words = self.analysis["jargon"]
        foreign_words = self.analysis["foreign_words"]
        passive_voice_sentences = self.analysis["passive_voice"]

        # Obliczenia metryk
        repetitions_per_sentence = len(repetitions) / total_sentences
        topic_changes_per_sentence = len(topic_changes) / total_sentences
        jargon_words_per_sentence = len(jargon_words) / total_sentences
        foreign_words_per_sentence = len(foreign_words) / total_sentences
        passive_voice_ratio = len(passive_voice_sentences) / total_sentences

        # Tworzenie kolumn w Streamlit
        colA, colB, colC = st.columns(3)
        colA.metric("Liczba słów", word_count, help="Liczba słów")
        colB.metric("Liczba zdań", sentence_count, help="Liczba zdań")
        colC.metric("Gunning FOG", gunning_fog, help="Indeks mglistości")

        col1, col2, col3, col4 = st.columns(4)

        # Dodawanie metryk do kolumn
        col1.metric("Długość słów", f"{square_mean_word_length:.2f}", help="Średnia długość słów na zdanie")
        col2.metric("Liczebniki", f"{numerals_count}", help="Średnia liczba liczebników w zdaniu")
        col3.metric("Długość zdań", f"{mean(sentence_lengths):.2f}", help="Średnia liczba słów w zdaniu")
        col4.metric("Powtórzenia na zdanie", f"{repetitions_per_sentence:.2f}", help="Średnia liczba powtórzeń na zdanie")

        # Tworzenie nowych kolumn dla kolejnych metryk
        col6, col7, col8, col9 = st.columns(4)

        # Dodawanie kolejnych metryk do nowych kolumn
        col6.metric("Zmiany tematów na zdanie", f"{topic_changes_per_sentence:.2f}", help="Średnia liczba zmian tematów na zdanie")
        col7.metric("Słów profesjonalnych na zdanie", f"{jargon_words_per_sentence:.2f}", help="Średnia liczba słów profesjonalnych na zdanie")
        col8.metric("Obcych wyrażeń na zdanie", f"{foreign_words_per_sentence:.2f}", help="Średnia liczba obcych wyrażeń na zdanie")
        col9.metric("Zdania w stronie biernej", f"{passive_voice_ratio:.2f}", help="Proporcja zdań w stronie biernej")
