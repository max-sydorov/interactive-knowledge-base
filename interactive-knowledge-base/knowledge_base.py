import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

MODEL = "gpt-3.5-turbo"

# Load environment variables from .env file
load_dotenv()

# Define the base directory for the quick-loan-platform
BASE_DIR = Path(__file__).parent.parent / "quick-loan-platform"

# Define the vector store parent directory
VECTOR_STORE_DIR = str(Path(__file__).parent / "chroma_db")

# Define the file extensions to process
#FILE_EXTENSIONS = [".md", ".sql", ".java", ".tsx"]
FILE_EXTENSIONS = [".java"]

def load_documents() -> List[Document]:
    """
    Load documents from the quick-loan-platform directory with specified extensions.
    """
    documents = []

    # Define loaders for each file extension
    for ext in FILE_EXTENSIONS:
        # Skip the extension's leading dot for the glob pattern
        glob_pattern = f"**/*{ext}"

        # Create a loader for the current extension
        loader = DirectoryLoader(
            str(BASE_DIR),
            glob=glob_pattern,
            loader_cls=TextLoader,
            show_progress=True,
            use_multithreading=True
        )

        # Load documents with the current extension
        ext_documents = loader.load()
        print(f"Loaded {len(ext_documents)} documents with extension {ext}")
        documents.extend(ext_documents)

    return documents

def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks for better processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")

    return chunks

def create_vector_store(chunks: List[Document]) -> Chroma:
    """
    Create a vector store from document chunks using OpenAI embeddings.
    """
    # Initialize the embeddings model
    # Use specific parameters to avoid proxies validation error
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Delete if already exists
    if os.path.exists(VECTOR_STORE_DIR):
        Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings).delete_collection()

    # Create the vector store
    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=VECTOR_STORE_DIR)

    # Persist the vector store to disk
    vector_store.persist()
    print(f"Created vector store with {len(chunks)} chunks")

    return vector_store

def create_rag_chain(vector_store: Chroma):
    """
    Create a RAG chain that retrieves relevant documents and generates an answer.
    """
    # Initialize the retriever
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 25}
    )

    # Initialize the LLM
    llm = ChatOpenAI(
        model_name=MODEL,
        temperature=0
    )

    # Create the prompt template
    template = """
    You are an assistant for the Quick Loan Platform, a modern loan application platform built with Spring Boot and React.

    Answer the question based only on the following context:
    {context}

    Question: {question}

    If the answer cannot be determined from the context, say "I don't have enough information to answer this question."
    """

    prompt = ChatPromptTemplate.from_template(template)

    # Create the RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

def process_query(query: str, rag_chain) -> str:
    """
    Process a user query using the RAG chain.
    """
    return rag_chain.invoke(query)

def main():
    """
    Main function to initialize the knowledge base and provide a simple CLI.
    """
    print("Loading documents from quick-loan-platform...")
    documents = load_documents()

    # print("Chunking documents...")
    # chunks = chunk_documents(documents)

    print("Creating vector store...")
    vector_store = create_vector_store(documents)

    print("Creating RAG chain...")
    rag_chain = create_rag_chain(vector_store)

    print("\nInteractive Knowledge Base initialized!")
    print("You can now ask questions about the Quick Loan Platform.")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nEnter your question: ")

        if query.lower() == 'exit':
            break

        print("\nGenerating answer...")
        answer = process_query(query, rag_chain)
        print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()
