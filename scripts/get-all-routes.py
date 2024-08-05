#to start just keeping page number and run it every fifteen minutes
import requests
import polyline
import json
import time

def get_activities(access_token,page):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'per_page': 145, 'page': page}

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
    access_token = '767560e712133877e6188d85f21103b9e0b19628'
    num_pages = 1 #this is 10 for me since i have just under 1000 runs and 100 per page so 10 pages.
    page = num_pages
    filename="../people/chid.js"
    while page>0:
        print(page)
        add_routes_to_file(access_token,page,filename)
        page = page-1
        if page==0:
            print("done")
            break
        print()
        break
        print(page)
        print()
        add_routes_to_file(access_token,page,filename)
        page = page-1
        if page==0:
            print("done")
            break
        time.sleep(15*60)
            
        


    
