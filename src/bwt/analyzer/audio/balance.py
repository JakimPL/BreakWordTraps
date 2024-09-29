from typing import Any, Dict
import os

from bwt.analyzer.audio.audio_analyzer import AudioAnalyzer


class BalanceAnalyzer(AudioAnalyzer):
    def __call__(self, audio_path: os.PathLike) -> Dict[str, Any]:
        pass
