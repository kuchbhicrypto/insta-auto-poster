import schedule
import time
import json
import requests
from generate_caption import generate_caption

def post_to_instagram():
    # Load token
    with open("tokens.json", "r") as f:
        tokens = json.load(f)

    access_token = tokens["access_token"]
    user_id = tokens["user_id"]

    # STEP 1: Upload image (URL must be public or base64 for reels)
    image_url = "https://your-public-image-url.jpg"
    caption = generate_caption("a luxury car on a beach road")

    # STEP 2: Create media object
    media_data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    res = requests.post(f"https://graph.facebook.com/v18.0/{user_id}/media", data=media_data)
    creation_id = res.json().get("id")

    # STEP 3: Publish it
    publish_data = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    res = requests.post(f"https://graph.facebook.com/v18.0/{user_id}/media_publish", data=publish_data)

    print("✅ Posted to Instagram!")

# Run daily at 12 PM
schedule.every().day.at("12:00").do(post_to_instagram)

print("Scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(60)
