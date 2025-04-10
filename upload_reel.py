"""
import os
import shutil
import json
import requests
import cloudinary
import cloudinary.uploader

# === Load Tokens ===

with open("tokens.json", "r") as f:
    tokens = json.load(f)

ACCESS_TOKEN = tokens['instagram']['access_token']
INSTAGRAM_ACCOUNT_ID = tokens['instagram']['account_id']

cloudinary.config(
    cloud_name=tokens['cloudinary']['cloud_name'],
    api_key=tokens['cloudinary']['api_key'],
    api_secret=tokens['cloudinary']['api_secret']
)

# === FOLDER PATHS ===

REEL_TO_UPLOAD = "static/ReelToUpload"
REEL_UPLOADED = "static/ReelUploaded"

# === Functions ===

def upload_video_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(
        file_path,
        resource_type="video",
        chunk_size=6000000  # 6MB chunks for large files
    )
    return result['secure_url']

def post_reel_to_instagram(video_url, caption=""):
    media_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_data = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }

    media_res = requests.post(media_url, data=media_data)
    media_result = media_res.json()

    if "id" not in media_result:
        print("❌ Failed to create media object:", media_result)
        return False

    creation_id = media_result["id"]

    publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_data = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }

    publish_res = requests.post(publish_url, data=publish_data)
    print("✅ Instagram upload response:", publish_res.json())
    return True

def move_to_uploaded_folder(file_path):
    os.makedirs(REEL_UPLOADED, exist_ok=True)
    shutil.move(file_path, os.path.join(REEL_UPLOADED, os.path.basename(file_path)))

def upload_reel():
    files = [f for f in os.listdir(REEL_TO_UPLOAD) if f.lower().endswith(('.mp4', '.mov', '.avi'))]

    if not files:
        print("📂 No reels to upload.")
        return

    file_to_upload = os.path.join(REEL_TO_UPLOAD, files[0])
    print(f"🚀 Uploading: {file_to_upload}")

    try:
        cloudinary_url = upload_video_to_cloudinary(file_to_upload)
        print(f"☁️ Uploaded to Cloudinary: {cloudinary_url}")

        success = post_reel_to_instagram(cloudinary_url, caption="🎬 Auto-posted Reel via Scheduler!")
        if success:
            move_to_uploaded_folder(file_to_upload)
            print("✅ Moved to ReelUploaded/")
        else:
            print("❌ Posting failed.")

    except Exception as e:
        print(f"🔥 Error: {e}")
"""

import os
import shutil
import json
import time
import requests
import cloudinary
import cloudinary.uploader

print("✅ Script started!")

# === Load Tokens ===
with open("tokens.json", "r") as f:
    tokens = json.load(f)

ACCESS_TOKEN = tokens['instagram']['access_token']
INSTAGRAM_ACCOUNT_ID = tokens['instagram']['account_id']

cloudinary.config(
    cloud_name=tokens['cloudinary']['cloud_name'],
    api_key=tokens['cloudinary']['api_key'],
    api_secret=tokens['cloudinary']['api_secret']
)

# === FOLDER PATHS ===
REEL_TO_UPLOAD = "static/ReelToUpload"
REEL_UPLOADED = "static/ReelUploaded"

# === Functions ===
def upload_video_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(file_path, resource_type="video")
    return result['secure_url']

def post_reel_to_instagram(video_url, caption=""):
    media_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_data = {
        "video_url": video_url,
        "caption": caption,
        "media_type": "REELS",
        "access_token": ACCESS_TOKEN
    }

    media_res = requests.post(media_url, data=media_data)
    media_result = media_res.json()

    if "id" not in media_result:
        print("❌ Failed to create media object:", media_result)
        return False

    creation_id = media_result["id"]

    time.sleep(10)  # ⏱️ wait 10 seconds for media to be ready

    publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_data = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }

    publish_res = requests.post(publish_url, data=publish_data)
    print("✅ Instagram upload response:", publish_res.json())
    return True

def move_to_uploaded_folder(file_path):
    os.makedirs(REEL_UPLOADED, exist_ok=True)
    shutil.move(file_path, os.path.join(REEL_UPLOADED, os.path.basename(file_path)))

def upload_reel():
    files = [f for f in os.listdir(REEL_TO_UPLOAD) if f.lower().endswith(('.mp4', '.mov', '.avi'))]

    if not files:
        print("📂 No reels to upload.")
        return

    file_to_upload = os.path.join(REEL_TO_UPLOAD, files[0])
    print(f"🚀 Uploading: {file_to_upload}")

    try:
        # Generate Caption + Hashtags
        from caption_generator import extract_thumbnail, generate_caption_and_hashtags_from_image
        thumbnail = extract_thumbnail(file_to_upload)
        ai_data = generate_caption_and_hashtags_from_image(thumbnail)
        caption = ai_data['caption']
        hashtags = ai_data['hashtags']
        full_caption = caption + "\n" + " ".join(hashtags)

        # 🔥 Print the generated caption and hashtags
        print(f"📝 Generated Caption: {caption}")
        print(f"🏷️ Hashtags: {' '.join(hashtags)}")

        # Upload to Cloudinary
        cloudinary_url = upload_video_to_cloudinary(file_to_upload)
        print(f"☁️ Uploaded to Cloudinary: {cloudinary_url}")

        # Post to Instagram
        success = post_reel_to_instagram(cloudinary_url, caption=full_caption)
        if success:
            move_to_uploaded_folder(file_to_upload)
            print("✅ Moved to ReelUploaded/")
        else:
            print("❌ Posting failed.")

    except Exception as e:
        print(f"🔥 Error: {e}")
