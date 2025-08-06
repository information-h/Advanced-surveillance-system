# Surveillance Project

## Setup Instructions

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Setup MySQL Database:
- Run `database.sql` in your MySQL server.

3. Add your images in the `images/` folder accordingly.

4. Update `main.py` with your MySQL password, Gmail credentials, and Twilio credentials.

5. Run the main program:
```
python main.py
```

## Features
- Face recognition using DeepFace
- Matches against criminals, missing persons, and VIPs
- Sends Email and SMS alerts on unknown person detection
- Optional buzzer trigger (for Raspberry Pi)
