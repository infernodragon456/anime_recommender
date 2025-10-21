import pandas as pd

class AnimeDataLoader:
    def __init__(self, source_csv: str, processed_csv: str) -> None:
        self.source_csv = source_csv
        self.processed_csv = processed_csv
        pass

    def load_and_process(self):
        df = pd.read_csv(self.source_csv, encoding='utf-8', on_bad_lines='skip')
        df.dropna(inplace=True)
        
        cols = {"title", "num_episodes", "mean", "popularity", "genres", "studios", "synopsis"}
        missing = cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df["combined_info"] = ("Title: " + df["title"] + ", Overview: " + df["synopsis"] + ", Genres: " + df["genres"] + ", Rating: " + df["mean"].astype(str) + ", Duration: " + df["num_episodes"].astype(str) + ", Popularity: " + df["popularity"].astype(str) + ", Made By: " + df["studios"])
        
        df[['combined_info']].to_csv(self.processed_csv , index=False,encoding='utf-8')
        return self.processed_csv
    