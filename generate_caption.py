import requests

def generate_caption(image_description):
    api_key = "YOUR_GEMINI_API_KEY"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "contents": [{
            "parts": [{"text": f"Write a viral Instagram caption with emojis and 10 trending hashtags for a photo of: {image_description}"}]
        }]
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    return result['candidates'][0]['content']['parts'][0]['text']
