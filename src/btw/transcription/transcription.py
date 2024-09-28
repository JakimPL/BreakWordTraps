import os
from pathlib import Path
from typing import Dict, Any
import moviepy.editor as mp
import whisper


class Transcriber:
    def __init__(self, model: str = "base"):
        self.model = whisper.load_model(model)
        self.temp_directory = Path("/tmp/video_transcription/")

    def _convert_video_to_audio(self, filepath: os.PathLike) -> os.PathLike:
        input_path = Path(filepath)
        output_path = Path(self.temp_directory) / input_path.with_suffix(".wav").name

        if not output_path.exists():
            video = mp.VideoFileClip(str(filepath))
            video.audio.write_audiofile(output_path)

        return output_path

    def __call__(self, filepath: os.PathLike) -> Dict[str, Any]:
        audio_path = self._convert_video_to_audio(filepath)
        return self.model.transcribe(audio_path)
