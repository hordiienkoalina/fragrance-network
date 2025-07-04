# Description

This project explores how to create a network of similar perfumes by processing TikTok videos from fragrance creators. Using a custom pipeline that includes audio transcription, OCR, named entity recognition via ChatGPT, TF-IDF embeddings, and Non-Negative Matrix Factorization (NMF), the project maps perfumes based on shared descriptors and computes pairwise cosine similarity. The goal is to provide a more intuitive, data-driven way to explore fragrance relationships beyond traditional note pyramids.

# Install

## 0. Setup
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 1. Download TikToks
```
python3 scripts/tt_download.py /path/to/urls.txt /path/to/output_folder
```

## 2. Transcribe
```
python3 scripts/tt_transcribe.py /path/to/mp4_folder /path/to/json_output_folder /path/to/mp3_output_folder
```

## 3. OCR
```
python3 scripts/tt_OCR.py /path/to/mp4_folder /path/to/output_folder
```

## 4. Combine Transcriptions + OCR
```
python3 scripts/tt_combine.py /path/to/transcriptions_folder /path/to/ocr_folder /path/to/output_folder
```

## 5. ChatGPT NER
```
python3 tt_chatgpt_NER.py /path/to/combined_folder /path/to/output_folder
```
## 6. Data Preprocessing
```
python3 scripts/tt_data_preprocess.py /path/to/folder1_NER /path/to/folder2_NER /path/to/folder3_NER --output_file data/preprocessed_descriptors.csv
```
## 7. Generate Embeddings
```
python3 scripts/tt_tfidf.py --input_csv data/preprocessed_descriptors.csv --output_tfidf data/tfidf_matrix.pkl --output_mapping data/perfume_mapping_clean.csv
```
## 8. Dimensionality Reduction using Non-Negative Matrix Factorisation
```
python3 scripts/tt_nmf_dim_reduction.py --tfidf_matrix_file data/tfidf_matrix.pkl --n_topics 10 --output_nmf_file data/nmf_model.pkl
```

## 9. Build and Visualise the Similarity Network
```
python3 scripts/tt_similarity_network.py --perfume_mapping_file data/perfume_mapping_clean.csv --nmf_file data/nmf_model.pkl --threshold 0.5
```
