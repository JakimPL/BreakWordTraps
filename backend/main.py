from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from bwt.pipeline.pipeline import Pipeline

app = FastAPI()


@app.post("/process_video/")
async def process_video(file: UploadFile = File(...)):
    tmp_dir = Path("/tmp/video_transcription/")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    file_path = tmp_dir / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    pipeline = Pipeline()
    output = pipeline(file_path)

    return output
