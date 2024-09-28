import os
from pathlib import Path
from typing import Dict, Any


class Transcriber:
    def __init__(self, backend: str = "whisper_timestamped", model: str = "medium", language: str = "pl"):
        self.backend = backend
        self.language = language
        if self.backend == "whisper":
            import whisper
            self.model = whisper.load_model(model)
        elif self.backend == "whisper_timestamped":
            import whisper_timestamped as whisper
            self.model = whisper.load_model(model, device="cpu")
        elif self.backend == "openai":
            from openai import OpenAI
            self.client = OpenAI()

        self.temp_directory = Path("/tmp/video_transcription/")
        self.temp_directory.mkdir(parents=True, exist_ok=True)

    def __call__(self, filepath: os.PathLike) -> Dict[str, Any]:
        if self.backend == "whisper":
            response = self.model.transcribe(str(filepath))
        elif self.backend == "whisper_timestamped":
            import whisper_timestamped as whisper
            audio = whisper.load_audio(str(filepath))
            return whisper.transcribe(self.model, audio, language=self.language)
        elif self.backend == "openai":
            with open(filepath, 'rb') as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

        else:
            raise ValueError("Invalid backend type: supported are: 'local' and 'openai'")

        return response
