import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt
import argparse

def build_similarity_network(perfume_mapping_file, nmf_file, threshold):
    # Step 1: Load the perfume mapping
    perfume_mapping = pd.read_csv(perfume_mapping_file)
    
    # Ensure the necessary columns are present
    if not {'index', 'brand', 'perfume_name'}.issubset(perfume_mapping.columns):
        raise ValueError("Perfume mapping CSV must contain 'index', 'brand', and 'perfume_name' columns.")
    
    # Create a unique identifier for each perfume
    perfume_mapping['unique_label'] = perfume_mapping['brand'] + ' - ' + perfume_mapping['perfume_name']
    
    # Step 2: Load the NMF model and matrices
    with open(nmf_file, 'rb') as f:
        nmf_data = pickle.load(f)
    W = nmf_data['W']  # Document-topic matrix
    
    # Step 3: Compute pairwise cosine similarity
    print("Computing pairwise cosine similarity...")
    similarity_matrix = cosine_similarity(W)

    sim_scores = similarity_matrix[np.triu_indices(similarity_matrix.shape[0], k=1)]

    plt.hist(sim_scores, bins=50)
    plt.xlabel('Similarity Score')
    plt.ylabel('Frequency')
    plt.title('Distribution of Similarity Scores')
    plt.show()
    
    # Step 4: Build the similarity network
    print("Building the similarity network...")
    N = 5  # Number of top edges to keep per node

    G = nx.Graph()
    # Add nodes with attributes
    for idx, row in perfume_mapping.iterrows():
        G.add_node(idx, perfume_name=row['unique_label'], brand=row['brand'])

    # Add top N edges per node
    num_perfumes = similarity_matrix.shape[0]
    for i in range(num_perfumes):
        similarities = similarity_matrix[i]
        # Get indices of the top N similar perfumes, excluding itself
        top_indices = similarities.argsort()[-(N+1):-1]  # Exclude the last one (itself)
        for j in top_indices:
            if i != j and similarities[j] >= threshold:
                G.add_edge(i, j, weight=similarities[j])
    
    nx.write_gexf(G, 'data/perfume_similarity_network.gexf')
    print('Graph exported to data/perfume_similarity_network.gexf')

    print("Similarity Matrix Sample:")
    print(similarity_matrix[:5, :5])  # Print a small sample

    # Step 5: Visualize the network
    print("Visualizing the network...")
    plt.figure(figsize=(15, 15))
    
    # Positions for all nodes using a force-directed layout
    pos = nx.spring_layout(G, k=0.5, iterations=50, weight='weight')
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='skyblue', alpha=0.8)
    
    # Draw edges with widths proportional to similarity
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[weight * 2 for weight in edge_weights], alpha=0.5)
    
    # Draw labels
    labels = nx.get_node_attributes(G, 'perfume_name')
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    
    plt.title(f'Perfume Similarity Network (Threshold = {threshold})')
    plt.axis('off')
    plt.show()
    
    print("Network visualization completed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build and visualize a perfume similarity network based on NMF results.')
    parser.add_argument('--perfume_mapping_file', type=str, required=True, help='Path to the perfume mapping CSV file.')
    parser.add_argument('--nmf_file', type=str, required=True, help='Path to the NMF model and matrices file (output from the NMF script).')
    parser.add_argument('--threshold', type=float, default=0.5, help='Similarity threshold for connecting perfumes (default: 0.5).')
    args = parser.parse_args()
    
    build_similarity_network(args.perfume_mapping_file, args.nmf_file, args.threshold)