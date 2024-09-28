import json
from typing import Any, Dict, List, Optional

from bwt.analyzer.text.analyzer import Analyzer
from bwt.logger import get_logger
from bwt.prompter.prompter import Prompter
from bwt.transcription.utility import Words
from bwt.transcription.utility import (
    find_sublist_indices,
    get_sentences,
    get_sentences_with_words,
    tokenize
)


class CombinedAnalyzer(Analyzer):
    name: str = "combined"

    def __init__(self):
        self.logger = get_logger("CombinedAnalyzer")
        self.prompter = Prompter()
        self.content = """Jesteś językoznawcą z 20-letnim doświadczeniem w badaniu języka polskiego w kontekście występów publicznych. Zwracasz baczną uwagę na szczegóły związane z jasnością przekazu i korzystając z doświadczenia, wiedzy i wyczucia potrafisz doskonale ocenić jakość czyjegoś wystąpienia.

Jako input dostaniesz TEKST"""
        self.message = """ZADANIE:
Zadanie składa się z 5 części.

    1. Oceń liczbę POWTÓRZEŃ w poniższym TEKŚCIE. Zlicz, ile razy każde słowo lub wyrażenie występuje w tekście. Określ w jakiej odległości od siebie znajdują się te powtórzenia. Zacytuj fragmenty, w których są powtórzenia.
    2. Oceń, czy w TEKŚCIE występują ZMIANY TEMATU. Twoim zadaniem jest zanalizować semantykę, zidentyfikować główny temat przewodni w TEKŚCIE i sprawdzić, czy wszystkie treści są z tym temaetm koherentne. Jeśli pojawiają się treści, które ewidentnie nie pasują do tematu i nie wiążą się z poprzednią treścią, wskaż fragment TEKSTU, w którym nastąpiła zmiana.
    3. Zidentyfikuj użycie ŻARGONU w TEKŚCIE. Żargon to wysokospecjalistyczne słownictwo, które trudno zrozumiałe dla osób z zewnątrz. Oceń je w kontekście całych zdań. Wymień zdania, w których jest duże nagromadzenie specjalistycznych terminów, które mogą utrudniać rozumienie. Wymień te terminy.
    4. Sprawdź, czy w TEKŚCIE występują OBCE SŁOWA. OBCE SŁOWA to słowa, które nie są w języku polskim. Podaj te słowa lub wyrażenia.
    5. Zidentyfikuj UŻYCIE STRONY BIERNEJ w TEKŚCIE. Analizuj konstrukcje gramatyczne w TEKŚCIE i znajdź zdania, które są w wyrażone w stronie biernej. Wskaż te zdania.

Wynik podaj w postaci słownika JSON bez żadnej dodatkowej treści.
{
    "repetitions": <lista fragmentów, w których występują powtórzenia>
    "topic_change": [fragment, w którym zmienia się temat]
    "jargon": <lista wysokospecjalistycznych słów>}
    "foreign_words": <lista obcych wyrażeń>,
    "passive_voice": <lista zdań, w których użyto stronę bierną>
}
"""

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Optional[Words]]:
        sentences = get_sentences(transcription)
        text = json.dumps(sentences, indent=4, ensure_ascii=False)
        messages = [self.message, text]
        response = self.prompter(
            content=self.content,
            messages=messages
        )

        self.logger.info(f"Response: {response}")

        if response is not None:
            sentences = get_sentences_with_words(transcription)
            return {
                key: self._process_response(value, sentences)
                for key, value in response.items()
            }

    @staticmethod
    def _process_response(response: List[str], sentences: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        mixed_language_fragments = []
        for sentence_id, fragments in enumerate(response):
            for fragment in fragments:
                response_sentence = tokenize(fragment)
                if sentence_id >= len(sentences):
                    continue

                sentence_words = [word["text"] for word in sentences[sentence_id]]
                result = find_sublist_indices(sentence_words, response_sentence)
                if result is not None:
                    start, end = result
                    start = sentences[sentence_id][start]["start"]
                    end = sentences[sentence_id][end]["end"]
                    mixed_language_fragments.append({
                        "text": fragment,
                        "start": start,
                        "end": end
                    })

        return mixed_language_fragments
