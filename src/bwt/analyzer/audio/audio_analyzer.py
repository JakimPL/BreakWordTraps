import os
from typing import Any, Dict


class AudioAnalyzer:
    name: str

    def __call__(self, audio_path: os.PathLike) -> Dict[str, Any]:
        raise NotImplementedError("Analyzer must implement __call__ method")
