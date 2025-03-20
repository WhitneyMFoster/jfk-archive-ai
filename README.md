# JFK Archive AI Terminal Interface

This project allows you to download, extract, and analyze JFK assassination records from the National Archives website, then query the data using an AI assistant powered by OpenAI.

## Features

- **Download PDFs:** Automatically download PDFs from the JFK Records release page.
- **Extract Text:** Extract text from the downloaded PDFs. Uses OCR (via Tesseract) if the PDF pages are image-based.
- **Create Vector Database:** Generate embeddings for the extracted text and build a FAISS index for efficient search.
- **Ask Questions:** Query the indexed documents using OpenAI's GPT model to receive evidence-based answers, with sources cited.

## Prerequisites

- OpenAI API key (available from [OpenAI](https://platform.openai.com/account/api-keys))
- Python 3.8 or later

## Installation and Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
    cd YOUR_REPO
    ```

2. **Set up the virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```

4. **Install dependencies:**
    ```bash
    python3 setup.py
    ```

5. **Set your OpenAI API key as an environment variable:**
    ```bash
    export OPENAI_API_KEY="your_api_key" 
    ```

## Usage

The script  accepts the following arguments:

- `--download`: Download JFK PDFs
- `--extract`: Extract text from PDFs
- `--index`: Create the vector database
- `--ask <question>`: Ask a question and get a response from the AI assistant

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License - see the [LICENSE](LICENSE) file for details.

You are free to share and adapt the material, provided you attribute the author and do not use it for commercial purposes.

## Curious and Lazy?

I went ahead and asked a few of the top questions. [Check it out](TLDR.md)
