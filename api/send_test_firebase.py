import firebase_admin
from firebase_admin import credentials, messaging
import os

# Path to your Firebase key
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Replace with real device token
test_token = "YOUR_REAL_DEVICE_FCM_TOKEN_HERE"

message = messaging.Message(
    notification=messaging.Notification(
        title="🔥 Test Title",
        body="✅ Test message from Firebase"
    ),
    token=test_token,
)

try:
    response = messaging.send(message)
    print("Successfully sent message:", response)
except Exception as e:
    print("❌ Error sending message:", e)
