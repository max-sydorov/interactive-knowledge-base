# Interactive Knowledge Base for Quick Loan Platform

This project implements a Retrieval-Augmented Generation (RAG) system for the Quick Loan Platform. It allows users to ask questions about the platform and receive answers based on the content of the platform's documentation and source code.

## Features

- Reads content from `.md`, `.sql`, `.java`, and `.tsx` files in the Quick Loan Platform repository
- Converts the content into LangChain documents and chunks them for better processing
- Creates vector embeddings for each chunk using OpenAI embeddings
- Stores the embeddings in a Chroma vector database
- Provides a query interface that retrieves relevant chunks and generates answers using an LLM

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository (if you haven't already):
   ```bash
   git clone <repository-url>
   cd interactive-knowledge-base
   ```

2. Install the required dependencies:
   ```bash
   cd interactive-knowledge-base
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key by creating a `.env` file in the interactive-knowledge-base directory:
   ```bash
   cd interactive-knowledge-base
   echo "OPENAI_API_KEY=your-api-key" > .env
   ```
   Replace `your-api-key` with your actual OpenAI API key.

## Usage

1. Run the knowledge base script:
   ```bash
   cd interactive-knowledge-base
   python knowledge_base.py
   ```

2. The script will:
   - Load all `.md`, `.sql`, `.java`, and `.tsx` files from the Quick Loan Platform repository
   - Chunk the documents and create vector embeddings
   - Store the embeddings in a Chroma database
   - Start an interactive CLI where you can ask questions

3. Enter your questions about the Quick Loan Platform when prompted. Type 'exit' to quit.

## How It Works

1. **Document Loading**: The system loads all files with the specified extensions from the Quick Loan Platform repository.

2. **Document Chunking**: The loaded documents are split into smaller chunks to improve retrieval accuracy and to fit within the context window of the LLM.

3. **Vector Store Creation**: Each chunk is converted into a vector embedding using OpenAI's embedding model and stored in a Chroma vector database.

4. **Query Processing**: When a user asks a question:
   - The question is converted to a vector embedding
   - The most similar chunks are retrieved from the vector store
   - The relevant chunks and the question are sent to the LLM
   - The LLM generates an answer based on the provided context

## Example Questions

- "What technologies are used in the Quick Loan Platform?"
- "How is the database schema structured?"
- "What are the main components of the frontend?"
- "How does the loan application process work?"

## Customization

You can modify the `knowledge_base.py` script to:
- Change the chunk size and overlap
- Use a different embedding model
- Adjust the number of chunks retrieved for each query
- Modify the prompt template for the LLM
