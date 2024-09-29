import concurrent.futures
import json
import os
from pathlib import Path
from typing import Dict, Any, List

from tqdm import tqdm

from bwt.analyzer.text.combined import CombinedAnalyzer
from bwt.analyzer.text.fast_speaking import FastSpeakingAnalyzer
from bwt.analyzer.text.gunning_fog import GunningFogIndex
from bwt.analyzer.text.long_sentences import LongSentencesAnalyzer
from bwt.analyzer.text.long_words import LongWordsAnalyzer
from bwt.analyzer.text.numerals import NumeralsAnalyzer
from bwt.analyzer.text.pauses import PausesAnalyzer
from bwt.analyzer.text.sentiment import SentimentAnalyzer
from bwt.analyzer.text.text_analyzer import TextAnalyzer
from bwt.converter.video_to_audio import VideoToAudioConverter
from bwt.logger import get_logger
from bwt.sha import compute_sha256, save_dict_to_json_file
from bwt.transcription.transcription import Transcriber


class Pipeline:
    def __init__(self):
        self.logger = get_logger("Pipeline")
        self.video_to_audio_converter = VideoToAudioConverter()
        self.transcriber = Transcriber()
        self.text_analyzers: List[TextAnalyzer] = [
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
        file_hash = compute_sha256(input_path)[:16]
        json_filename = f"{file_hash}.json"
        json_path = Path("/tmp/video_transcription/") / json_filename

        if json_path.exists():
            self.logger.info("Loading cached results...")
            with open(json_path, "r") as json_file:
                return json.load(json_file)

        self.logger.info("Converting video to audio...")
        audio_path = self.video_to_audio_converter(input_path)
        self.logger.info("Transcribing audio to text...")
        transcription = self.transcriber(audio_path)

        output = self._analyze(transcription)
        final = {
            "transcription": transcription,
            "analysis": output
        }

        self.logger.info(f"Saving cached results to {json_path}...")
        save_dict_to_json_file(final, json_path)
        return final

    def _analyze(self, transcription: Dict[str, Any]) -> Dict[str, Any]:
        output = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(analyzer, transcription): analyzer for analyzer in self.text_analyzers}
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Text analysis"):
                result = future.result()
                output.update(result)

        return output
