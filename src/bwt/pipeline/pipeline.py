import concurrent.futures
import os
from typing import Dict, Any

from tqdm import tqdm

from bwt.analyzer.text.combined import CombinedAnalyzer
from bwt.analyzer.text.fast_speaking import FastSpeakingAnalyzer
from bwt.analyzer.text.gunning_fog import GunningFogIndex
from bwt.analyzer.text.long_sentences import LongSentencesAnalyzer
from bwt.analyzer.text.long_words import LongWordsAnalyzer
from bwt.analyzer.text.numerals import NumeralsAnalyzer
from bwt.analyzer.text.pauses import PausesAnalyzer
from bwt.analyzer.text.sentiment import SentimentAnalyzer
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
            GunningFogIndex(),
            LongSentencesAnalyzer(),
            LongWordsAnalyzer(),
            NumeralsAnalyzer(),
            PausesAnalyzer(),
            SentimentAnalyzer()
        ]

    def __call__(self, input_path: os.PathLike) -> Dict[str, Any]:
        self.logger.info("Converting video to audio...")
        audio_path = self.video_to_audio_converter(input_path)
        self.logger.info("Transcribing audio to text...")
        transcription = self.transcriber(audio_path)

        output = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(analyzer, transcription): analyzer for analyzer in self.text_analyzers}
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Text analysis"):
                result = future.result()
                output.update(result)

        return output
