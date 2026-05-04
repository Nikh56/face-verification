from deepface import DeepFace
import numpy as np

def get_embedding(image_array):
    """
    Extracts face embedding from an RGB numpy array using DeepFace.
    Returns embedding (numpy array) or None if no face found.
    """
    try:
        # DeepFace expects BGR format when passing numpy arrays directly (OpenCV default)
        # The input image_array is RGB from PIL, so we convert it to BGR
        image_bgr = image_array[:, :, ::-1]
        
        # enforce_detection=True will raise ValueError if no face is found
        # We use Facenet model which is lightweight and accurate
        result = DeepFace.represent(img_path=image_bgr, model_name="Facenet", enforce_detection=True)
        
        if result and len(result) > 0:
            return np.array(result[0]["embedding"])
        return None
    except Exception as e:
        # Usually triggered when no face is detected
        return None

def compare_embeddings(target_embedding, stored_embeddings, threshold=0.6):
    """
    Compare target against stored embeddings using Cosine Similarity.
    Returns (best_match_name, confidence_score) or (None, 0.0)
    """
    if not stored_embeddings:
        return None, 0.0
        
    best_match_name = None
    best_similarity = -1
    
    # Normalize target embedding for Cosine Similarity
    target_norm = target_embedding / np.linalg.norm(target_embedding)
    
    for name, stored_emb in stored_embeddings.items():
        stored_emb = np.array(stored_emb)
        stored_norm = stored_emb / np.linalg.norm(stored_emb)
        
        # Calculate cosine similarity (value between -1 and 1)
        similarity = np.dot(target_norm, stored_norm)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_name = name
            
    # For Facenet, a cosine similarity > 0.6 is a good match indicator.
    if best_similarity >= threshold:
        # Calculate a percentage confidence mapped from threshold to 1.0
        confidence = ((best_similarity - threshold) / (1.0 - threshold)) * 100
        # Cap at 100% and floor at 0%
        confidence = max(0.0, min(100.0, confidence))
        return best_match_name, confidence
        
    return None, 0.0
