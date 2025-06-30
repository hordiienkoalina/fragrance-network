import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse
import pickle

def compute_tfidf(input_csv, output_tfidf, output_mapping):
    # Step 1: Load the data
    df = pd.read_csv(input_csv)
    
    # Ensure that the DataFrame has the expected columns
    if not {'brand', 'perfume_name', 'descriptors'}.issubset(df.columns):
        raise ValueError("Input CSV file must contain 'brand', 'perfume_name', and 'descriptors' columns.")
    
    # Step 2: Handle missing values
    # Convert 'descriptors' to string type
    df['descriptors'] = df['descriptors'].astype(str)
    
    # Replace 'nan' strings with actual NaN
    df['descriptors'] = df['descriptors'].replace('nan', pd.NA)
    
    # Check for missing values in 'descriptors'
    missing_count = df['descriptors'].isnull().sum()
    print(f"Number of missing descriptors: {missing_count}")
    
    if missing_count > 0:
        # Remove rows with missing descriptors
        df = df.dropna(subset=['descriptors'])
        print(f"Removed {missing_count} rows with missing descriptors.")
        # Reset the index
        df = df.reset_index(drop=True)
    
    # Remove rows with empty descriptors
    empty_count = (df['descriptors'].str.strip() == '').sum()
    if empty_count > 0:
        df = df[df['descriptors'].str.strip() != '']
        df = df.reset_index(drop=True)
        print(f"Removed {empty_count} rows with empty descriptors.")
    
    # Step 3: Combine descriptors for each unique perfume
    df = df.groupby(['brand', 'perfume_name'], as_index=False).agg({'descriptors': ' '.join})
    # Reset index after grouping
    df = df.reset_index(drop=True)
    print(f"Combined descriptors for {len(df)} unique perfumes.")
    
    # Step 4: Extract descriptors
    descriptors = df['descriptors'].tolist()
    
    # Step 5: Compute TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptors)
    
    # Step 6: Save the TF-IDF matrix and mapping
    # Save the TF-IDF matrix using pickle
    with open(output_tfidf, 'wb') as f:
        pickle.dump(tfidf_matrix, f)
    
    # Save the vectorizer for future use
    with open('data/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    # Save the mapping of perfumes to their indices
    perfume_mapping = df[['brand', 'perfume_name']].reset_index()
    perfume_mapping.to_csv(output_mapping, index=False)
    
    print(f"TF-IDF matrix saved to {output_tfidf}")
    print(f"Vectorizer saved to data/tfidf_vectorizer.pkl")
    print(f"Perfume mapping saved to {output_mapping}")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute TF-IDF vectors for perfume descriptors.')
    parser.add_argument('--input_csv', type=str, required=True, help='Path to the input CSV file containing preprocessed data.')
    parser.add_argument('--output_tfidf', type=str, default='tfidf_matrix.pkl', help='Path to save the TF-IDF matrix (default: tfidf_matrix.pkl)')
    parser.add_argument('--output_mapping', type=str, default='perfume_mapping.csv', help='Path to save the perfume mapping CSV file (default: perfume_mapping.csv)')
    args = parser.parse_args()
    
    compute_tfidf(args.input_csv, args.output_tfidf, args.output_mapping)
