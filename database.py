import os
import json
import uuid
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor
from costanti import *
import pandas as pd
from tqdm import tqdm

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Inizializza il modello di embedding
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

# Crea o ricrea la collezione
if not client.collection_exists(collection_name=COLLECTION_NAME):
    print(f"Prima di eseguire l'embedding devi creare la collezione '{COLLECTION_NAME}'")
    print("Esegui il comando 'crea_collezione.py' per crearla.")
    exit()

# Funzione per generare embedding e caricare i dati su Qdrant
def process_paper(paper):
    paper = paper._asdict()
    combined_text = f"{paper['title']}\n{paper['authors']}\n{paper['categories']}\n{paper['abstract']}"
    embedding = embedding_model.encode(combined_text, convert_to_tensor=False)

    point_id = str(uuid.uuid4())

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": point_id,
                "vector": embedding.tolist(),
                "payload": {
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "categories": paper["categories"],
                    "summary": paper["abstract"],
                    "published": paper["created"],
                    "updated": paper["update_date"],
                },
            }
        ],
    )

    #print(f"Caricato: {paper['id']}")
    return point_id

# Itera sui file di metadati
print('Loading metadata')
papers = pd.read_json('cs-23-24.json').head(100)
print('Metadata loaded!')

max_workers = os.cpu_count() / 2

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    results = list(tqdm(executor.map(process_paper, papers.itertuples()), total=len(papers)))

print("Caricamento completato.")