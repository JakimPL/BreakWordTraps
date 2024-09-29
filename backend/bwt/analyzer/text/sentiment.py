import json
from typing import Any, Dict, Optional

from bwt.analyzer.text.text_analyzer import TextAnalyzer
from bwt.logger import get_logger
from bwt.prompter.prompter import Prompter
from bwt.tokenizer.tokenizer import Tokenizer
from bwt.transcription.utility import Words
from bwt.transcription.utility import get_sentences


class SentimentAnalyzer(TextAnalyzer):
    name: str = "sentiment"

    def __init__(self):
        self.logger = get_logger("SentimentAnalyzer")
        self.tokenizer = Tokenizer()
        self.prompter = Prompter()
        self.content = """Jesteś językoznawcą z 20-letnim doświadczeniem w badaniu języka polskiego. Zwracasz baczną uwagę na szczegóły znaczeniowe i korzystając z doświadczenia, kontekst i wyczucie potrafisz doskonale ocenić wydźwięk wypowiedzi. 

Jako input dostaniesz TEKST"""
        self.message = """ZADANIE składa się z 4 części: 

    1. Oceń WYDŹWIĘK poniższego TEKSTU. Określ wydźwięk dla całej wypowiedzi. Weź pod uwagę tematy, użyte słownictwo i ogólny kontekst. Użyj do tego skali od -1 do 1, gdzie: -1 to skrajnie negatywny wydźwięk, 0 to neutralny wydźwięk,
    1 to skrajnie pozytywny wydźwięk. Analizuj uważnie i nie dawaj punktów za sentyment pochopnie! Bądź wyczulony na niuanse!  Pamiętaj, że wiele wypowiedzi może być neutralnych. 
    2. Oceń  INTENCJE  Wyjaśnij szczegółowo, obszernie i jasno intencje autora poniższego TEKSTU. 
    3. Oceń ZROZUMIAŁÓŚĆ przekazu w TEKŚCIE. Weź pod uwagę, że mają być to treści zrozumiałe dla potencjalnego odbiorcy. Weź pod uwagę klarowność struktury wywodu, koherencje treści. Przeanalizuj wykorzystane zabiegi retoryczne i błędy. 
    4. Zestaw ZROZUMIAŁOŚĆ z INTENCJAMI autora w tekście i oceń ogólną jakość przekazu.

Wynik podaj w postaci słownika JSON bez żadnej dodatkowej treści.
{
    "sentiment": wartość,
    "sentiment_explanation": wyjaśnienie decyzji,    
    "intentions": wyjaśnienie intencji,
    "understandability": ocena zrozumiałości,    
    "intentions_vs_understandability": ocena zrozumiałości w stosunku do intencji
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
        return response
