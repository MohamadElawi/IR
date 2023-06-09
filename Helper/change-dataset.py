def process_data(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        # Read the contents of the file
        content = input_file.read()

        # Remove the first row
        content = content.split('\n', 1)[1]

        # Replace spaces with commas
        content = content.replace(',', '\t')

    with open(output_file_path, 'w') as output_file:
        # Write the processed data to the output file
        output_file.write(content)

    print("Data processed and saved to", output_file_path)


# file_path = 'resources/wikIR1k/documents.csv'
# file_output = 'resources/wikIR1k/documents-new.tsv'

file_path = '../resources/wikIR1k/validation/queries.csv'
file_output = '../resources/wikIR1k/validation/queries-new.csv'


process_data(file_path ,file_output)






