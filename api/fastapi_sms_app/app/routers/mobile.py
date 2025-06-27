import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, constr

from ..services.sms_service import SMSService
from ..services.firebase_config import send_push_notification

# 🔧 APIRouter setup
router = APIRouter(prefix="/mobile", tags=["mobile"])

# 🔒 Phone number validation pattern
PhoneStr = constr(pattern=r"^\+[1-9]\d{9,14}$")  # E.164 format

# 🗃️ JSON file path
DATA_FILE = Path(__file__).resolve().parent.parent.parent / "mobile_numbers.json"

# 📲 SMS service instance
sms_service = SMSService()

# 📥 Input schema for phone and token
class MobileIn(BaseModel):
    phone: PhoneStr
    mobile_token: constr(strip_whitespace=True, min_length=6) = Field(...)

# 🔐 Firebase message schema
class FirebaseRequest(BaseModel):
    mobile_number: str
    mobile_token: str
    title: str
    message: str

# 🔄 Load all records from file
def _load_numbers() -> list[dict[str, str]]:
    if not DATA_FILE.exists():
        return []
    try:
        data: Any = json.loads(DATA_FILE.read_text())
        return [
            item for item in data
            if isinstance(item, dict)
            and "phone" in item
            and "mobile_token" in item
        ]
    except json.JSONDecodeError:
        return []

# 💾 Save unique record
def _save_number(phone: str, token: str) -> None:
    numbers = _load_numbers()
    if any(rec["phone"] == phone or rec["mobile_token"] == token for rec in numbers):
        return
    numbers.append({"phone": phone, "mobile_token": token})
    DATA_FILE.write_text(json.dumps(numbers, indent=2))

# ✅ Register mobile API
@router.post("/register", status_code=201)
async def register_mobile(payload: MobileIn):
    _save_number(payload.phone, payload.mobile_token)
    return {
        "status": "stored",
        "phone": payload.phone,
        "mobile_token": payload.mobile_token,
    }

# 📤 Send SMS via Twilio
@router.post("/notify")
async def notify_mobile(payload: MobileIn, message: str = "Hello from FastAPI 🎉"):
    try:
        sid = sms_service.send_sms(payload.phone, message)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"status": "sent", "sid": sid}

# 🔔 Send Firebase push notification
@router.post("/send_firebase_message")
def send_firebase_message(data: FirebaseRequest):
    try:
        res = send_push_notification(
            token=data.mobile_token,
            title=data.title,
            body=data.message
        )
        return {"status": "success", "firebase_response": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# ---------------------------------------------------------------------
@router.get("/test_push", tags=["mobile"])
def test_push(token: str, title: str = "Test", body: str = "Hello from FastAPI"):
    """
    Quickly trigger Firebase push from Swagger UI or curl
    without crafting a JSON payload.
    """
    try:
        res = send_push_notification(token=token, title=title, body=body)
        return {"status": "success", "firebase_response": res}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
