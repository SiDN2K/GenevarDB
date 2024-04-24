import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Set page title and other configurations
st.set_page_config(page_title="GenevarDB - Type 2 Diabetes Genetic Variants Database")

# Home Page
def home():
    st.markdown("# GenevarDB")
    st.markdown("A comprehensive database of genetic variants of Type 2 Diabetes mellitus.")
    st.markdown("This database features Single Nucleotide Polymorphisms of a collection of genes that are associated with the occurrence of Type 2 Diabetes.")

# Detailed Gene Page
def display_gene_details(gene_name):
    st.write(f"## Gene: {gene_name}")

    # Display coding synonymous variants
    st.write('### Coding and Synonymous Variants')
    filtered_synonymous = coding_synonymous_variants[coding_synonymous_variants['gene'] == gene_name]
    st.write(filtered_synonymous)

    # Display coding missense variants
    st.write('### Coding and Missense Variants')
    filtered_missense = coding_missense_variants[coding_missense_variants['gene'] == gene_name]
    st.write(filtered_missense)

    # Display gene-specific network
    G = nx.Graph()
    with open(network_file_path, 'r') as network_file:
        for line in network_file:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                node1, interaction, node2 = parts[:3]
                G.add_edge(node1, node2, label=interaction)

    # Filter the graph to show only interactions related to the gene
    gene_edges = [edge for edge in G.edges(data=True) if gene_name in edge[:2]]
    gene_graph = nx.Graph(gene_edges)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(gene_graph, k=1)
    nx.draw(gene_graph, pos, with_labels=True, font_size=10, node_color='lightblue', edge_color='gray', ax=ax)
    edge_labels = nx.get_edge_attributes(gene_graph, 'label')
    nx.draw_networkx_edge_labels(gene_graph, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    ax.set_title(f'Gene-specific Network for {gene_name}')
    st.pyplot(fig)

# Sidebar navigation
nav_selection = st.sidebar.radio("Navigation", ["Home", "Gene Details", "Contact Us"])

if nav_selection == "Home":
    home()

elif nav_selection == "Gene Details":
    st.sidebar.markdown("### Select Gene")
    gene_name = st.sidebar.selectbox("Gene", mutation_expression['gene'].unique())
    display_gene_details(gene_name)

else:  # Contact Us
    st.markdown("## Contact Us")
    st.write("Author: Siddharth Singh")
    st.write("Mail: siddharth1r2@gmail.com")
    st.write("LinkedIn: [Siddharth Singh](https://www.linkedin.com/in/siddharth-singh-ab80951a0/)")
