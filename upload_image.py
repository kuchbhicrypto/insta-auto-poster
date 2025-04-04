import requests
import json
from generate_caption import generate_caption

def upload_image():
    with open("tokens.json", "r") as f:
        tokens = json.load(f)

    access_token = tokens["access_token"]
    user_id = tokens["user_id"]

    image_url = "https://your-public-image-url.jpg"
    caption = generate_caption("beach vacation")

    media_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }

    media_res = requests.post(f"https://graph.facebook.com/v18.0/{user_id}/media", data=media_payload)
    creation_id = media_res.json().get("id")

    publish_payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }

    publish_res = requests.post(f"https://graph.facebook.com/v18.0/{user_id}/media_publish", data=publish_payload)
    
    print("✅ Image posted successfully!")
