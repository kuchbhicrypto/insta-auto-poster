'''
import schedule
import time
from upload_image import upload_image
from upload_reel import upload_reel

# Every day at 12 PM — image
schedule.every().day.at("11:20").do(upload_image)

# Every day at 6 PM — reel
schedule.every().day.at("11:21").do(upload_reel)

print("✅ Scheduler started!")

while True:
    schedule.run_pending()
    time.sleep(60)
'''

import schedule
import time

def post_image():
    print("Post uploaded successfully!")

def run_schedule():
    # Set specific times to post (you can change these times)
    schedule.every().day.at("12:00").do(post_image)  # Post at 12 PM
    schedule.every().day.at("18:00").do(post_image)  # Post at 6 PM
    while True:
        schedule.run_pending()  # Keeps checking the schedule
        time.sleep(1)

if __name__ == "__main__":
    run_schedule()
