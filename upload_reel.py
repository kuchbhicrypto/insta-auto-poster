import requests
import json
from generate_caption import generate_caption

def upload_reel():
    with open("tokens.json", "r") as f:
        tokens = json.load(f)

    access_token = tokens["access_token"]
    user_id = tokens["user_id"]

    video_url = "https://your-public-reel-url.mp4"
    caption = generate_caption("funny pet video")

    media_payload = {
        "video_url": video_url,
        "caption": caption,
        "access_token": access_token,
        "media_type": "REELS"
    }

    media_res = requests.post(f"https://graph.facebook.com/v18.0/{user_id}/media", data=media_payload)
    creation_id = media_res.json().get("id")

    publish_payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }

    publish_res = requests.post(f"https://graph.facebook.com/v18.0/{user_id}/media_publish", data=publish_payload)

    print("✅ Reel posted successfully!")
