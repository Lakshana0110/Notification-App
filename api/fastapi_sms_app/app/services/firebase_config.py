import firebase_admin
from firebase_admin import credentials, messaging
import os

# Path to your service account key
# cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), '../../serviceAccountKey.json'))
# cred = credentials.Certificate((os.path.dirname(__file__), '../../../serviceAccountKey.json'))
cred = credentials.Certificate('E:/notificationproject/notification/serviceAccountKey.json')

firebase_app = firebase_admin.initialize_app(cred)

def send_push_notification(token: str, title: str, body: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )
    response = messaging.send(message)
    return response
