import pickle
from sklearn.decomposition import NMF
import argparse

def perform_nmf(tfidf_matrix_file, n_topics, output_nmf_file):
    # Step 1: Load the TF-IDF matrix
    with open(tfidf_matrix_file, 'rb') as f:
        tfidf_matrix = pickle.load(f)
    
    # Step 2: Apply NMF for dimensionality reduction
    print(f"Applying NMF with {n_topics} topics...")
    nmf_model = NMF(n_components=n_topics, random_state=42)
    W = nmf_model.fit_transform(tfidf_matrix)  # Document-topic matrix
    H = nmf_model.components_                  # Topic-term matrix
    
    # Step 3: Save the NMF model and matrices
    with open(output_nmf_file, 'wb') as f:
        pickle.dump({'nmf_model': nmf_model, 'W': W, 'H': H}, f)
    print(f"NMF model and matrices saved to {output_nmf_file}")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform NMF dimensionality reduction on TF-IDF matrix.')
    parser.add_argument('--tfidf_matrix_file', type=str, required=True, help='Path to the TF-IDF matrix file (output from your TF-IDF script).')
    parser.add_argument('--n_topics', type=int, default=10, help='Number of topics for NMF (default: 10).')
    parser.add_argument('--output_nmf_file', type=str, default='nmf_model.pkl', help='Filename to save the NMF model and matrices (default: nmf_model.pkl).')
    args = parser.parse_args()
    
    perform_nmf(args.tfidf_matrix_file, args.n_topics, args.output_nmf_file)