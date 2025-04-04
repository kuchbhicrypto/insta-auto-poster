import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image_url = request.form['image_url']
    caption = request.form['caption']
    
    # ⚠️ Add your Instagram upload logic here (via Graph API)
    print(f"Posting to Instagram...\nImage: {image_url}\nCaption: {caption}")
    
    return f"✅ Image scheduled for Instagram!\nImage: {image_url}\nCaption: {caption}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render binds to this PORT
    app.run(host='0.0.0.0', port=port, debug=True)
