from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_groq import ChatGroq
from src.prompt import get_prompt

class AnimeRecommender:
    def __init__(self, retriever, api_key:str, model_name:str):
        self.llm = ChatGroq(api_key=api_key, model_name=model_name, temperature=0.1)
        self.retriever = retriever
        
        prompt_template = get_prompt()
        
        self.question_answer_chain = create_stuff_documents_chain(self.llm, prompt_template)
        
        self.chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    def recommend(self, question: str):
        result = self.chain.invoke({"input": question})
        return result["answer"]
