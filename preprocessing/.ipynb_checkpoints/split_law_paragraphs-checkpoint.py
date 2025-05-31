{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "e13350f7-3afd-4291-b33c-b5454fe3a83c",
   "metadata": {},
   "outputs": [],
   "source": [
    "# preprocessing/split_law_paragraphs.py\n",
    "\n",
    "import pandas as pd\n",
    "import re\n",
    "import os\n",
    "\n",
    "def split_into_paragraphs(csv_path=\"data/zakony_data.csv\", output_path=\"data/law_paragraphs.csv\"):\n",
    "    df = pd.read_csv(csv_path)\n",
    "    \n",
    "    # List to hold all split paragraphs\n",
    "    paragraphs = []\n",
    "\n",
    "    for idx, row in df.iterrows():\n",
    "        law_name = row['Název předpisu'] if 'Název předpisu' in row else f\"Law_{idx}\"\n",
    "        full_text = row['Aktuální znění']\n",
    "\n",
    "        # Split into paragraphs by § symbol (used in Czech laws)\n",
    "        # Each paragraph starts with § and may include \"§ 123\", \"§ 123a\", etc.\n",
    "        split = re.split(r\"(?=§\\s?\\d+[a-zA-Z]?)\", full_text)\n",
    "\n",
    "        for part in split:\n",
    "            clean = part.strip()\n",
    "            if clean:\n",
    "                paragraphs.append({\n",
    "                    \"Law\": law_name,\n",
    "                    \"Paragraph\": clean\n",
    "                })\n",
    "\n",
    "    # Save to DataFrame\n",
    "    para_df = pd.DataFrame(paragraphs)\n",
    "    os.makedirs(os.path.dirname(output_path), exist_ok=True)\n",
    "    para_df.to_csv(output_path, index=False, encoding=\"utf-8-sig\")\n",
    "    \n",
    "    print(f\"✅ Split into {len(para_df)} paragraphs. Saved to {output_path}\")\n",
    "    return para_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c4c67627-82a1-4d92-803a-6f52800ee06f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
