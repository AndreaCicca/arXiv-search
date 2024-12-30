import os
import json
import uuid
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor
from costanti import *

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
                    "published": paper["versions"][0]["created"],
                    "updated": paper["update_date"],
                },
            }
        ],
    )

    print(f"Caricato: {paper['id']}")

# Itera sui file di metadati
with open('dataset/arxiv-computer-science.json', 'r', encoding='utf-8') as f:
    papers = [json.loads(line) for line in f]

max_workers = os.cpu_count() / 2

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(process_paper, papers)

print("Caricamento completato.")