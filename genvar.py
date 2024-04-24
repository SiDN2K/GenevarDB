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
    search_type = st.selectbox("Search by", ["Gene", "Expression", "Expression 2", "All"])

    if search_type == "Gene":
        gene_search = st.text_input("Enter gene name")
        result = mutation_expression[mutation_expression['gene'].str.contains(gene_search, case=False)]
        st.write("Search Results:")
        st.write(result)

    elif search_type == "Expression":
        expression_search = st.text_input("Enter expression")
        result = mutation_expression[mutation_expression['expression'].str.contains(expression_search, case=False)]
        st.write("Search Results:")
        st.write(result)

    elif search_type == "Expression 2":
        expression2_search = st.text_input("Enter expression 2")
        result = mutation_expression[mutation_expression['expression 2'].str.contains(expression2_search, case=False)]
        st.write("Search Results:")
        st.write(result)

    elif search_type == "All":
        search_query = st.text_input("Enter search query")
        result = mutation_expression[mutation_expression.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]
        st.write("Search Results:")
        st.write(result)

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

    # Display the gene-specific network
    st.write('### Gene-specific Network (Graph)')
    G = nx.Graph()
    with open(network_file_path, 'r') as network_file:
        for line in network_file:
            parts = line.strip().split('\t')
            if len(parts) >= 3:  # Check if there are at least 3 parts in the line
                node1, interaction, node2 = parts[:3]
                G.add_edge(node1, node2, label=interaction)  # Add edge with interaction as label

    fig, ax = plt.subplots(figsize=(10, 8))  # Set figure size
    pos = nx.spring_layout(G, k=0.5)  # Adjust k for spacing between nodes
    nx.draw(G, pos, with_labels=True, font_size=10, node_color='lightblue', edge_color='gray', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='gray', ax=ax)
    ax.set_title('Gene-specific Network')
    st.pyplot(fig)

else:  # Contact Us
    st.header("Contact Us")
    st.write("Author: Siddharth Singh")
    st.write("Mail: siddharth1r2@gmail.com")
    st.write("LinkedIn: [Siddharth Singh](https://www.linkedin.com/in/siddharth-singh-ab80951a0/)")
