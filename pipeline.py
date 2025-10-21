from src.vectorstore import AnimeVectorStore
from src.dataloader import AnimeDataLoader
from src.recommender import AnimeRecommender
from config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommenderPipeline:
    def __init__(self, persist_directory: str = "chromadb_store", source_csv: str = None, processed_csv: str = None):
        try:
            logger.info("Initializing AnimeRecommenderPipeline")

            # If source_csv and processed_csv are provided, build the vectorstore
            if source_csv and processed_csv:
                logger.info(f"Building AnimeRecommenderPipeline with source_csv: {source_csv} and processed_csv: {processed_csv}")
                data_loader = AnimeDataLoader(source_csv=source_csv, processed_csv=processed_csv)
                processed_csv_path = data_loader.load_and_process()
                
                self.vectorstore = AnimeVectorStore(persist_directory=persist_directory, csv_file=processed_csv_path)
                self.vectorstore.build_and_save_vectorstore()
                logger.info(f"AnimeRecommenderPipeline built successfully with processed_csv: {processed_csv_path}")
            else:
                # Load existing vectorstore
                self.vectorstore = AnimeVectorStore(persist_directory=persist_directory, csv_file="")
            
            self.retriever = self.vectorstore.load_vectorstore().as_retriever()
            self.recommender = AnimeRecommender(retriever=self.retriever, api_key=GROQ_API_KEY, model_name=MODEL_NAME)

            logger.info("AnimeRecommenderPipeline initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AnimeRecommenderPipeline: {e}")
            raise CustomException(e)
    
    def recommend(self, question:str):
        try:
            logger.info(f"Recommending anime for question: {question}")
            recommendation = self.recommender.recommend(question)
            logger.info(f"Recommendation: {recommendation}")
            return recommendation
        except Exception as e:
            logger.error(f"Error recommending anime: {e}")
            raise CustomException(e)



if __name__ == "__main__":
    pipeline = AnimeRecommenderPipeline(source_csv="data/anime_data.csv", processed_csv="data/anime_processed.csv")
    

