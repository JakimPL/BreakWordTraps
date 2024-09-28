import json
from typing import Any, Dict

from bwt.prompter.prompter import Prompter
from bwt.transcription.utility import get_segments


class MixedLanguagesAnalyzer:
    def __init__(self):
        self.prompter = Prompter()
        self.content = "Jesteś językoznawcą z 20-letnim doświadczeniem w badaniu języka polskiego w kontekście występów publicznych. Zwracasz baczną uwagę na szczegóły związane z jasnością przekazu i korzystając z doświadczenia, wiedzy i wyczucia potrafisz doskonale ocenić jakość czyjegoś wystąpienia."
        self.message = """
ZADANIE:
Zadanie polega na wskazaniu w liście składających się z paru wypowiedzi anglicyzmów oraz zapożyczeń z języka angielskiego. Poszczególne wypowiedzi są wyróżnione cudzysłowem. Wynik należy podać jako listę
Nie podawaj imion i nazwisk.

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

    def __call__(self, transcription: Dict[str, Any]) -> int:
        segments = get_segments(transcription)
        text = json.dumps(segments, indent=4, ensure_ascii=False)
        messages = [self.message, text]
        result = self.prompter(
            content=self.content,
            messages=messages
        )

        return json.loads(result.choices[0].message.content)
