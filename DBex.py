import requests
import xml.etree.ElementTree as ET
import pandas as pd

def fetch_snps_for_gene():
    while True:
        gene_name = input("Enter the gene name: ")
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi?db=snp&term={gene_name}[Gene Name]+AND+human[Organism]&retmode=xml&retmax=1000&usehistory=y"
        search_response = requests.get(search_url)
        search_tree = ET.fromstring(search_response.content)
        webenv = search_tree.findtext(".//WebEnv")
        query_key = search_tree.findtext(".//QueryKey")
        fetch_url = f"{base_url}efetch.fcgi?db=snp&query_key={query_key}&WebEnv={webenv}&retmode=xml&rettype=xml&retmax=1000"
        fetch_response = requests.get(fetch_url)
        print(fetch_response.text)
        
        if input("\nRun SNP extraction again? (yes/no): ").lower() != 'yes':
            break

def combine_excel_sheets():
    while True:
        input_file = input("Enter the input Excel file name: ")
        output_file = input("Enter the output Excel file name: ")
        xls = pd.ExcelFile(input_file)
        df_list = []
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df['Sheet'] = sheet_name
            df_list.append(df)
        combined_df = pd.concat(df_list, ignore_index=True)
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            combined_df.to_excel(writer, index=False)
        print("Sheets combined successfully into:", output_file)
        
        if input("\nCombine another set of sheets? (yes/no): ").lower() != 'yes':
            break

def sort_excel_data():
    while True:
        existing_file = input("Enter the full path to the Excel file you want to sort: ")
        df = pd.read_excel(existing_file)
        keywords = input("Enter keywords to filter by (separated by comma): ").split(',')
        keywords = [keyword.strip() for keyword in keywords]
        filtered_df = df[df.apply(lambda row: any(keyword in str(value) for keyword in keywords for value in row.values), axis=1)]
        new_file = input("Enter the name of the new Excel file to save filtered results: ")
        filtered_df.to_excel(new_file, index=False)
        print("Filtered data saved to:", new_file)
        df = df[df.apply(lambda row: not any(keyword in str(value) for keyword in keywords for value in row.values), axis=1)]
        df.to_excel(existing_file, index=False)
        print("Original data updated after filtering and saved back to:", existing_file)
        
        if input("\nSort another Excel file? (yes/no): ").lower() != 'yes':
            break

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. SNP Extraction")
        print("2. Combine Excel Sheets")
        print("3. Sort Excel Data")
        print("4. Exit")
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            fetch_snps_for_gene()
        elif choice == '2':
            combine_excel_sheets()
        elif choice == '3':
            sort_excel_data()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please choose again.")

        if input("\nReturn to the main menu? (yes/no): ").lower() != 'yes':
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main_menu()
