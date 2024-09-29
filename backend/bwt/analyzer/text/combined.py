import json
from typing import Any, Dict, List, Optional

from bwt.analyzer.text.text_analyzer import TextAnalyzer
from bwt.logger import get_logger
from bwt.prompter.prompter import Prompter
from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import Words
from bwt.transcription.utility import (
    find_sublist_indices,
    get_sentences,
    get_words
)


class CombinedAnalyzer(TextAnalyzer):
    name: str = "combined"

    def __init__(self):
        self.logger = get_logger("CombinedAnalyzer")
        self.tokenizer = Tokenizer()
        self.prompter = Prompter()
        self.content = """Jesteś językoznawcą z 20-letnim doświadczeniem w badaniu języka polskiego w kontekście występów publicznych. Zwracasz baczną uwagę na szczegóły związane z jasnością przekazu i korzystając z doświadczenia, wiedzy i wyczucia potrafisz doskonale ocenić jakość czyjegoś wystąpienia.

Jako input dostaniesz TEKST"""
        self.message = """ZADANIE:
Zadanie składa się z 5 części.

    1. Oceń liczbę POWTÓRZEŃ w poniższym TEKŚCIE. Zlicz, ile razy każde słowo lub wyrażenie występuje w tekście. Określ w jakiej odległości od siebie znajdują się te powtórzenia. Zacytuj fragmenty, w których są powtórzenia.
    2. Oceń, czy w TEKŚCIE występują ZMIANY TEMATU. Twoim zadaniem jest zanalizować semantykę, zidentyfikować główny temat przewodni w TEKŚCIE i sprawdzić, czy wszystkie treści są z tym temaetm koherentne. Jeśli pojawiają się treści, które ewidentnie nie pasują do tematu i nie wiążą się z poprzednią treścią, wskaż fragment TEKSTU, w którym nastąpiła zmiana.
    3. Zidentyfikuj użycie ŻARGONU w TEKŚCIE. Żargon to wysokospecjalistyczne słownictwo, które trudno zrozumiałe dla osób z zewnątrz. Oceń je w kontekście całych zdań. Wymień zdania, w których jest duże nagromadzenie specjalistycznych terminów, które mogą utrudniać rozumienie. Wymień te terminy.
    4. Sprawdź, czy w TEKŚCIE występują OBCE WYRAŻENIA. OBCE WYRAŻENIA to słowa lub ciągi słów, które nie występują w języku polskim. Podaj te słowa lub wyrażenia.
    5. Zidentyfikuj UŻYCIE STRONY BIERNEJ w TEKŚCIE. Analizuj konstrukcje gramatyczne w TEKŚCIE i znajdź zdania, które są w wyrażone w stronie biernej. Wskaż te zdania.

Cytuj fragmenty dokładnie z ich oryginalną pisownią. Wynik podaj w postaci słownika JSON bez żadnej dodatkowej treści.

{
    "repetitions": <lista fragmentów, w których występują powtórzenia>
    "topic_change": <lista fragmentów, w którym zmienia się temat>,
    "jargon": <lista fragmentów, w których występują wysokospecjalistyczne wyrażenia>}
    "foreign_words": <lista obcych wyrażeń>,
    "passive_voice": <lista zdań, w których użyto stronę bierną>
}
"""

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Optional[Words]]:
        sentences = get_sentences(transcription, self.tokenizer)
        text = json.dumps(sentences, indent=4, ensure_ascii=False)
        messages = [self.message, text]
        response = self.prompter(
            content=self.content,
            messages=messages
        )

        self.logger.info(f"Response: {response}")

        if response is not None:
            words = get_words(transcription)
            return {
                key: self._process_response(value, words)
                for key, value in response.items()
            }

    def _process_response(self, fragments: List[str], words: Words) -> List[Dict[str, Any]]:
        bad_fragments = []
        for fragment in fragments:
            response_sentence = self.tokenizer(fragment)
            sentence_words = [word["text"] for word in words]
            result = find_sublist_indices(sentence_words, response_sentence)
            if result is not None:
                start, end = result
                start = words[start]["start"]
                end = words[end]["end"]
                bad_fragments.append({
                    "text": fragment,
                    "start": start,
                    "end": end
                })

        return bad_fragments
