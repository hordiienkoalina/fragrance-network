import json
import re
import os
import pandas as pd
import argparse
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import download

# Download NLTK resources if not already downloaded
download('stopwords')
download('wordnet')
download('omw-1.4')

nltk_stop_words = set(stopwords.words('english'))

# Custom stop words specific to perfume descriptions
custom_stop_words = {
    "smells", "like", "than", "fragrance", "not", "well", "very", "really", "similar",
    "no", "a", "perfect", "makes", "me", "so", "much", "of", "at", "and", "smelled",
    "yet", "full", "size", "my", "good", "great", "best", "bad", "amazing", "love",
    "favorite", "smell", "perfume", "scent", "nice", "also", "one", "still", "get",
    "better", "got", "new", "go", "want", "would", "definitely", "never", "first",
    "bought", "buy", "could", "thought", "ever", "day", "last", "even", "tried",
    "think", "time", "come", "try", "know", "just", "now", "since", "find", "say",
    "thing", "way", "feel", "everything", "absolutely", "maybe", "though", "nothing",
    "see", "make", "every", "always", "around", "another", "probably", "give",
    "people", "recommend", "goes", "ever", "take", "see", "many", "used", "using",
    "went", "smelling", "smelled", "overall", "little", "pretty", "completely",
    "totally", "lot", "almost", "much", "less", "long", "however", "sure", "hard",
    "work", "def", "find", "found", "keep", "put", "let", "without", "cant",
    "anything", "everything", "something", "someone", "thing", "some", "done",
    "felt", "say", "give", "made", "maybe", "might", "mine", "must", "oh", "ok",
    "okay", "use", "used", "using", "yes", "yet", "think", "got", "getting", "try",
    "trying", "look", "looking", "looked", "feeling", "felt", "feel", "keep",
    "keeps", "kept", "getting", "came", "also", "said", "went", "gone", "back",
    "right", "left", "took", "taking", "takes", "want", "wanted", "wants", "note",
    "notes", "pleasant", "beautiful", "composition", "evokes", "trail", "vibe", 
    "base", "enjoyable", "longevity", "shorter", "short", "incredible", "wearable", 
    "highly", "high", "mode", "feel", "year", "eve", "feeling", "reapplying", "hint", 
    "extremely", "top", "middle", "bottom", "layer", "layering", "aroma", "sillage", 
    "cologne", "reminds", "slight", "worthy", "lovely", "suitable", "scented", "scent",
    "element", "dna", "dry", "down", "cut", "london", "shower", "gel", "pound", "stunning",
    "delicious", "affordable", "comforting", "complementary", "compliment", "everyday", 
    "unique", "drydown", "witty", "fog", "together", "aromatic", "super", "opening", "steep",
    "wonderful", "sophisticated", "forward", "sensual", 'supermilk', 'beauty', 'bottle', 'nostalgic', 
    'interesting', 'straightforward', 'weird', 'gray', 'blood', 'cheap','lasting','limited',
    'pleasantly','surprised','getter','compliment','actual','hitting','dup','bb','store','redundant',
    'twist','insanely','brush'
    }

# Combined stop words (NLTK + custom)
all_stop_words = nltk_stop_words.union(custom_stop_words)

def load_and_preprocess(data_folders):
    # Aggregate data from all specified folders
    data = []
    for folder in data_folders:
        for file_name in os.listdir(folder):
            if file_name.endswith('.json'):
                file_path = os.path.join(folder, file_name)
                with open(file_path, 'r') as f:
                    content = json.load(f)
                    data.extend(content['data'])

    # Preprocess descriptors
    def preprocess(text):
        text = text.lower()
        # Remove punctuation, numbers, special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        words = text.split()
        lemmatizer = WordNetLemmatizer()
        # Remove stop words, words of length <= 1, and lemmatize
        filtered_words = [
            lemmatizer.lemmatize(word)
            for word in words
            if word not in all_stop_words and len(word) > 1
        ]
        return ' '.join(filtered_words)

    # Convert to DataFrame and preprocess descriptors
    df = pd.DataFrame(data)
    df['descriptors'] = df['descriptors'].apply(preprocess)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Loading and Preprocessing Script")
    parser.add_argument(
        'data_folders',
        type=str,
        nargs='+',
        help="List of paths to folders containing JSON data files."
    )
    parser.add_argument(
        '--output_file',
        type=str,
        default='processed_descriptors.csv',
        help="Path for the output CSV file (default: processed_descriptors.csv)"
    )

    args = parser.parse_args()

    # Load and preprocess data from multiple folders
    df = load_and_preprocess(args.data_folders)

    # Save processed data to a CSV file
    df.to_csv(args.output_file, index=False)
    print(f"Data preprocessed and saved to {args.output_file}")