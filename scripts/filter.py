import json
from shapely.geometry import Point, Polygon

polygon_coordinates = [[-72.57495,41.5046],[-72.57413,41.51164],[-72.56323,41.516],[-72.53239,41.55149],[-72.3317,41.62854],[-72.32898,41.63952],[-72.33702,41.64217],[-72.37603,41.63288],[-72.45404,41.60779],[-72.48255,41.64195],[-72.52741,41.6618],[-72.60467,41.64994],[-72.64271,41.60874],[-72.64271,41.59795],[-72.65299,41.58801],[-72.7029,41.58276],[-72.76191,41.58501],[-72.77987,41.55031],[-72.74702,41.50231],[-72.67862,41.4543],[-72.62274,41.46335],[-72.59843,41.49002],[-72.57495,41.5046]]

bounding_polygon = Polygon(polygon_coordinates)

# Function to check if a coordinate is within the bounding box
def within_filter(lon,lat):
    point = Point(lon, lat)
    return bounding_polygon.contains(point)

routes=[]
# Read the input JSON file
#names = ["bruce", "calder", "calhoun", "dale", "don", "dylan", "evan", "foge", "jude", "kerm", "lara", "levine"
# , "mike", "miles", "mckinney","noah", "owen", "phil", "ratner", "rob", "sam", "taffet", "tony","will", "zallen"]
names =["chid"]
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
            inside=False
            for cor in route['features'][0]['geometry']['coordinates'][0]:
                #lon = route['features'][0]['geometry']['coordinates'][0][0][0]
                #lat = route['features'][0]['geometry']['coordinates'][0][0][1]
                lon=cor[0]
                lat=cor[1]
            
                if within_filter(lon, lat):
                    inside=True
            if inside:
                json_str = json.dumps(route)  # Serialize the JSON object
                file.write(f"\nroutes.push({json_str});")
