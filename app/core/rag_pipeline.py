from sentence_transformers import SentenceTransformer, util

# Model ek hi baar load hoga (thoda time lagega pehli baar)
model = SentenceTransformer('all-MiniLM-L6-v2')

def answer_question(text, question):
    """
    Contract ke text ko paragraphs mein todta hai,
    phir sawal se sabse zyada milta julta paragraph dhoondta hai.
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip() and len(p.strip()) > 20]

    if not paragraphs:
        return {"answer": "No content found in document.", "confidence": 0}

    # Har paragraph aur sawal ko "embedding" (number form) mein convert karna
    paragraph_embeddings = model.encode(paragraphs, convert_to_tensor=True)
    question_embedding = model.encode(question, convert_to_tensor=True)

    # Similarity (kitna milta julta hai) calculate karna
    similarities = util.cos_sim(question_embedding, paragraph_embeddings)[0]

    # Sabse zyada milta julta paragraph dhoondna
    best_idx = similarities.argmax().item()
    best_score = similarities[best_idx].item()

    return {
        "answer": paragraphs[best_idx],
        "confidence": round(best_score, 2)
    }