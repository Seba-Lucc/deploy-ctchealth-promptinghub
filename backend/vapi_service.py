# backend/vapi_service.py

import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vapi_server_sdk import Vapi

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione, specifica solo i domini necessari
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Vapi
VAPI_KEY = os.getenv("VAPI_PRIVATE_KEY")
if not VAPI_KEY:
    raise RuntimeError("VAPI_PRIVATE_KEY non configurata!")

vapi_client = Vapi(token=VAPI_KEY)

class CreateAssistantRequest(BaseModel):
    name: str
    system_prompt: str

@app.post("/create_assistant/")
async def create_assistant(request: CreateAssistantRequest):
    """
    Crea un nuovo assistente Vapi con il system prompt fornito.
    """
    try:
        assistant = vapi_client.assistants.create(
            name=request.name,
            model={
                "provider": "openai",
                "model": "gpt-4o",
                "temperature": 0.7,
                "messages": [{
                    "role": "system",
                    "content": request.system_prompt
                }]
            },
            voice={
                "provider": "11labs",
                "voiceId": "21m00Tcm4TlvDq8ikWAM"
            },
            transcriber={
                "provider": "deepgram",
                "model": "nova-2",
                "language": "en"
            },
            firstMessage="Hello, I'm ready to start our role-play session."
        )
        
        return {"assistant_id": assistant.id, "status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}