# VideoAnalyzer

Narzędzie do analizy błędów językowych do prezentacji składa się z dwóch komponentów:
* backendu `backend` napisanego w języku Python z wykorzystaniem frameworka _FastAPI_,
* frontendu `interface` wykorzystującego bibliotekę _streamlit_.

## Uruchomienie

Aplikacja pozwala na analizę błędów językowych w tekście. W tym celu należy wkleić tekst do pola tekstowego, a następnie nacisnąć przycisk `Przetwórz wideo`. Po chwili aplikacja zwróci wyniki podstawowe informacje oraz wskaże błędy w materiale.

Szczegółowe i kompletne, aczkolwiek bardzo techniczne, dane w postaci słownika JSON zamieszczone są pod przetworzonym wideo. 

**Uwaga!** Przetwarzanie jednominutowego filmu trwa około 2-3 minuty.

## Komponenty

Aplikacja składa się z modułów analizujących poszczególne aspekty językowe. W chwili obecnej dostępne są:

* `fast_speaking` - wskazuje fragmenty, w których mówca mówi zbyt szybko
* `foreign_words` - wskazuje zapożyczenia, anglicyzmy oraz inne obcojęzyczne słowa
* `jargon` - odnajduje specjalistyczne słownictwo, język fachowy
* `long_sentences` - wyróżnia zdania zbyt długie (ponad 15 słów)
* `long_words` - wskazuje zdania, w których występują słowa zbyt długie
* `passive_voice` - znajduje zdania wyrażone w stronie biernej
* `pauses` - znajduje pauzy i zastoje
* `repetitions` - znajduje powtórzenia słów, wyrażeń w tekście

Ponadto aplikacja wyznacza i interpretuje wskaźnik mglistości Gunninga (`gunning_fog`). 