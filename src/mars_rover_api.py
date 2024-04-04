import os
import requests

API_KEY = "YOUR_API_KEY"

base_url = "https://api.nasa.gov/mars-photos/api/v1"

info = {
    "curiosity": {
        "name": "Curiosity",
        "cameras": ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"]
    },
    "opportunity": {
        "name": "Opportunity",
        "cameras": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"]
    },
    "spirit": {
        "name": "Spirit",
        "cameras": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"]
    }
}


def get_manifest(rover_name):
    manifest_url = f"{base_url}/manifests/{rover_name}"
    response = requests.get(manifest_url, params={"api_key": API_KEY})
    if response.status_code == 200:
        manifest = response.json()['photo_manifest']
        return manifest
    else:
        print("Failed to fetch mission manifest:", response.status_code)
        return None


def fetch_photo(rover_name, earth_date, camera):
    photos_url = f"{base_url}/rovers/{rover_name}/photos"
    params = {
        "earth_date": earth_date,
        "camera": camera,
        "api_key": API_KEY
    }
    response = requests.get(photos_url, params=params)
    if response.status_code == 200:
        photos_data = response.json()
        if photos_data['photos']:
            photo_url = photos_data['photos'][0]['img_src']
            return photo_url
        else:
            print(f"\nNo photo available for {rover_name}, date {earth_date}, camera {camera}")
            return None
    else:
        print(f"\nFailed to fetch photo for {rover_name}, date {earth_date}, camera {camera}: {response.status_code}")
        return None


def save_photo(rover_name, camera_name, earth_date, photo_url):
    response = requests.get(photo_url)
    if response.status_code == 200:
        content_type = response.headers['content-type']
        if 'image' in content_type:
            extension = content_type.split('/')[-1]
        else:
            extension = '.jpg'  # Default extension if content type is not image
        file_name = f"{rover_name}_{camera_name}_{earth_date}.{extension}"
        save_path = os.path.join("results", file_name)

        if not os.path.exists("results"):
            os.makedirs("results")

        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"\nPhoto saved successfully: {save_path}")
    else:
        print(f"Failed to save photo: {response.status_code}")
