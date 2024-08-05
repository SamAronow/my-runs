# Open the file in read mode
with open('../people/wes-chid.js', 'r') as file:
    # Read the file contents
    content = file.read()

# Replace all occurrences of 'routes' with 'routes1'
content = content.replace('routes', 'wesChid')

# Open the file in write mode
with open('../people/wesChid.js', 'w') as file:
    # Write the modified content back to the file
    file.write(content)

