#to start just keeping page number and run it every fifteen minutes
import requests
import polyline
import json
import time

def get_activities(access_token,page):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'per_page': 125, 'page': page}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        activities = response.json()
        if len(activities) == 0:
            print("No activities found on the 4th page.")
            return None
        return activities
    else:
        print(f"Error: {response.status_code} when accessing activities")
        print(response.json())
        return None

def extract_runs(activities):
    return [activity for activity in activities if activity['type'] == 'Run']

def get_activity_details(access_token, run_id):
    url = f'https://www.strava.com/api/v3/activities/{run_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} when accessing activity {run_id}")
        print(response.json())
        return None
    
def add_routes_to_file(access_token,page,file_path):
    activities = get_activities(access_token,page)
    
    if activities:
        runs = extract_runs(activities)
        runs.reverse()
        for run in runs:
            run_id = run['id']
            activity = get_activity_details(access_token, run_id)

            if activity:
                poly_str = activity.get('map', {}).get('polyline')
                start_date = activity.get('start_date')

                if poly_str:
                    coordinates = polyline.decode(poly_str)
                    coords = [[lon, lat] for lat, lon in coordinates]

                    geojson_data = {
                            "type": "FeatureCollection",
                            "features": [
                                {
                                    "type": "Feature",
                                    "start": start_date,
                                    "geometry": {
                                        "type": "MultiLineString",
                                        "coordinates": [coords]
                                    },
                                    "properties": {}
                                }
                            ]
                    }


                    with open(file_path, "a") as file:
                        file.write(f"\nroutes.push({json.dumps(geojson_data)});")

                        print(f"GeoJSON data for run {run_id} written to {file_path}")
    else:
        print("No activities found.")

if __name__ == "__main__":
    access_token = '339aae7e908b761b6bedf0a7e7f22b39e9a0bb02'
    num_pages = 8 #this is 8 for me since i have just under 1000 runs and 125 per page so 8 pages.
    for i in range(num_pages):
        add_routes_to_file(access_token,num_pages-i,"test.js")
        time.sleep(15*60)


    