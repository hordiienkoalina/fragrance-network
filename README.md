## Install

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Download
```
python3 scripts/tt_download.py /path/to/urls.txt /path/to/output_folder
```

## 1. Transcribe
```
python3 scripts/tt_transcribe.py /path/to/mp4_folder /path/to/json_output_folder /path/to/mp3_output_folder
```

## 2. OCR
```
python3 scripts/tt_OCR.py /path/to/mp4_folder /path/to/output_folder
```

## 3. Combine Transcriptions + OCR
```
python3 scripts/tt_combine.py /path/to/transcriptions_folder /path/to/ocr_folder /path/to/output_folder
```

## 4. ChatGPT NER
```
python3 tt_chatgpt_NER.py /path/to/combined_folder /path/to/output_folder
```