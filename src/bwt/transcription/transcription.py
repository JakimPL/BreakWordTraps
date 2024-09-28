import os
from pathlib import Path
from typing import Dict, Any

import moviepy.editor as mp


class Transcriber:
    def __init__(self, backend: str = "whisper_timestamped", model: str = "medium", language: str = "pl"):
        self.backend = backend
        self.language = language
        if self.backend == "whisper":
            import whisper
            self.model = whisper.load_model(model)
        elif self.backend == "whisper_timestamped":
            import whisper_timestamped as whisper
            self.model = whisper.load_model("tiny", device="cpu")
        elif self.backend == "openai":
            from openai import OpenAI
            self.client = OpenAI()

        self.temp_directory = Path("/tmp/video_transcription/")
        self.temp_directory.mkdir(parents=True, exist_ok=True)

    def _convert_video_to_audio(self, filepath: os.PathLike) -> os.PathLike:
        input_path = Path(filepath)
        output_path = Path(self.temp_directory) / input_path.with_suffix(".wav").name

        if not output_path.exists():
            video = mp.VideoFileClip(str(filepath))
            video.audio.write_audiofile(output_path)

        return output_path

    def __call__(self, filepath: os.PathLike) -> Dict[str, Any]:
        audio_path = self._convert_video_to_audio(filepath)

        if self.backend == "whisper":
            response = self.model.transcribe(str(audio_path))
        elif self.backend == "whisper_timestamped":
            import whisper_timestamped as whisper
            audio = whisper.load_audio(str(audio_path))
            return whisper.transcribe(self.model, audio, language=self.language)
        elif self.backend == "openai":
            with open(audio_path, 'rb') as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

        else:
            raise ValueError("Invalid backend type: supported are: 'local' and 'openai'")

        return response
