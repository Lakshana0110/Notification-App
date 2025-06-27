import os
from pathlib import Path
from dotenv import load_dotenv
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv(dotenv_path="E:/notificationproject/notification/api/fastapi_sms_app/env.example")


# Load .env from the correct absolute path
env_path = Path(__file__).resolve().parent.parent / "env.example"
load_dotenv(dotenv_path=env_path)

class SMSService:
    def __init__(self):
        self.client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"),
            os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.from_number = os.getenv("TWILIO_FROM_NUMBER")
        if not self.from_number:
            raise RuntimeError("Missing TWILIO_FROM_NUMBER in env.example")

    def send_sms(self, to_number: str, body: str) -> str:
        message = self.client.messages.create(
            body=body,
            from_=self.from_number,
            to=to_number
        )
        return message.sid
print("FROM:", os.getenv("TWILIO_FROM_NUMBER"))
