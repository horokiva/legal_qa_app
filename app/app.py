import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import openai

# Global API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable")

openai.api_key = OPENAI_API_KEY

# Load embedding model
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Load data with precomputed embeddings
df = pd.read_pickle("../data/laws_with_embeddings.pkl")
embeddings = np.vstack(df["embedding"].apply(np.array))

# Init GUI
root = tk.Tk()
root.title("Legal QA App")
root.geometry("900x600")

# UI Variables
query_var = tk.StringVar()
top_paragraph = ""
last_explanation = ""

# UI Elements
tk.Label(root, text="Zadejte právní dotaz:", font=("Arial", 14)).pack(pady=10)
query_entry = tk.Entry(root, textvariable=query_var, font=("Arial", 12), width=80)
query_entry.pack(pady=5)

result_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 11))
result_box.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

def run_query():
    global top_paragraph, last_explanation
    query = query_var.get()
    if not query.strip():
        return

    query_vec = model.encode([query])
    scores = cosine_similarity(query_vec, embeddings)[0]
    df["score"] = scores
    top = df.sort_values("score", ascending=False).head(5)

    result_box.delete(1.0, tk.END)
    last_explanation = ""
    for _, row in top.iterrows():
        result_box.insert(tk.END, f"📘 Zákon: {row['Law']}\n")
        result_box.insert(tk.END, f"📜 Paragraf: {row['Paragraph']}\n")
        result_box.insert(tk.END, f"🔍 Skóre: {row['score']:.4f}\n\n")

    top_paragraph = top.iloc[0].get("Text") or top.iloc[0].get("Paragraph") or ""
    explain_button.config(state=tk.NORMAL if top_paragraph else tk.DISABLED)

def explain_top():
    global last_explanation
    if not top_paragraph:
        messagebox.showinfo("Info", "Není vybrán žádný paragraf k vysvětlení.")
        return

    query = query_var.get()
    prompt = (
        f"Vysvětli tento právní text v jednoduchých slovech:\n\n"
        f"Paragraf: {top_paragraph}\n\n"
        f"Na základě dotazu: {query}\n\n"
        "Vysvětlení:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jsi právní asistent, který jednoduše vysvětluje zákony."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        explanation = response.choices[0].message.content.strip()
        last_explanation = explanation
    except Exception as e:
        explanation = f"Chyba při získávání vysvětlení: {e}"
        last_explanation = explanation

    # Popup
    win = tk.Toplevel(root)
    win.title("Vysvětlení")
    win.geometry("600x400")
    text = tk.Text(win, wrap=tk.WORD, font=("Arial", 12))
    text.pack(expand=True, fill=tk.BOTH)
    text.insert(tk.END, explanation)
    text.config(state=tk.DISABLED)

def clear_all():
    query_var.set("")
    result_box.delete(1.0, tk.END)
    explain_button.config(state=tk.DISABLED)

def export_txt():
    content = result_box.get(1.0, tk.END).strip()
    if not content:
        messagebox.showinfo("Info", "Žádné výsledky k exportu.")
        return

    explanation = last_explanation or "Žádné vysvětlení nebylo vygenerováno."
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Uložit jako..."
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("🔎 Výsledky vyhledávání:\n\n")
            f.write(content + "\n\n")
            f.write("🧠 Vysvětlení:\n\n")
            f.write(explanation)
        messagebox.showinfo("Hotovo", "Výsledky byly úspěšně exportovány.")

# Buttons
tk.Button(root, text="🔎 Hledat", command=run_query, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=5)
explain_button = tk.Button(root, text="🧠 Vysvětlit", command=explain_top, font=("Arial", 12), bg="#2196F3", fg="white", state=tk.DISABLED)
explain_button.pack(pady=5)
tk.Button(root, text="💾 Exportovat do TXT", command=export_txt, font=("Arial", 12), bg="#9C27B0", fg="white").pack(pady=5)
tk.Button(root, text="❌ Vymazat dotaz", command=clear_all, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=5)
tk.Button(root, text="🚪 Ukončit aplikaci", command=root.destroy, font=("Arial", 12), bg="#607D8B", fg="white").pack(pady=5)

# Start
root.mainloop()
