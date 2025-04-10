'''
import requests
import json

import requests
import json

# ⬇️ Load Gemini key from tokens.json
with open("tokens.json", "r") as f:
    tokens = json.load(f)

GEMINI_API_KEY = tokens["gemini_api_key"]

def generate_caption(image_context: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Write a short Instagram caption for: {image_context}"
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()

    # Debug Gemini API output
    print("🔍 Gemini Response:", json.dumps(result, indent=2))

    try:
        return result['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        return "📛 Failed to generate caption – check API response"



def generate_caption(desc="luxury travel"):
    api_key = "YOUR_GEMINI_API_KEY"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "contents": [{
            "parts": [{"text": f"Write a viral Instagram caption for: {desc}. Add emojis and 10 trending hashtags."}]
        }]
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    return result['candidates'][0]['content']['parts'][0]['text']




import os
import json
import google.generativeai as genai
import PIL.Image
import cv2
import json
import google.generativeai as genai
from PIL import Image

# === Load Gemini API Key ===
with open("tokens.json", "r") as f:
    tokens = json.load(f)

GEMINI_API_KEY = tokens['gemini']['api_key']

genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel('gemini-1.5-pro')
vision_model = genai.GenerativeModel('gemini-1.5-pro')
model = genai.GenerativeModel("models/gemini-1.5-pro")

# === Extract a Thumbnail from Reel ===
def extract_thumbnail(video_path, frame_time=2):
    thumbnail_path = "thumbnail.jpg"
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(fps * frame_time)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(thumbnail_path, frame)
        return thumbnail_path
    else:
        print("❌ Failed to extract thumbnail.")
        return None

# === Describe Image Using Gemini Vision ===
def describe_image_with_gemini(image_path):
    try:
        img = PIL.Image.open(image_path)

        response = vision_model.generate_content([
            "Describe what is happening in this Instagram Reel thumbnail in a short sentence.",
            img
        ])

        return response.text.strip()

    except Exception as e:
        print("🔥 Gemini Vision error:", e)
        return "Aesthetic Instagram reel content."

# === JSON Extract Helper ===
def safe_extract_json(output_text):
    try:
        json_str = re.search(r'\{.*\}', output_text, re.DOTALL).group(0)
        return json.loads(json_str)
    except Exception as e:
        print("⚠️ JSON extract error:", e)
        return {
            "caption": "✨ Auto-posted from Ella’s Empire!",
            "hashtags": ["#ai", "#luxury", "#explorepage", "#automation", "#ellasempire"]
        }

# === Generate Caption & Hashtags from Image ===
def generate_caption_and_hashtags_from_image(image_path):
    try:
        prompt = """
You are a creative Instagram content creator.
Look at this image and give a short, catchy caption and 10 relevant trending hashtags.
Respond ONLY in this JSON format:
{
  "caption": "...",
  "hashtags": ["#tag1", "#tag2", ...]
}
"""

        image = Image.open(image_path)
        print("📸 Sending to Gemini Vision...")
        print(f"🧠 Gemini Caption: {caption}")

        response = model.generate_content([prompt, image], stream=False)
        print(f"🏷️ Hashtags: {' '.join(hashtags)}")


        return safe_extract_json(response.text)

    except Exception as e:
        print("🔥 Gemini Vision Error:", e)
        return {
            "caption": "✨ Auto-posted from Ella’s Empire!",
            "hashtags": ["#ai", "#luxury", "#explorepage", "#automation", "#ellasempire"]
        }
'''

import os
import json
import re  # ✅ FIXED: Required for safe_extract_json
import google.generativeai as genai
import PIL.Image
from PIL import Image
import cv2

# === Load Gemini API Key ===
with open("tokens.json", "r") as f:
    tokens = json.load(f)

GEMINI_API_KEY = tokens['gemini']['api_key']
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro")

# === Extract a Thumbnail from Reel ===
def extract_thumbnail(video_path, frame_time=2):
    thumbnail_path = "thumbnail.jpg"
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(fps * frame_time)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(thumbnail_path, frame)
        return thumbnail_path
    else:
        print("❌ Failed to extract thumbnail.")
        return None

# === JSON Extract Helper ===
def safe_extract_json(output_text):
    try:
        json_str = re.search(r'\{.*\}', output_text, re.DOTALL).group(0)
        return json.loads(json_str)
    except Exception as e:
        print("⚠️ JSON extract error:", e)
        return {
            "caption": "✨ Auto-posted from Ella’s Empire!",
            "hashtags": ["#ai", "#luxury", "#explorepage", "#automation", "#ellasempire"]
        }

# === Generate Caption & Hashtags from Image ===
def generate_caption_and_hashtags_from_image(image_path):
    try:
        prompt = """
You are a creative Instagram content creator.
Look at this image and give a short, catchy caption and 10 relevant trending hashtags.
Respond ONLY in this JSON format:
{
  "caption": "...",
  "hashtags": ["#tag1", "#tag2", ...]
}
"""
        image = Image.open(image_path)
        print("📸 Sending to Gemini Vision...")

        response = model.generate_content([prompt, image], stream=False)

        # Extract JSON from Gemini output
        ai_data = safe_extract_json(response.text)
        print(f"🧠 Gemini Caption: {ai_data['caption']}")
        print(f"🏷️ Hashtags: {' '.join(ai_data['hashtags'])}")

        return ai_data

    except Exception as e:
        print("🔥 Gemini Vision Error:", e)
        return {
            "caption": "✨ Auto-posted from Ella’s Empire!",
            "hashtags": ["#ai", "#luxury", "#explorepage", "#automation", "#ellasempire"]
        }
