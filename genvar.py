import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Set page title and other configurations
st.set_page_config(page_title="Database for Type 2 Diabetes Genetic Variants")

# Load the data files with updated file paths
coding_synonymous_variants = pd.read_csv('data/Genvariantsyn.csv')
coding_missense_variants = pd.read_csv('data/Genvariantmis.csv')
mutation_expression = pd.read_excel('data/try_version_1.xlsb.xlsx')

# Sidebar for user input
st.sidebar.title('Filter Options')
gene_filter = st.sidebar.selectbox('Select Gene', mutation_expression['gene'].unique())

# Filter data based on user input
filtered_coding_synonymous = coding_synonymous_variants[coding_synonymous_variants['gene'] == gene_filter]
filtered_coding_missense = coding_missense_variants[coding_missense_variants['gene'] == gene_filter]
filtered_mutation_expression = mutation_expression[mutation_expression['gene'] == gene_filter]

# Display filtered data and expressions
st.write('## Database for Type 2 Diabetes Genetic Variants')
st.write(f'Filtered Gene: {gene_filter}')

# Display filtered data from coding_synonymous_variants
st.write('### Coding and Synonymous Variants')
st.write(filtered_coding_synonymous)

# Display filtered data from coding_missense_variants
st.write('### Coding and Missense Variants')
st.write(filtered_coding_missense)

# Display expressions from mutation_expression connected with the filtered gene
st.write('### Mutation Expression')
st.write(filtered_mutation_expression[['gene', 'expression', 'expression 2']])

# Load and display the network from .sif file as a graph
st.write('## Entire Network (Graph)')
network_file_path = 'C:\\Users\\siddh\\Downloads\\T2DM_Network.sif'

# Create an empty graph
G = nx.Graph()

# Read edges from .sif file and add them to the graph
with open(network_file_path, 'r') as network_file:
    for line in network_file:
        parts = line.strip().split('\t')
        if len(parts) >= 3:  # Check if there are at least 3 parts in the line
            node1, interaction, node2 = parts[:3]
            G.add_edge(node1, node2, label=interaction)  # Add edge with interaction as label

# Create a figure and plot the network visualization
fig, ax = plt.subplots(figsize=(15, 12))  # Larger figsize for bigger graph
pos = nx.spring_layout(G, k=0.5)  # Increase k for more spacing between nodes

# Draw the entire graph with gray edges
nx.draw(G, pos, with_labels=True, font_size=10, node_color='lightblue', edge_color='gray', ax=ax)

# Draw gray lines for edges between nodes with their interactions as labels
for edge in G.edges(data=True):
    pos_edge = (pos[edge[0]], pos[edge[1]])
    ax.annotate('', xy=pos_edge[1], xytext=pos_edge[0], arrowprops=dict(arrowstyle='-', color='gray'))

ax.set_title('Entire Network (Graph)')

# Highlight the filtered gene by zooming in on it
if gene_filter in G.nodes():
    subgraph_nodes = [gene_filter]  # Nodes around the filtered gene
    subgraph = G.subgraph(subgraph_nodes)  # Create subgraph around the filtered gene
    pos_subgraph = nx.spring_layout(subgraph, k=2)  # Adjust k for spacing in the subgraph
    # Draw nodes and edges of the subgraph with different colors
    nx.draw(subgraph, pos_subgraph, with_labels=True, font_size=10, node_color='green', edge_color='black', ax=ax)
    ax.set_title(f'Zoomed In on {gene_filter}')

# Display the plot using st.pyplot(fig)
st.pyplot(fig)
