import cv2
import mysql.connector
from deepface import DeepFace
import os
import smtplib
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
from twilio.rest import Client

# ===== MySQL Connection =====
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",  # <-- MySQL password
    database="surveillance"
)
cursor = db.cursor()

# ===== Email Alert =====
def send_email_alert(location_address):
    sender = "youremail@gmail.com"      # <-- Gmail ID
    password = "your_app_password"      # <-- Gmail App Password
    receiver = "headoffice@example.com" # <-- Head Office Email

    subject = "🚨 Unknown Person Detected"
    body = f"An unknown person was detected near:\n{location_address}\nCheck CCTV immediately."

    msg = MIMEText(body)
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print("[EMAIL SENT] Alert sent to head office")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

# ===== SMS Alert =====
def send_sms_alert(location_address):
    account_sid = "your_twilio_sid"
    auth_token = "your_twilio_auth_token"
    twilio_number = "+1XXXXXXXXXX"
    target_number = "+91XXXXXXXXXX"  # <-- Your phone number

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"🚨 Unknown Person Detected near {location_address}",
        from_=twilio_number,
        to=target_number
    )
    print("[SMS SENT] Alert SMS sent")

# ===== Buzzer Trigger (Optional - Raspberry Pi) =====
def trigger_buzzer():
    try:
        import RPi.GPIO as GPIO
        import time
        buzzer_pin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(buzzer_pin, GPIO.LOW)
        GPIO.cleanup()
        print("[BUZZER] Siren Triggered")
    except ImportError:
        print("[BUZZER] Raspberry Pi GPIO not available, skipping buzzer.")

# ===== Location Detection =====
def get_location():
    geolocator = Nominatim(user_agent="geoapi")
    latitude, longitude = 25.5937, 85.1376  # <-- CCTV location
    location = geolocator.reverse(f"{latitude}, {longitude}")
    return location.address if location else "Unknown Location"

# ===== Fetch DB Images =====
def fetch_images(table):
    cursor.execute(f"SELECT name, image_path FROM {table}")
    return cursor.fetchall()

criminals = fetch_images("criminals")
missing = fetch_images("missing_persons")
vip = fetch_images("vip_access")

# ===== Face Matching =====
def match_with_db(face_img, db_data):
    for person in db_data:
        name, img_path = person
        if os.path.exists(img_path):
            try:
                result = DeepFace.verify(face_img, img_path, enforce_detection=False)
                if result["verified"]:
                    return name
            except:
                pass
    return None

# ===== Start Camera =====
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    face_detected = "frame.jpg"
    cv2.imwrite(face_detected, frame)

    matched = (
        match_with_db(face_detected, criminals) or
        match_with_db(face_detected, missing) or
        match_with_db(face_detected, vip)
    )

    if matched:
        print(f"[MATCH FOUND] {matched}")
    else:
        print("[ALERT] Unknown person detected!")
        location_address = get_location()
        send_email_alert(location_address)
        send_sms_alert(location_address)
        trigger_buzzer()

    cv2.imshow("Surveillance Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
