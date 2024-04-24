import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Set page title and other configurations
st.set_page_config(page_title="GenevarDB - Type 2 Diabetes Genetic Variants Database")

# Load the data files with updated file paths
coding_synonymous_variants = pd.read_csv('data/Genvariantsyn.csv')
coding_missense_variants = pd.read_csv('data/Genvariantmis.csv')
mutation_expression = pd.read_excel('data/try_version_1.xlsb.xlsx')
network_file_path = 'data/T2DM_Network.sif'

# Sidebar navigation
nav_selection = st.sidebar.radio("Navigation", ["Home", "Search", "Browse", "Contact Us"])

if nav_selection == "Home":
    st.markdown("# GenevarDB")
    st.markdown("A comprehensive database of genetic variants of Type 2 Diabetes mellitus.")
    st.markdown("This database features Single Nucleotide Polymorphisms of a collection of genes that are associated with the occurrence of Type 2 Diabetes.")

elif nav_selection == "Search":
    st.header("Search")
    search_type = st.selectbox("Search by", ["Gene", "Expression", "Expression 2"])

    search_query = st.text_input("Enter search query")
    if search_query:
        if search_type == "Gene":
            result = mutation_expression[mutation_expression['gene'].str.contains(search_query, case=False)]
        elif search_type == "Expression":
            result = mutation_expression[mutation_expression['expression'].str.contains(search_query, case=False)]
        elif search_type == "Expression 2":
            result = mutation_expression[mutation_expression['expression 2'].str.contains(search_query, case=False)]
        
        if not result.empty:
            st.write("Search Results:")
            st.write(result)
        else:
            st.write("No results found.")

elif nav_selection == "Browse":
    st.header("Browse")
    genes_list = mutation_expression['gene'].unique()
    gene_selected = st.selectbox("Select Gene", genes_list)
    
    # Display gene details for the selected gene
    st.write(f"## Gene: {gene_selected}")

    # Display coding synonymous variants
    st.write('### Coding and Synonymous Variants')
    filtered_synonymous = coding_synonymous_variants[coding_synonymous_variants['gene'] == gene_selected]
    st.write(filtered_synonymous)

    # Display coding missense variants
    st.write('### Coding and Missense Variants')
    filtered_missense = coding_missense_variants[coding_missense_variants['gene'] == gene_selected]
    st.write(filtered_missense)

    # Display expressions from mutation_expression connected with the gene
    st.write('### Mutation Expression')
    filtered_mutation_expression = mutation_expression[mutation_expression['gene'] == gene_selected]
    st.write(filtered_mutation_expression[['gene', 'expression', 'expression 2']])

    # Load and display the network from .sif file as a graph
    st.write('### Gene-specific Network (Graph)')
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
    if gene_selected in G.nodes():
        subgraph_nodes = [gene_selected]  # Nodes around the filtered gene
        subgraph = G.subgraph(subgraph_nodes)  # Create subgraph around the filtered gene
        pos_subgraph = nx.spring_layout(subgraph, k=2)  # Adjust k for spacing in the subgraph
        # Draw nodes and edges of the subgraph with different colors
        nx.draw(subgraph, pos_subgraph, with_labels=True, font_size=10, node_color='green', edge_color='black', ax=ax)
        ax.set_title(f'Zoomed In on {gene_selected}')

    # Display the plot using st.pyplot(fig)
    st.pyplot(fig)

else:  # Contact Us
    st.header("Contact Us")
    st.write("Author: Siddharth Singh")
    st.write("Mail: siddharth1r2@gmail.com")
    st.write("LinkedIn: [Siddharth Singh](https://www.linkedin.com/in/siddharth-singh-ab80951a0/)")
