from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

class AnimeVectorStore:
    def __init__(self, csv_file: str, persist_directory: str = "chromadb_store"):
        self.csv_file = csv_file
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
    def build_and_save_vectorstore(self):
        loader = CSVLoader(file_path=self.csv_file, encoding="utf-8", metadata_columns = [])

        data = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(data)

        db = Chroma.from_documents(texts, self.embeddings, persist_directory=self.persist_directory)
        db.persist()

    def load_vectorstore(self):
        return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        
    