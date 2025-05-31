from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
df = pd.read_csv("data/law_paragraphs.csv")

# Generate embeddings
df["embedding"] = df["Paragraph"].apply(lambda x: model.encode(x).tolist())

# Save for search
df.to_json("data/law_paragraphs_embedded.json", orient="records", lines=True)
