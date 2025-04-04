from flask import Flask, request, redirect
import requests
import json

app = Flask(__name__)

CLIENT_ID = 'YOUR_INSTAGRAM_CLIENT_ID'
CLIENT_SECRET = 'YOUR_INSTAGRAM_CLIENT_SECRET'
REDIRECT_URI = 'https://YOUR_RENDER_URL/insta/callback'

@app.route('/')
def login():
    return f'''
    <h1>Auto Poster App</h1>
    <a href="https://api.instagram.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user_profile,user_media&response_type=code">Login with Instagram</a>
    '''

@app.route('/insta/callback')
def callback():
    code = request.args.get('code')

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    res = requests.post("https://api.instagram.com/oauth/access_token", data=payload)
    data = res.json()

    with open("tokens.json", "w") as f:
        json.dump(data, f, indent=4)

    return "✅ Instagram connected! Token saved."

if __name__ == '__main__':
    app.run(debug=True)
