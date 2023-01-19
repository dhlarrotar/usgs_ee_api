import requests
import os

# define the API endpoint
api_endpoint = "https://github.com/dhlarrotar/usgs_ee_api/blob/main/eesearch.py"

# define the search criteria
location = "35.68,139.75"
date_range = "2022-01-01,2022-01-31"
cloud_cover = "20"
api_key = "YOUR_VALID_API_KEY"
download=False



# send the GET request to the API endpoint
response = requests.get(f"{api_endpoint}?location={location}&date_range={date_range}&cloud_cover={cloud_cover}&api_key={api_key}")

# parse the response
response_json = response.json()


# print the number of scenes found
print(f"Number of scenes found: {response_json['number_of_scenes']}")

for scene in response_json['scenes']:
    print(f"Scene {scene['id']}")
    print(f"Location: {scene['location']}")
    print(f"Date: {scene['date']}")
    print(f"Cloud cover: {scene['cloud_cover']}%")
    print(f"File name: {scene['file_name']}")

