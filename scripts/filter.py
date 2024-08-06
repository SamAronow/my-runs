import json
from shapely.geometry import Point, Polygon
import os

midd_coordinates = [[-72.57495,41.5046],[-72.57413,41.51164],[-72.56323,41.516],[-72.53239,41.55149],[-72.3317,41.62854],[-72.32898,41.63952],[-72.33702,41.64217],[-72.37603,41.63288],[-72.45404,41.60779],[-72.48255,41.64195],[-72.52741,41.6618],[-72.60467,41.64994],[-72.64271,41.60874],[-72.64271,41.59795],[-72.65299,41.58801],[-72.7029,41.58276],[-72.76191,41.58501],[-72.77987,41.55031],[-72.74702,41.50231],[-72.67862,41.4543],[-72.62274,41.46335],[-72.59843,41.49002],[-72.57495,41.5046]]
freeman_coordinates = [[-72.66281,41.55217],[-72.66554,41.5514],[-72.66908,41.54977],[-72.67141,41.54833],[-72.66957,41.54441],[-72.66699,41.54127],[-72.67026,41.53494],[-72.67036,41.53323],[-72.66705,41.53261],[-72.66542,41.53357],[-72.66526,41.53481],[-72.66407,41.53504],[-72.66346,41.53585],[-72.66184,41.5371],[-72.66137,41.53863],[-72.65919,41.54423],[-72.65847,41.54805],[-72.65794,41.55146],[-72.65819,41.55408],[-72.66272,41.5522]]

#[[-72.66264,41.55182],[-72.66531,41.55084],[-72.66908,41.54977],[-72.67141,41.54833],[-72.66957,41.54441],[-72.66664,41.54138],[-72.67026,41.53494],[-72.67036,41.53357],[-72.66705,41.53261],[-72.66542,41.53357],[-72.66526,41.53481],[-72.66407,41.53504],[-72.66346,41.53585],[-72.66137,41.53863],[-72.65919,41.54423],[-72.65847,41.54805],[-72.65794,41.55146],[-72.65807,41.55389],[-72.6625,41.55191]]
midd_polygon = Polygon(midd_coordinates)
freeman_polygon = Polygon(freeman_coordinates)

# Function to check if a coordinate is within the bounding box
def within_filter(lon,lat):
    point = Point(lon, lat)
    return midd_polygon.contains(point) and not freeman_polygon.contains(point)

# Read the input JSON file
#names = ["bruce", "calder", "calhoun","chid", "dale", "don", "dylan", "evan", "foge", "george","jude", "kerm", "lara", "levine"
# , "mike", "miles", "mckinney","noah", "owen", "phil", "ratner", "rob", "sam", "taffet", "tony","will", "zallen"]
names =["bruce", "calder", "calhoun","chid", "dale", "don", "dylan", "evan", "foge", "george","jude", "kerm", "lara", "levine", "mike", "miles", "mckinney","noah", "owen", "phil", "ratner", "rob", "sam", "taffet", "tony", "will", "zallen"]
for name in names:
    routes=[]
    print(name)
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

    file_path="../people/wes_"+name+".js"

    with open("temp.js", "w") as file:
        file.write("var routes = new Array(0);\n")  # Initialize the routes array

        for route in routes:
            inside=False
            for cor in route['features'][0]['geometry']['coordinates'][0]:
                lon=cor[0]
                lat=cor[1]
            
                if within_filter(lon, lat):
                    inside=True
            if inside:
                json_str = json.dumps(route)  # Serialize the JSON object
                file.write(f"\nroutes.push({json_str});")

    with open('temp.js', 'r') as file:
        content = file.read()

    content = content.replace('routes', 'wes_'+name)

    with open(file_path, 'w') as file:
        file.write(content)

    os.remove("temp.js")