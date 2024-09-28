import json
from json import JSONDecodeError
from typing import Any, Dict, List, Optional

from bwt.prompter.prompter import Prompter
from bwt.transcription.utility import (
    find_sublist_indices,
    get_sentences,
    get_sentences_with_words,
    tokenize
)


class MixedLanguagesAnalyzer:
    def __init__(self):
        self.prompter = Prompter()
        self.content = "Jesteś językoznawcą z 20-letnim doświadczeniem w badaniu języka polskiego w kontekście występów publicznych. Zwracasz baczną uwagę na szczegóły związane z jasnością przekazu i korzystając z doświadczenia, wiedzy i wyczucia potrafisz doskonale ocenić jakość czyjegoś wystąpienia."
        self.message = """
ZADANIE:
Zadanie polega na wskazaniu w liście składających się z paru wypowiedzi anglicyzmów oraz zapożyczeń z języka angielskiego. Poszczególne wypowiedzi są wyróżnione cudzysłowem. Wynik należy podać jako listę bez żadnej dodatkowej treści. Nie podawaj imion i nazwisk. 

PRZYKŁAD
[
    "Komisarz Unii Europejskiej do spraw stabilności finansowej, usług finansowych i Unii Rynków Kapitałowych",
    "Mayread Maguines, Minister Finansów Niemiec Christian Lindner oraz Minister Finansów Francji Bruno Le Maire",
    "wzięli udział w bilateral meetings podczas których uczestnicy dyskutowali m.in. na temat",
    "wzmocnienia solidarności w European Union"
]

ODPOWIEDŹ:
[
    [],
    [],
    ["bilateral meetings"],
    ["European Union"]
]

Lista wypowiedzi zostanie przesłana w następnej wiadomości."""

    def __call__(self, transcription: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        sentences = get_sentences(transcription)
        text = json.dumps(sentences, indent=4, ensure_ascii=False)
        messages = [self.message, text]
        response = self.prompter(
            content=self.content,
            messages=messages
        )

        if response is not None:
            sentences = get_sentences_with_words(transcription)
            return self._process_response(response, sentences)

    @staticmethod
    def _process_response(response: List[str], sentences: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        mixed_language_fragments = []
        for sentence_id, fragments in enumerate(response):
            for fragment in fragments:
                response_sentence = tokenize(fragment)
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
