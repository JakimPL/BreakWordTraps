from typing import Any, Dict

from bwt.transcription.utility import Words


class Analyzer:
    name: str

    def __call__(self, transcription: Dict[str, Any]) -> Dict[str, Words]:
        raise NotImplementedError("Analyzer must implement __call__ method")
