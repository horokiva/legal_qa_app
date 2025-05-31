import pandas as pd
import re
import os

def split_into_paragraphs(csv_path="data/zakony_data.csv", output_path="data/law_paragraphs.csv"):
    df = pd.read_csv(csv_path)
    paragraphs = []

    for idx, row in df.iterrows():
        law_name = row.get('Název předpisu', f"Law_{idx}")
        full_text = row.get('Aktuální znění', '')

        split = re.split(r"(?=§\s?\d+[a-zA-Z]?)", full_text)

        for part in split:
            clean = part.strip()
            if clean:
                paragraphs.append({
                    "Law": law_name,
                    "Paragraph": clean
                })

    para_df = pd.DataFrame(paragraphs)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    para_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ Split into {len(para_df)} paragraphs. Saved to {output_path}")
    return para_df
