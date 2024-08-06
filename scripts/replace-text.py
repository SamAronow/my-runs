# Open the file in read mode
with open('../people/wes-george.js', 'r') as file:
    # Read the file contents
    content = file.read()

# Replace all occurrences of 'routes' with 'routes1'
content = content.replace('routes', 'wesGeorge')

# Open the file in write mode
with open('../people/wesGeorge.js', 'w') as file:
    # Write the modified content back to the file
    file.write(content)

