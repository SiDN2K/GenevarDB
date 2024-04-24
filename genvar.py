import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Set page title and other configurations
st.set_page_config(page_title="GenevarDB - Type 2 Diabetes Genetic Variants Database")

# Home Page
st.markdown("# GenevarDB")
st.markdown("A comprehensive database of genetic variants of Type 2 Diabetes mellitus.")
st.markdown("This database features Single Nucleotide Polymorphisms of a collection of genes that are associated with the occurrence of Type 2 Diabetes.")

# Load the data files with updated file paths
coding_synonymous_variants = pd.read_csv('data/Genvariantsyn.csv')
coding_missense_variants = pd.read_csv('data/Genvariantmis.csv')
mutation_expression = pd.read_excel('data/try_version_1.xlsb.xlsx')

# Sidebar navigation
nav_selection = st.sidebar.radio("Navigation", ["Search", "Browse", "Contact Us"])

if nav_selection == "Search":
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
    gene_details = mutation_expression[mutation_expression['gene'] == gene_selected]
    st.write("Gene Overview:")
    st.write(gene_details)

else:  # Contact Us
    st.header("Contact Us")
    st.write("Author: Siddharth Singh")
    st.write("Mail: siddharth1r2@gmail.com")
    st.write("LinkedIn: [Siddharth Singh](https://www.linkedin.com/in/siddharth-singh-ab80951a0/)")
