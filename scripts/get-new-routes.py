#to start just keeping page number and run it every fifteen minutes
import requests
import polyline
import json
from datetime import datetime

def get_activities(access_token):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'per_page': 10, 'page': 1}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        activities = response.json()
        if len(activities) == 0:
            print("No activities found on the 1st page.")
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

if __name__ == "__main__":
    access_token = '8de23f5f44e602fe5de83a69b4d472ac1e3ec85b'
    activities = get_activities(access_token)
    file_path = "people/sam.js"
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        last_start=last_line[85:105]
        print(last_start)
        last_start_time = datetime.fromisoformat(last_start)
    
    if activities:
        runs = extract_runs(activities)
        runs.reverse()
        for run in runs:
            run_id = run['id']
            activity = get_activity_details(access_token, run_id)

            if activity:
                poly_str = activity.get('map', {}).get('polyline')
                start_date = activity.get('start_date')
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))


                if start_datetime > last_start_time and poly_str:
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
