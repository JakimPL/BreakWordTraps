import os
from pathlib import Path

import moviepy.editor as mp

TEMP_DIR = "/tmp/video_transcription/"


class VideoToAudioConverter:
    def __init__(self, temp_directory: os.PathLike = TEMP_DIR):
        self.temp_directory = Path(temp_directory)
        self.temp_directory.mkdir(parents=True, exist_ok=True)

    def __call__(self, filepath: os.PathLike) -> Path:
        input_path = Path(filepath)
        output_path = Path(self.temp_directory) / input_path.with_suffix(".wav").name

        if not output_path.exists():
            video = mp.VideoFileClip(str(filepath))
            video.audio.write_audiofile(output_path)

        return output_path
