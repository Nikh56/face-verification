import pickle
import os

DB_FILE = "embeddings.pkl"

def load_embeddings():
    """Load face embeddings from local storage."""
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    except Exception:
        return {}

def save_embedding(name, embedding):
    """Save a face embedding to local storage."""
    data = load_embeddings()
    data[name] = embedding
    with open(DB_FILE, "wb") as f:
        pickle.dump(data, f)
        
def clear_embeddings():
    """Clear all saved embeddings."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
