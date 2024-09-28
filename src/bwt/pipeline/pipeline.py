import os
from typing import Dict, Any

from tqdm import tqdm

from bwt.analyzer.text.combined import CombinedAnalyzer
from bwt.analyzer.text.fast_speaking import FastSpeakingAnalyzer
from bwt.analyzer.text.long_sentences import LongSentencesAnalyzer
from bwt.analyzer.text.numerals import NumeralsAnalyzer
from bwt.analyzer.text.pauses import PausesAnalyzer
from bwt.converter.video_to_audio import VideoToAudioConverter
from bwt.logger import get_logger
from bwt.transcription.transcription import Transcriber


class Pipeline:
    def __init__(self):
        self.logger = get_logger("Pipeline")
        self.video_to_audio_converter = VideoToAudioConverter()
        self.transcriber = Transcriber()
        self.text_analyzers = [
            CombinedAnalyzer(),
            FastSpeakingAnalyzer(),
            LongSentencesAnalyzer(),
            NumeralsAnalyzer(),
            PausesAnalyzer(),
        ]

    def __call__(self, input_path: os.PathLike) -> Dict[str, Any]:
        self.logger.info("Converting video to audio...")
        audio_path = self.video_to_audio_converter(input_path)
        self.logger.info("Transcribing audio to text...")
        transcription = self.transcriber(audio_path)

        output = {}
        for analyzer in tqdm(self.text_analyzers, desc="Text analysis"):
            output.update(analyzer(transcription))

        return output
