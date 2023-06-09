import re

# Read the file
filename = '../resources/wikIR1k/validation/qrels'
with open(filename, 'r') as file:
    content = file.readlines()

# Process each line
modified_content = []
for line in content:
    # Remove extra whitespace
    line = re.sub(r'\s+', ' ', line.strip())

    # Split the line into elements
    elements = line.split(' ')

    # Ensure there are four elements
    if len(elements) == 4:
        modified_content.append(line)
    else:
        print(f"Ignoring line: {line}")

# Write the modified content back to the file
with open(filename, 'w') as file:
    file.write('\n'.join(modified_content))