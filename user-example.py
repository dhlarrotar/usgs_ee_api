import requests
import os

# define the API endpoint
api_endpoint = "/eesearch.py"

# define the search criteria
location = "35.68,139.75"
date_range = "2022-01-01,2022-01-31"
cloud_cover = "20"
api_key = "YOUR_VALID_API_KEY"

# define the folder where the scenes will be stored
scenes_folder = "scenes"

# send the GET request to the API endpoint
response = requests.get(f"{api_endpoint}?location={location}&date_range={date_range}&cloud_cover={cloud_cover}&api_key={api_key}")

# parse the response
response_json = response.json()

# create the scenes folder if it doesn't exist
if not os.path.exists(scenes_folder):
    os.makedirs(scenes_folder)

# print the number of scenes found
print(f"Number of scenes found: {response_json['number_of_scenes']}")

# download the scenes
for scene in response_json["scenes"]:
    file_path = f"{scenes_folder}/{scene['file_name']}"
    if not os.path.exists(file_path):
        # download the scene
        download_url = f"https://earthexplorer.usgs.gov/download?item_id={scene['id']}&api_key={api_key}"
        response = requests.get(download_url)
        open(file_path, "wb").write(response.content)
        print(f"Scene {scene['id']} has been downloaded.")
    else:
        print(f"Scene {scene['id']} already exists in the scenes folder.")