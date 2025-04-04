import schedule
import time
from upload_image import upload_image
from upload_reel import upload_reel

# Every day at 12 PM — image
schedule.every().day.at("12:00").do(upload_image)

# Every day at 6 PM — reel
schedule.every().day.at("18:00").do(upload_reel)

print("✅ Scheduler started!")

while True:
    schedule.run_pending()
    time.sleep(60)
