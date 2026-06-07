import os
import json
import logging
import argparse
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ingest")

def load_documents(data_dir: str):
    """Reads all .txt files from the data directory."""
    documents = []
    if not os.path.exists(data_dir):
        logger.info(f"Directory '{data_dir}' does not exist. Creating it.")
        os.makedirs(data_dir, exist_ok=True)
        return documents

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    documents.append({
                        "filename": filename,
                        "content": content
                    })
                    logger.info(f"Loaded document: {filename} ({len(content)} chars)")
            except Exception as e:
                logger.error(f"Error reading file {filename}: {e}")
    return documents

def get_embeddings(texts, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Computes vector embeddings for a list of texts using sentence-transformers
    or Hugging Face transformers with mean pooling as fallback.
    """
    logger.info(f"Computing embeddings for {len(texts)} texts using model: {model_name}")
    try:
        from sentence_transformers import SentenceTransformer
        logger.info("Using sentence-transformers library.")
        model = SentenceTransformer(model_name)
        embeddings = model.encode(texts)
        return np.array(embeddings, dtype=np.float32)
    except ImportError:
        logger.info("sentence-transformers not installed. Falling back to Hugging Face transformers and PyTorch.")
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
            
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            
            # Tokenize all texts
            encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
            
            with torch.no_grad():
                model_output = model(**encoded_input)
                
            # Perform mean pooling
            token_embeddings = model_output[0]
            attention_mask = encoded_input["attention_mask"]
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            embeddings = sum_embeddings / sum_mask
            
            # Normalize embeddings
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            return embeddings.cpu().numpy().astype(np.float32)
        except ImportError:
            logger.warning(
                "Neither 'sentence-transformers' nor 'transformers' is installed. "
                "Falling back to generating random mock embeddings (dim=384) for local testing."
            )
            # Generate random unit vectors as mock embeddings
            dimension = 384
            mock_embeddings = []
            for _ in texts:
                vec = np.random.randn(dimension)
                vec = vec / np.linalg.norm(vec)
                mock_embeddings.append(vec)
            return np.array(mock_embeddings, dtype=np.float32)
        except Exception as e:
            logger.critical(f"Unexpected error when generating embeddings: {e}")
            raise e

def main():
    parser = argparse.ArgumentParser(description="Ingest text documents into a Turbovec Index.")
    parser.add_argument("--data-dir", default="data", help="Directory containing source .txt files")
    parser.add_argument("--index-path", default="aceh_knowledge.tq", help="Output path for Turbovec index file")
    parser.add_argument("--mapping-path", default="aceh_knowledge_docs.json", help="Output path for document mapping JSON")
    args = parser.parse_args()

    # 1. Read documents
    documents = load_documents(args.data_dir)
    if not documents:
        logger.warning(
            f"No documents found in directory '{args.data_dir}'. "
            "Please place some .txt files in the directory and re-run."
        )
        return

    # 2. Compute Embeddings
    texts = [doc["content"] for doc in documents]
    try:
        embeddings = get_embeddings(texts)
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        return

    # 3. Add to Turbovec Index (384 dimensions, 4-bit compression)
    dimension = 384
    logger.info(f"Initializing Turbovec index with dim={dimension}, bit_width=4")
    try:
        from turbovec import TurboQuantIndex
        
        # Initialize the index
        index = TurboQuantIndex(dim=dimension, bit_width=4)
        
        # Add vectors to index
        logger.info(f"Ingesting {embeddings.shape[0]} vectors into Turbovec...")
        index.add(embeddings)
        
        # Save index to binary file
        index.write(args.index_path)
        logger.info(f"Saved Turbovec index to: {args.index_path}")
        
    except ImportError:
        logger.warning(
            "turbovec is not installed. Index file (.tq) will NOT be created. "
            "However, document mapping will still be generated."
        )
        # Mock/placeholder file creation for dry-run/testing purposes
        with open(args.index_path, "wb") as f:
            f.write(b"MOCK_TURBOVEC_INDEX_4BIT_COMPRESSED_DATA")
        logger.info(f"Saved mock Turbovec index to: {args.index_path}")
    except Exception as e:
        logger.error(f"Error during Turbovec index processing: {e}")
        return

    # 4. Save index mapping dictionary to JSON
    # Map index id (str) -> document text and source metadata
    mapping = {
        str(i): {
            "filename": doc["filename"],
            "content": doc["content"]
        }
        for i, doc in enumerate(documents)
    }

    try:
        with open(args.mapping_path, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved document mapping to: {args.mapping_path}")
    except Exception as e:
        logger.error(f"Error writing mapping JSON: {e}")

if __name__ == "__main__":
    main()
