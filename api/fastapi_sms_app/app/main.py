from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import the router from mobile.py
from .routers.mobile import router as mobile_router

app = FastAPI(
    title="FastAPI SMS Demo",
    description="Register & notify mobile numbers via Twilio using phone & token",
    version="1.0.0",
)

# Allow everything for development (change in production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the /mobile routes
app.include_router(mobile_router)

# Health check
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
