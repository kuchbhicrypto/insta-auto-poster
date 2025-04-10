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

IMG_TO_UPLOAD = "static/ImageToUpload"
IMG_UPLOADED = "static/ImageUploaded"

# === Functions ===

def upload_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result['secure_url']

def post_to_instagram(image_url, caption=""):
    media_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_data = {
        "image_url": image_url,
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
    os.makedirs(IMG_UPLOADED, exist_ok=True)
    shutil.move(file_path, os.path.join(IMG_UPLOADED, os.path.basename(file_path)))

def upload_image():
    files = [f for f in os.listdir(IMG_TO_UPLOAD) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not files:
        print("📂 No images to upload.")
        return

    file_to_upload = os.path.join(IMG_TO_UPLOAD, files[0])
    print(f"🚀 Uploading: {file_to_upload}")

    try:
        cloudinary_url = upload_to_cloudinary(file_to_upload)
        print(f"☁️ Uploaded to Cloudinary: {cloudinary_url}")

        success = post_to_instagram(cloudinary_url, caption="✨ Auto-posted via Scheduler!")
        if success:
            move_to_uploaded_folder(file_to_upload)
            print("✅ Moved to ImgUploaded/")
        else:
            print("❌ Posting failed.")

    except Exception as e:
        print(f"🔥 Error: {e}")


import os
import shutil
import json
import requests
import cloudinary
import cloudinary.uploader
from caption_generator import generate_caption_and_hashtags_from_image

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
IMG_TO_UPLOAD = "static/ImageToUpload"
IMG_UPLOADED = "static/ImageUploaded"

def upload_image_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(file_path, resource_type="image")
    return result['secure_url']

def post_image_to_instagram(image_url, caption=""):
    media_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_data = {
        "image_url": image_url,
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
    os.makedirs(IMG_UPLOADED, exist_ok=True)
    shutil.move(file_path, os.path.join(IMG_UPLOADED, os.path.basename(file_path)))

def upload_image():
    files = [f for f in os.listdir(IMG_TO_UPLOAD) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not files:
        print("📂 No images to upload.")
        return

    file_to_upload = os.path.join(IMG_TO_UPLOAD, files[0])
    print(f"🚀 Uploading: {file_to_upload}")

    try:
        # Generate caption + hashtags from image
        ai_data = generate_caption_and_hashtags_from_image(file_to_upload)
        full_caption = ai_data['caption'] + "\n" + " ".join(ai_data['hashtags'])

        # Upload to Cloudinary
        cloudinary_url = upload_image_to_cloudinary(file_to_upload)
        print(f"☁️ Uploaded to Cloudinary: {cloudinary_url}")

        # Post to Instagram
        success = post_image_to_instagram(cloudinary_url, caption=full_caption)
        if success:
            move_to_uploaded_folder(file_to_upload)
            print("✅ Moved to ImgUploaded/")
        else:
            print("❌ Posting failed.")

    except Exception as e:
        print(f"🔥 Error: {e}")


import os
import shutil
import json
import requests
import cloudinary
import cloudinary.uploader
import re
from caption_generator import generate_caption_and_hashtags_from_image

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
IMG_TO_UPLOAD = "static/ImageToUpload"
IMG_UPLOADED = "static/ImageUploaded"

def upload_image_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(file_path, resource_type="image")
    return result['secure_url']

def post_image_to_instagram(image_url, caption=""):
    media_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_data = {
        "image_url": image_url,
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
    os.makedirs(IMG_UPLOADED, exist_ok=True)
    shutil.move(file_path, os.path.join(IMG_UPLOADED, os.path.basename(file_path)))

def upload_image():
    files = [f for f in os.listdir(IMG_TO_UPLOAD) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not files:
        print("📂 No images to upload.")
        return

    file_to_upload = os.path.join(IMG_TO_UPLOAD, files[0])
    print(f"🚀 Uploading: {file_to_upload}")

    try:
        # Generate caption + hashtags from image
        ai_data = generate_caption_and_hashtags_from_image(file_to_upload)
        print("🧠 AI Output:", ai_data)

        full_caption = ai_data['caption'] + "\n" + " ".join(ai_data['hashtags'])

        # Upload to Cloudinary
        cloudinary_url = upload_image_to_cloudinary(file_to_upload)
        print(f"☁️ Uploaded to Cloudinary: {cloudinary_url}")

        # Post to Instagram
        success = post_image_to_instagram(cloudinary_url, caption=full_caption)
        if success:
            move_to_uploaded_folder(file_to_upload)
            print("✅ Moved to ImgUploaded/")
        else:
            print("❌ Posting failed.")

    except Exception as e:
        print(f"🔥 Error during upload process: {e}")
"""
import os
import shutil
import json
import requests
import cloudinary
import cloudinary.uploader
from caption_generator import generate_caption_and_hashtags_from_image

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
IMG_TO_UPLOAD = "static/ImageToUpload"
IMG_UPLOADED = "static/ImageUploaded"

def upload_image_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(file_path, resource_type="image")
    return result['secure_url']

def post_image_to_instagram(image_url, caption=""):
    media_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_data = {
        "image_url": image_url,
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
    os.makedirs(IMG_UPLOADED, exist_ok=True)
    shutil.move(file_path, os.path.join(IMG_UPLOADED, os.path.basename(file_path)))

def upload_image():
    files = [f for f in os.listdir(IMG_TO_UPLOAD) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not files:
        print("📂 No images to upload.")
        return

    file_to_upload = os.path.join(IMG_TO_UPLOAD, files[0])
    print(f"🚀 Uploading: {file_to_upload}")

    try:
        # Generate caption + hashtags from image
        ai_data = generate_caption_and_hashtags_from_image(file_to_upload)
        caption = ai_data['caption']
        hashtags = ai_data['hashtags']
        full_caption = f"{caption}\n{' '.join(hashtags)}"

        # Upload to Cloudinary
        cloudinary_url = upload_image_to_cloudinary(file_to_upload)
        print(f"☁️ Uploaded to Cloudinary: {cloudinary_url}")

        # Post to Instagram
        success = post_image_to_instagram(cloudinary_url, caption=full_caption)
        if success:
            move_to_uploaded_folder(file_to_upload)
            print("✅ Moved to ImgUploaded/")
        else:
            print("❌ Posting failed.")

    except Exception as e:
        print(f"🔥 Error during upload process: {e}")
