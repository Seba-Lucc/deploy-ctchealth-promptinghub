# backend/vapi_service.py

import os
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from vapi import Vapi


app = FastAPI()

# --- 1. CORS: permette richieste dal frontend Streamlit ---
origins = [
    "http://localhost:8501",          # sviluppo locale
    "https://share.streamlit.io",     # se usi Streamlit Community Cloud
    "https://<TUO-APP-STREAMLIT>.app" # il dominio definitivo
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# --- 2. Inizializza Vapi SDK ---
VAPI_KEY = os.getenv("VAPI_PRIVATE_KEY")
if not VAPI_KEY:
    raise RuntimeError("Imposta la variabile VAPI_PRIVATE_KEY!")
vapi = Vapi(api_key=VAPI_KEY)

# Memorizziamo in memoria l’assistant_id creato (durante l’esecuzione)
_assistant_id = None

@app.post("/create_assistant/")
def create_assistant():
    """
    Crea un nuovo assistant e ne restituisce l'ID.
    Viene chiamato dal frontend subito all'avvio o su pressione.
    """
    global _assistant_id
    if _assistant_id is None:
        name = f"CTC-Health-Assistant-{int(time.time())}"
        asst = vapi.assistants.create(
            transcriber={"provider":"deepgram","model":"nova-2","language":"it"},
            model={"messages":[{"role":"system","content":"Sei un assistente vocale CTC Health"}]},
            voice={"provider":"google","languageCode":"it-IT"}
        )
        _assistant_id = asst.id
    return {"assistant_id": _assistant_id}

@app.post("/process_voice/")
async def process_voice(
    audio: UploadFile = File(...),
    assistant_id: str = ""
):
    """
    Riceve un WAV, invia a Vapi, e ritorna trascrizione e risposta.
    """
    try:
        data = await audio.read()
        call = vapi.calls.create(assistant_id=assistant_id)
        call.send_audio(data)
        call.end()
        return {
            "transcript": call.transcription,
            "assistant_response": call.get_messages()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
