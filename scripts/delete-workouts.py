import json
from shapely.geometry import Point, Polygon

polygon_coordinates = [[-72.66193,41.55227],[-72.66472,41.55146],[-72.66588,41.55034],[-72.66898,41.54992],[-72.67132,41.54862],[-72.67069,41.54481],[-72.66898,41.54443],[-72.66685,41.54278],[-72.66699,41.533],[-72.66598,41.53292],[-72.66542,41.53466],[-72.6656,41.54296],[-72.65922,41.54382],[-72.65881,41.54865],[-72.65779,41.55103],[-72.65806,41.55395],[-72.66188,41.55229]]

bounding_polygon = Polygon(polygon_coordinates)

# Function to check if a coordinate is within the bounding box
def within_filter(lon,lat):
    point = Point(lon, lat)
    return bounding_polygon.contains(point)

routes=[]
# Read the input JSON file
#names = ["bruce", "calder", "calhoun", "dale", "don", "dylan", "evan", "foge", "george","jude", "kerm", "lara", "levine"
# , "mike", "miles", "mckinney","noah", "owen", "phil", "ratner", "rob", "sam", "taffet", "tony","will", "zallen"]
names =["wesBruce"]
for name in names:
    file='../people/'+name+".js"
    with open(file, 'r') as infile:
        lines = infile.readlines()[2:]  # Skip the first two lines

    i=0
    for line in lines:
        i=i+1
        # Extract the substring from the 13th character to the third-to-last character
        json_str = line[12:-3]
        try:
            json_obj = json.loads(json_str)
            routes.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {i}")
            print(f"Error message: {e}")

    file_path="../people/wes-"+name+".js"
    with open(file_path, "w") as file:
        file.write("var routes = new Array(0);\n")  # Initialize the routes array

        for route in routes:
            outside=False
            for cor in route['features'][0]['geometry']['coordinates'][0]:
                lon=cor[0]
                lat=cor[1]
            
                if not within_filter(lon, lat):
                    outside=True
            if outside:
                json_str = json.dumps(route)  # Serialize the JSON object
                file.write(f"\nroutes.push({json_str});")


                                                                      