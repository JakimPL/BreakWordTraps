from typing import Any, Dict


class TextAnalyzer:
    name: str

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Analyzer must implement __call__ method")
