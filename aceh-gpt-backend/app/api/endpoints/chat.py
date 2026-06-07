import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.rag import rag_service

logger = logging.getLogger("aceh-gpt-backend.chat_api")

router = APIRouter()

class ChatRequest(BaseModel):
    # Input validation conforming to secure coding guidelines: Limit the length of input
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Pertanyaan atau pesan yang diajukan oleh pengguna."
    )

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Jawaban yang dihasilkan oleh RAG Chatbot.")

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint utama untuk tanya jawab RAG Chatbot.
    Melakukan pencarian ke Turbovec database dan menghasilkan jawaban terkontekstualisasi.
    """
    try:
        logger.info(f"Processing chat request with message length: {len(request.message)}")
        answer = await rag_service.generate_response(request.message)
        return ChatResponse(answer=answer)
    except Exception as e:
        # Conforming to secure coding guidelines: Log diagnostic details internally, return generic error.
        logger.error(f"Error occurred in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan pada sistem backend. Silakan coba beberapa saat lagi."
        )
