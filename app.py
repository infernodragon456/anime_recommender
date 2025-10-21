import streamlit as st
from pipeline import AnimeRecommenderPipeline
from dotenv import load_dotenv


st.set_page_config(page_title="Anime Recommender", page_icon=":tv:", layout="centered")

load_dotenv()

@st.cache_resource
def init_pipeline():
    return AnimeRecommenderPipeline()

pipeline = init_pipeline()

st.title("Anime Recommender")
query = st.text_input("Enter preferences to get anime suggestions!")

if query:
    with st.spinner("Generating recommendations..."):
        response = pipeline.recommend(query)
        st.markdown("### Recommendations:")
        st.write(response)