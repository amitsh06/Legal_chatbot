import PyPDF2
from sentence_transformers import SentenceTransformer, util
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline  # Import for summarization


def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return text


def chunk_text(text, chunk_size=500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def create_embeddings(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    return embeddings, model


def find_relevant_chunks(query, embeddings, model, chunks, top_n=5):
    query_embedding = model.encode(query)
    similarities = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:top_n]
    relevant_chunks = [chunks[i] for i in top_indices]
    return relevant_chunks


def summarize_text(text, max_length=150, min_length=50):
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return summary
    except KeyError as e:
        print(f"KeyError during summarization: {e}.  Check model output format.")
        return "Error: Could not extract summary.  Model output might have changed."
    except RuntimeError as e:
        print(f"RuntimeError during summarization: {e}.  This might be a CUDA issue.")
        return "Error: A runtime error occurred.  This could be related to GPU memory."
    except Exception as e:
        print(f"An unexpected error occurred during summarization: {e}")
        return "Error during summarization."

# Example Usage (Optional - you can comment this out or remove it for the final submission)
if __name__ == "__main__":
    # Replace with your actual PDF file names
    litigation_text = read_pdf("data/your_litigation_pdf.pdf")
    icai_text = read_pdf("data/your_icai_pdf.pdf")

    if litigation_text:
      litigation_chunks = chunk_text(litigation_text)
      litigation_embeddings, litigation_model = create_embeddings(litigation_chunks)
      print(f"Litigation PDF - Number of Chunks: {len(litigation_chunks)}")

      query = "steps involved in filing a lawsuit"
      relevant_chunks = find_relevant_chunks(query, litigation_embeddings, litigation_model, litigation_chunks)

      print(f"\nRelevant Chunks for '{query}':")
      for chunk in relevant_chunks:
          print(chunk)

    if icai_text:
        icai_chunks = chunk_text(icai_text)
        icai_embeddings, icai_model = create_embeddings(icai_chunks)
        print(f"\nICAI PDF - Number of Chunks: {len(icai_chunks)}")

        query = "taxation laws in India"
        relevant_chunks = find_relevant_chunks(query, icai_embeddings, icai_model, icai_chunks)

        print(f"\nRelevant Chunks for '{query}':")
        for chunk in relevant_chunks:
            print(chunk)