import logging
from typing import List
from app.config import settings
from app.services.vector_db import vector_db_service

logger = logging.getLogger("aceh-gpt-backend.rag")

class RAGService:
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.embedding_model_name = settings.EMBEDDING_MODEL
        self.tokenizer = None
        self.model = None
        self.embedding_model = None
        self._load_models()

    def _load_models(self):
        """Lazy load Hugging Face models for embedding and response generation."""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            logger.info(f"Loading tokenizer and model: {self.model_name}")
            # Ensure model loading handles hardware acceleration (e.g., CUDA or CPU) safely
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            # Note: We keep the direct loading commented out in boilerplate to avoid slow startup and massive downloads during testing.
            # self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            # self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)
            logger.info(f"Models configuration checked on device: {self.device}")
        except ImportError:
            logger.warning("transformers or torch libraries are not installed. Running in mock mode.")
        except Exception as e:
            logger.warning(f"Could not load Hugging Face models: {e}. Running in mockup mode.")

    async def get_embedding(self, text: str) -> List[float]:
        """Generate vector embedding for the input text."""
        try:
            import numpy as np
            # Mocking embedding generation with a random unit vector for placeholder testing
            dimension = 384  # Standard dimensions for sentence transformers
            vector = np.random.randn(dimension)
            vector = vector / np.linalg.norm(vector)
            return vector.tolist()
        except ImportError:
            logger.warning("numpy is not installed. Returning standard zero embedding vector.")
            return [0.0] * 384
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return [0.0] * 384

    async def generate_response(self, query: str) -> str:
        """Standard RAG pipeline: Query Vector DB -> Construct Prompt -> Generate Answer."""
        # 1. Retrieve query embedding
        query_vector = await self.get_embedding(query)
        
        # 2. Retrieve relevant context from vector database
        context_docs = await vector_db_service.search(query_vector, top_k=3)
        context_text = "\n".join([doc["document"] for doc in context_docs]) if context_docs else "Tidak ada dokumen pendukung."
        
        logger.info(f"Retrieved context size: {len(context_text)}")
        
        # 3. Construct prompt
        # In actual deployment, this prompt is sent to the LLM (Transformers / OpenAI / Hugging Face model).
        prompt = (
            f"Gunakan informasi berikut untuk menjawab pertanyaan pengguna tentang Aceh.\n"
            f"Informasi Pendukung:\n{context_text}\n\n"
            f"Pertanyaan: {query}\n"
            f"Jawaban:"
        )
        
        # 4. Generate answer using LLM
        # For boilerplate/mock validation:
        response = (
            f"[RAG Response] Terima kasih atas pertanyaannya.\n"
            f"Pertanyaan Anda: '{query}'\n"
            f"Informasi Referensi dari Turbovec: '{context_text}'"
        )
        return response

rag_service = RAGService()
