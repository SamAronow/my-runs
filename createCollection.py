import json
import re

# Read the JavaScript file
with open('people/wes_all.js', 'r') as file:
    js_code = file.read()

# Regular expression to find the JSON objects within the push statements
json_objects = re.findall(r'routes\.push\((\{.*?\})\);', js_code, re.DOTALL)

# Function to clean and convert JS-like JSON to proper JSON
def clean_json(js_str):
    # Replace single quotes with double quotes
    js_str = js_str.replace("'", '"')
    # Remove any trailing commas before the closing brackets
    js_str = re.sub(r",\s*([\]}])", r"\1", js_str)
    return js_str

# Convert the extracted JSON objects into Python dictionaries
routes = [json.loads(clean_json(obj)) for obj in json_objects]

# Initialize the array to store the start time and coordinates
start_coords_array = []

# Iterate over the routes and extract the start time and coordinates
for route in routes:
    features = route.get("features", [])
    for feature in features:
        start = feature.get("start", None)
        coordinates = feature.get("geometry", {}).get("coordinates", None)
        if start and coordinates:
            # Append the start time and coordinates as a list of 2 elements
            start_coords_array.append([start, coordinates])

# Initialize the content for the JS file

feature_collection_content = 'const featureCollection = {\n'
feature_collection_content += '    "type": "FeatureCollection",\n'
feature_collection_content += '    "features": [\n'

# Construct the features for the JS file
for start, coordinates in start_coords_array:
    feature_collection_content += '        {\n'
    feature_collection_content += '            "type": "Feature",\n'
    feature_collection_content += '            "properties": {\n'
    feature_collection_content += f'                "name": "{start}"\n'
    feature_collection_content += '            },\n'
    feature_collection_content += '            "geometry": {\n'
    feature_collection_content += '                "type": "LineString",\n'
    feature_collection_content += f'                "coordinates": {json.dumps(coordinates[0])}\n'
    feature_collection_content += '            }\n'
    feature_collection_content += '        },\n'

# Remove the last comma and close the JSON structure
feature_collection_content = feature_collection_content.rstrip(',\n') + '\n'
feature_collection_content += '    ]\n'
feature_collection_content += '};\n'

# Write the content to a new JS file
with open('featureCollections/wes_all.js', 'w') as file:
    file.write(feature_collection_content)

print("feature_sam.js has been created successfully.")
