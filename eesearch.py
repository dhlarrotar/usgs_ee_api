from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# define the folder where the scenes will be stored
scenes_folder = "scenes"

@app.route("/search", methods=["GET"])
def search():
    location = request.args.get("location")
    date_range = request.args.get("date_range")
    cloud_cover = request.args.get("cloud_cover")
    download = request.args.get("download")
    
    # construct the search query and send it to the USGS Earth Explorer catalog
    search_url = f"https://earthexplorer.usgs.gov/search?location={location}&date_range={date_range}&cloud_cover={cloud_cover}&api_key={api_key}"
    search_results = requests.get(search_url).json()
    
    # parse the response and extract the relevant information for each scene
    scenes = []
    for result in search_results["results"]:
        scene = {
            "id": result["id"],
            "location": result["location"],
            "date": result["date"],
            "cloud_cover": result["cloud_cover"],
            "file_name": result["file_name"]
        }
         # calculate NDVI
        scene_url = f"https://earthexplorer.usgs.gov/download?item_id={scene['id']}&api_key={api_key}"
        scene_data = requests.get(scene_url).json()
        red = scene_data["bands"]["red"]
        nir = scene_data["bands"]["nir"]
        ndvi = (nir - red) / (nir + red)
        scene["ndvi"] = ndvi
        
        if download:
            # check if the scene is already in the scenes folder
            file_path = f"{scenes_folder}/{scene['file_name']}"
            if not os.path.exists(file_path):
                # download the scene
                download_url = f"https://earthexplorer.usgs.gov/download?item_id={scene['id']}&api_key={api_key}"
                response = requests.get(download_url)
                open(file_path, "wb").write(response.content)

        
        scenes.append(scene)


@app.route("/delete", methods=["DELETE"])
def delete_scene():
    scene_id = request.args.get("id")
    file_path = f"{scenes_folder}/{scene_id}.tif"
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"status": "success", "message": f"Scene {scene_id} has been deleted."})
    else:
        return jsonify({"status": "error", "message": f"Scene {scene_id} not found."})
        
       
    # format the response as a JSON object
    response = {
        "number_of_scenes": len(scenes),
        "scenes": scenes
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run()