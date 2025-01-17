import os
import uuid
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor
from costanti import *
import pandas as pd
from tqdm import tqdm
import torch

MAX_WORKERS = os.cpu_count() / 2
BATCH_SIZE = 250

print('Loading libraries')
# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Inizializza il modello di embedding
device = 'cuda:1' if torch.cuda.is_available() else 'cpu'
embedding_model = SentenceTransformer(EMBEDDING_MODEL).to(device)

# Crea o ricrea la collezione
if not client.collection_exists(collection_name=COLLECTION_NAME):
    print(f"Prima di eseguire l'embedding devi creare la collezione '{COLLECTION_NAME}'")
    print("Esegui il comando 'crea_collezione.py' per crearla.")
    exit()

def process_papers(papers):
    text_batch = [
        f"{paper['title']}\n{paper['authors']}\n{paper['categories']}\n{paper['abstract']}"
        for _, paper in papers.iterrows()
    ]

    embeddings = embedding_model.encode(text_batch, convert_to_tensor=False, show_progress_bar=False)

    points = []
    for i, (_, paper) in enumerate(papers.iterrows()):
        point = {
            "id": str(uuid.uuid4()),
            "vector": embeddings[i].tolist(),
            "payload": {
                "title": paper["title"],
                "authors": paper["authors"],
                "categories": paper["categories"],
                "summary": paper["abstract"],
                "published": paper["created"],
                "arxiv-id": paper["id"]
            },
        }
        points.append(point)

    return points

def process_batch(batch):
    points = process_papers(batch)
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    return len(points)

def main():
    print('Loading metadata')
    papers = pd.read_json('dataset/cs-12-24.json',dtype=False) #.sample(10000)
    print('Metadata loaded!')

    batches = [papers[i:i + BATCH_SIZE] for i in range(0, len(papers), BATCH_SIZE)]

    #with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    #    futures = [executor.submit(process_batch, batch) for batch in batches]
    #
    #    for future in tqdm(futures, total=len(batches)):
    #        future.result()
    for batch in tqdm(batches, desc="Processing batches"):
        process_batch(batch)

    print("Caricamento completato.")

if __name__ == "__main__":
    main()