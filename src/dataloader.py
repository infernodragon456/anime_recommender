import pandas as pd

class AnimeDataLoader:
    def __init__(self, source_csv: str, processed_csv: str) -> None:
        self.source_csv = source_csv
        self.processed_csv = processed_csv
        pass

    def load_and_process(self):
        df = pd.read_csv(self.source_csv, encoding='utf-8', error_bad_lines=False)
        df.dropna(inplace=True)
        
        cols = {"title", "num_episodes", "mean", "popularity", "genres", "studios", "synopsis"}
        missing = cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df["combined_info"] = ("Title: " + df["title"] + ", Overview: " + df["synopsis"] + ", Genres: " + df["genres"] + ", Rating: " + df["mean"] + ", Duration: " + df["num_episodes"] + ", Popularity: " + df["popularity"] + ", Made By: " + df["studios"])
        
        df[['combined_info']].to_csv(self.processed_csv , index=False,encoding='utf-8')
        return self.processed_csv
    