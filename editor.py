import os

def delete_column(file_path, column_index_to_delete=2, overwrite=True):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    cleaned_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) > column_index_to_delete:
            del parts[column_index_to_delete]
        cleaned_lines.append(' '.join(parts))

    output_path = file_path if overwrite else file_path.replace('.txt', '_cleaned.txt')

    with open(output_path, 'w') as outfile:
        outfile.write('\n'.join(cleaned_lines))

    print(f"Column {column_index_to_delete + 1} removed. Saved to: {output_path}")

# Example usage:
if __name__ == "__main__":
    # Change this to your file path
    file_path = r"E:\CSE491 Project\Project-1_Graph_Coloring\Dataset\New\New 1\soc-sign-Slashdot081106.txt\soc-sign-Slashdot081106.txt"
    
    # Call the function
    delete_column(file_path, column_index_to_delete=2, overwrite=True)  # column index starts from 0
