import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_openai import OpenAI
import argparse
import pytesseract

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configuration
JFK_URL = "https://www.archives.gov/research/jfk/release-2025"
PDF_DIR = "JFK_Files_2025"
TEXT_DIR = "JFK_Texts_2025"
INDEX_FILE = "jfk_faiss.index"
FILENAMES_FILE = "jfk_filenames.npy"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
API_KEY = os.getenv("OPENAI_API_KEY")

# Function: Download PDFs from the JFK release page
def download_pdfs():
    os.makedirs(PDF_DIR, exist_ok=True)
    response = requests.get(JFK_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    base_url = "https://www.archives.gov"
    pdf_links = [link["href"] for link in soup.find_all("a", href=True) if link["href"].endswith(".pdf")]
    for link in pdf_links:
        pdf_url = base_url + link
        pdf_name = link.split("/")[-1]
        pdf_path = os.path.join(PDF_DIR, pdf_name)
        if not os.path.exists(pdf_path):
            print(f"Downloading {pdf_name}...")
            pdf_response = requests.get(pdf_url)
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(pdf_response.content)

# Function: Extract text from PDFs (uses OCR if needed)
def extract_text():
    os.makedirs(TEXT_DIR, exist_ok=True)
    for pdf_file in os.listdir(PDF_DIR):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, pdf_file)
            text_path = os.path.join(TEXT_DIR, pdf_file.replace(".pdf", ".txt"))
            if not os.path.exists(text_path):
                print(f"Extracting text from {pdf_file}...")
                text = extract_text_from_pdf(pdf_path)
                with open(text_path, "w", encoding="utf-8") as text_file:
                    text_file.write(text)

# Function: Extract text from a single PDF, using OCR for image-based pages
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    print(f"Processing {pdf_path}...")
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")
        if page_text.strip():
            print(f"Page {page_num}: text extracted.")
            text += page_text
        else:
            print(f"Page {page_num}: no text found, performing OCR...")
            pix = page.get_pixmap()
            img_path = f"temp_page_{page_num}.png"
            pix.save(img_path)
            img_text = pytesseract.image_to_string(img_path)
            text += img_text
            os.remove(img_path)
    return text

# Function: Create a vector database from the extracted text files using FAISS
def create_vector_db():
    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = []
    file_names = []
    for file in os.listdir(TEXT_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(TEXT_DIR, file), "r", encoding="utf-8") as f:
                text = f.read()
                texts.append(text)
                file_names.append(file)
    embeddings = model.encode(texts)
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings))
    faiss.write_index(index, INDEX_FILE)
    np.save(FILENAMES_FILE, file_names)
    print("Vector database created!")

# Function: Ask a question and return a response with cited sources
def ask_question(question):
    model = SentenceTransformer(EMBEDDING_MODEL)
    index = faiss.read_index(INDEX_FILE)
    file_names = np.load(FILENAMES_FILE)
    query_embedding = model.encode([question])
    distances, indices = index.search(np.array(query_embedding), 5)
    results = []
    sources = []
    for idx in indices[0]:
        file_name = file_names[idx]
        sources.append(f"Source: {file_name}")
        with open(os.path.join(TEXT_DIR, file_name), "r", encoding="utf-8") as f:
            results.append(f.read())
    combined_text = " ".join(results)
    print("Context being sent for analysis (first 1000 characters):")
    print(combined_text[:1000])
    llm = OpenAI(api_key=API_KEY)
    response = llm.invoke(
        f"""You are an advanced research assistant with expert-level knowledge of historical events, intelligence analysis, and forensic investigation.

Context for analysis:
{combined_text}

Question:
{question}

Your response should:
- Provide a clear, evidence-based conclusion.
- Explain your reasoning step by step.
- Cite the documents used.
- If the answer is not found, respond with 'Not found in documents.'

Final Answer:""")
    source_text = "\n\nSources Used:\n" + "\n".join(sources)
    return response + source_text

# CLI Handling
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JFK Archive AI Terminal Interface")
    parser.add_argument("--download", action="store_true", help="Download all JFK PDFs")
    parser.add_argument("--extract", action="store_true", help="Extract text from downloaded PDFs")
    parser.add_argument("--index", action="store_true", help="Create a vector database from extracted texts")
    parser.add_argument("--ask", type=str, help="Ask a question about the JFK documents")
    args = parser.parse_args()

    if args.download:
        download_pdfs()
    elif args.extract:
        extract_text()
    elif args.index:
        create_vector_db()
    elif args.ask:
        answer = ask_question(args.ask)
        print("Answer:")
        print(answer)
    else:
        parser.print_help()
