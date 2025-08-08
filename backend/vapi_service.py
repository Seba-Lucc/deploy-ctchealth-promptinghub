# backend/vapi_service.py

import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import corretto per vapi-server-sdk
try:
    from vapi_server_sdk import Vapi
except ImportError:
    # Fallback se il nome del modulo è diverso
    try:
        from vapi import Vapi
    except ImportError:
        raise RuntimeError("Impossibile importare Vapi SDK. Verifica l'installazione.")

load_dotenv()

app = FastAPI()

# CORS configuration - permette richieste dal frontend Streamlit
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
    print("⚠️ WARNING: VAPI_PRIVATE_KEY non configurata! Il servizio potrebbe non funzionare.")
    # Non sollevare errore per permettere il deploy
else:
    print(f"✅ VAPI_PRIVATE_KEY configurata correttamente")

# Inizializza il client Vapi solo se la chiave è presente
vapi_client = None
if VAPI_KEY:
    try:
        vapi_client = Vapi(token=VAPI_KEY)
        print("✅ Vapi client inizializzato con successo")
    except Exception as e:
        print(f"❌ Errore nell'inizializzazione del client Vapi: {e}")

class CreateAssistantRequest(BaseModel):
    name: str
    system_prompt: str

@app.get("/")
async def root():
    """Root endpoint per verificare che il server sia online"""
    return {
        "status": "online",
        "service": "Vapi Assistant Creator",
        "vapi_configured": vapi_client is not None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "vapi_configured": vapi_client is not None,
        "timestamp": time.time()
    }

@app.post("/create_assistant/")
async def create_assistant(request: CreateAssistantRequest):
    """
    Crea un nuovo assistente Vapi con il system prompt fornito.
    """
    if not vapi_client:
        raise HTTPException(
            status_code=503, 
            detail="Vapi client non configurato. Verifica VAPI_PRIVATE_KEY."
        )
    
    try:
        print(f"📞 Creazione assistente: {request.name}")
        
        # Configurazione dell'assistente
        assistant_config = {
            "name": request.name,
            "model": {
                "provider": "openai",
                "model": "gpt-4o",
                "temperature": 0.7,
                "messages": [{
                    "role": "system",
                    "content": request.system_prompt
                }]
            },
            "voice": {
                "provider": "11labs",
                "voiceId": "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
            },
            "transcriber": {
                "provider": "deepgram",
                "model": "nova-2",
                "language": "en"
            }
        }
        
        # Aggiungi il first message solo se non è vuoto
        if request.system_prompt:
            assistant_config["firstMessage"] = "Hello, I'm ready to start our role-play session."
        
        # Crea l'assistente
        assistant = vapi_client.assistants.create(**assistant_config)
        
        print(f"✅ Assistente creato con successo: {assistant.id}")
        
        return {
            "assistant_id": assistant.id,
            "status": "success",
            "name": request.name
        }
    
    except Exception as e:
        print(f"❌ Errore nella creazione dell'assistente: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Errore nella creazione dell'assistente: {str(e)}"
        )

@app.post("/test_vapi/")
async def test_vapi_connection():
    """
    Endpoint di test per verificare la connessione con Vapi
    """
    if not vapi_client:
        return {
            "status": "error",
            "message": "Vapi client non configurato"
        }
    
    try:
        # Prova a recuperare la lista degli assistenti come test
        assistants = vapi_client.assistants.list(limit=1)
        return {
            "status": "success",
            "message": "Connessione a Vapi funzionante",
            "test_passed": True
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Errore di connessione: {str(e)}",
            "test_passed": False
        }

# Aggiungi un log all'avvio
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)