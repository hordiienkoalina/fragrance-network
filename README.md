## Install

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Batch Transcribe + OCR
```
python3 scripts/tt_transcribe.py /path/to/video_folder
python3 scripts/tt_OCR.py /path/to/video_folder /path/to/output_folder
python3 scripts/tt_combine.py /path/to/transcriptions_folder /path/to/ocr_folder /path/to/output_folder
```