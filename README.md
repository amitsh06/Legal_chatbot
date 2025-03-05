# Gen AI Legal Chatbot

## Project Description

This project implements a multi-agent chatbot designed to provide concise and easy-to-understand summaries of legal information. The chatbot leverages two main agents:

*   **Query Agent:**  Fetches relevant sections from legal documents based on user queries.
*   **Summarization Agent:** Extracts key explanations from complex legal topics and converts lengthy legal text into plain, easy-to-understand language while preserving accuracy.

The chatbot is designed to be used with legal documents such as:

*   **Guide to Litigation in India:** (Provides an overview of litigation procedures in India)
*   **Legal Compliance & Corporate Laws by ICAI:** (Covers corporate and taxation laws)

This project was developed as part of a Gen AI Engineer Assignment to showcase coding skills in building a practical AI application.

## Technologies Used

*   **Python:** Programming language
*   **Flask:** Web framework for creating the user interface
*   **PyPDF2:** Library for reading PDF documents
*   **Sentence Transformers:** Library for generating sentence embeddings for semantic search
*   **LangChain:** Library for text splitting and document processing
*   **Hugging Face Transformers:** Library for pre-trained summarization model (`facebook/bart-large-cnn`)
*   **Gunicorn:** WSGI HTTP server for production deployment

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/amitsh06/Legal_chatbot
    cd legal_chatbot
    ```
    
2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Linux/macOS
    venv\Scripts\activate    # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Place PDF data:**
    *   Create a folder named `data` in the project root directory.
    *   Place your PDF documents (e.g., `Guide_to_Litigation_in_India.pdf`, `Legal_Compliance_ICAI.pdf`) inside the `data` folder. **Ensure the filenames in `app.py` match your PDF filenames.**

## Running the Chatbot Locally

To run the chatbot on your local machine:

1.  **Navigate to the project root directory** in your terminal.
2.  **Make sure your virtual environment is activated.**
3.  **Run the Flask application:**

    ```bash
    python app.py
    ```

4.  **Open your web browser** and go to `http://127.0.0.1:5000/`.
5.  **Start using the chatbot!** Enter legal queries in the text area and click "Submit".

## Project Structure


*   **`data/`:**  Contains the legal PDF documents used as data sources.
*   **`templates/`:** Contains the `index.html` file for the chatbot's web interface.
*   **`app.py`:** The main Flask application file that handles routing, user queries, and orchestrates the Query and Summarization Agents.
*   **`utils.py`:**  Contains utility functions for reading PDFs, chunking text, creating embeddings, finding relevant chunks, and summarizing text.
*   **`walkthrough.md`:**  Detailed walkthrough document explaining the project architecture, code, demo, challenges, and improvements.
*   **`README.md`:**  This file, providing a general overview of the project.
*   **`requirements.txt`:**  Lists all Python library dependencies required to run the project.
*   **`Procfile`:**  Specifies the process type and command for Heroku to run the web application.
*   **`runtime.txt`:**  Specifies the Python runtime version for Heroku.
*   **.gitignore:** Specifies intentionally untracked files that Git should ignore (e.g., `venv/`, `_pycache_/`).

## Demo

Example queries and responses are provided in the [walkthrough.md](walkthrough.md) document, along with screenshots of the chatbot in action.

## Walkthrough Document

For a detailed explanation of the project architecture, code implementation, demo, challenges faced, and possible improvements, please refer to the [walkthrough.md](walkthrough.md) file.


## Author

*  **Amit Sharma**
*  **https://github.com/amitsh06**

---

*This README.md file was generated for the Gen AI Legal Chatbot project.*
