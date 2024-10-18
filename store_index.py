# Import necessary libraries
from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Pinecone API key and environment from environment variables
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')

# Load PDF data and create text chunks
extracted_data = load_pdf("data/")  # Adjust the path to your PDF file directory
text_chunks = text_split(extracted_data)

# Download embeddings (Hugging Face embeddings in this case)
embeddings = download_hugging_face_embeddings()

# Initialize Pinecone client
pc = Pinecone(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)

# Define the index name
index_name = "medical-bot"

# Check if the index exists and handle it
try:
    # List existing indexes
    existing_indexes = pc.list_indexes().names()

    if index_name in existing_indexes:
        print(f"Index '{index_name}' already exists. Deleting and recreating with the correct dimension.")
        pc.delete_index(index_name)  # Delete existing index if necessary
    else:
        print(f"Index '{index_name}' does not exist. Creating it now...")

    # Recreate the index with dimension 384 (for sentence-transformers/all-MiniLM-L6-v2 embeddings)
    pc.create_index(
        name=index_name,
        dimension=384,  # Match the dimension of your embeddings
        metric='cosine',  # Change based on your requirements (e.g., 'euclidean')
        spec=ServerlessSpec(
            cloud='aws', 
            region=PINECONE_API_ENV
        )
    )
    print(f"Index '{index_name}' created successfully with dimension 384.")
except Exception as e:
    print(f"Error checking or creating index: {e}")

