# app.py
from flask import Flask, request, jsonify, render_template
from utils import read_pdf, chunk_text, create_embeddings, find_relevant_chunks, summarize_text
import os
from sentence_transformers import SentenceTransformer, util  # <---- ADD THIS LINE

app = Flask(__name__)

# --- Load Data and Create Embeddings (This happens once, when the app starts) ---

data_dir = os.path.join(os.path.dirname(__file__), 'data')

# Load Litigation PDF
litigation_pdf_path = os.path.join(data_dir, "your_litigation_pdf.pdf")  # Your actual file name
litigation_text = read_pdf(litigation_pdf_path)
if litigation_text:
    litigation_chunks = chunk_text(litigation_text)
    litigation_embeddings, litigation_model = create_embeddings(litigation_chunks)
else:
    litigation_embeddings, litigation_model = None, None
    print("Error: Litigation PDF loading failed.")

# Load ICAI PDF
icai_pdf_path = os.path.join(data_dir, "your_icai_pdf.pdf")  # Your actual file name
icai_text = read_pdf(icai_pdf_path)
if icai_text:
    icai_chunks = chunk_text(icai_text)
    icai_embeddings, icai_model = create_embeddings(icai_chunks)
else:
    icai_embeddings, icai_model = None, None
    print("Error: ICAI PDF loading failed.")

print("Embeddings created and loaded successfully!")

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query']

    all_relevant_chunks = []

    if litigation_embeddings is not None and litigation_model is not None:
        relevant_litigation_chunks = find_relevant_chunks(
            user_query, litigation_embeddings, litigation_model, litigation_chunks
        )
        all_relevant_chunks.extend(relevant_litigation_chunks)

    if icai_embeddings is not None and icai_model is not None:
        relevant_icai_chunks = find_relevant_chunks(
            user_query, icai_embeddings, icai_model, icai_chunks
        )
        all_relevant_chunks.extend(relevant_icai_chunks)

    # --- (Optional) Better Chunk Combination - Use this block if you want sorted chunks ---
    # Create a list of (chunk, score) tuples
    all_chunks_with_scores = []

    if litigation_embeddings is not None and litigation_model is not None:
        query_embedding = litigation_model.encode(user_query)  # Encode query once
        litigation_similarities = util.cos_sim(query_embedding, litigation_embeddings)[0]
        top_litigation_indices = litigation_similarities.argsort(descending=True)[:5]  # Get top 5
        for i in top_litigation_indices:
            all_chunks_with_scores.append((litigation_chunks[i], litigation_similarities[i].item()))

    if icai_embeddings is not None and icai_model is not None:
        query_embedding = icai_model.encode(user_query)  # Encode query once
        icai_similarities = util.cos_sim(query_embedding, icai_embeddings)[0]
        top_icai_indices = icai_similarities.argsort(descending=True)[:5]  # Get top 5
        for i in top_icai_indices:
            all_chunks_with_scores.append((icai_chunks[i], icai_similarities[i].item()))

    # Sort by score in descending order
    all_chunks_with_scores.sort(key=lambda x: x[1], reverse=True)

    # Extract just the chunks (we don't need the scores anymore)
    sorted_chunks = [chunk for chunk, score in all_chunks_with_scores]
    combined_text = " ".join(sorted_chunks)

    # --- (End of Optional Block) ---

    # --- If you are NOT using the optional block, use this line instead: ---
    # combined_text = " ".join(all_relevant_chunks)

    if combined_text:
        if len(combined_text) < 20:  # Check length
            return jsonify({'result': 'Relevant information is too short to summarize.'})
        summary = summarize_text(combined_text)
        return jsonify({'result': summary})
    else:
        return jsonify({'result': 'No relevant information found.'})

if __name__ == '__main__':
    app.run(debug=True)