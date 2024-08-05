#names = ["bruce", "calder", "calhoun", "dale", "don", "dylan", "evan", "foge", "jude", "kerm", "lara", "levine"]
names = ["mckinney", "mike", "miles", "noah", "owen", "phil", "ratner","rob", "sam", "taffet", "will", "zallen"]
# Open wes-all.js in write mode
with open('../wes-all.js', 'w') as all_file:
    for name in names:
        # Write the name as a comment
        all_file.write(f'// {name}\n')

        # Open wes-name.js and read its content
        with open(f'../people/wes-{name}.js', 'r') as name_file:
            # Skip the first two lines
            next(name_file)
            next(name_file)
            content = name_file.read()
        
        # Write the content to wes-all.js
        all_file.write(content)
        all_file.write('\n')  # Add a newline for separation between files

print("Content copied successfully!")
