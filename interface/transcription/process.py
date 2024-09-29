from typing import Any, Dict


def fill_transcription(result: Dict[str, Any], transcription_box: Any) -> None:
    transcription = result.get("transcription", {}).get("text", "").strip()
    transcription_box.text_area("Transcription", value=transcription, height=200, disabled=True)
