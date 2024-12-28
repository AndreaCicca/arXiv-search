import os
import json
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from constanti import *

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Inizializza il modello di embedding
embedding_model = SentenceTransformer(ENBEDDING_MODEL)

# Crea o ricrea la collezione
if not client.collection_exists(collection_name=COLLECTION_NAME):
    print(f"Prima di eseguire l'embedding devi creare la collezione '{COLLECTION_NAME}'")
    print("Esegui il comando 'create_collection.py' per crearla.")
    exit()

# Funzione per estrarre il testo dai PDF
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Errore durante l'estrazione del testo da {pdf_path}: {e}")
        return None

def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Itera sui file di metadati
for metadata_file in os.listdir(METADATA_DIR):
    if not metadata_file.endswith(".json"):
        continue

    # Carica i metadati
    metadata_path = os.path.join(METADATA_DIR, metadata_file)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Estrarre il nome del PDF associato
    pdf_filename = metadata_file.replace(".json", ".pdf")  # Usa il nome del file JSON
    # markdown_filename = metadata_file.replace(".json", ".md")  # Usa il nome del file JSON
    
    # Posso estrarre il testo del PDF dalla sua versione Markdown
    pdf_path = os.path.join(PDF_DIR, pdf_filename)
    # markdown_path = os.path.join(MARKDOWN_DIR, markdown_filename)

    # Controlla se il PDF esiste
    if not os.path.exists(pdf_path):
        print(f"PDF non trovato per {metadata_file}. Percorso atteso: {pdf_path}")
        continue

    # Estrai il testo dal PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        print(f"Errore durante l'estrazione del testo per {metadata_file}. Salto.")
        continue
    
    # Estrai il testo dal Markdown
    # markdown_text = read_markdown_file(markdown_path)
    # if not markdown_text:
    #     print(f"Errore durante l'estrazione del testo per {metadata_file}. Salto.")
    #     continue

    # Genera embedding combinando metadati e testo PDF
    combined_text = f"{metadata['title']}\n{metadata['summary']}\n{pdf_text}"
    embedding = embedding_model.encode(combined_text, convert_to_tensor=False)

    # Genera un ID valido per Qdrant
    point_id = str(uuid.uuid4())  # Genera un UUID univoco

    
    
    # NOTA BEBNE: il campo `vector` è obbligatorio e deve essere coerente con quello che viene utilizzato quando si crea la collezione
    client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        {
            "id": point_id,
            "vector": embedding.tolist(),  # Usa il campo `vector`
            "payload": {
                "title": metadata["title"],
                "summary": metadata["summary"],
                "text": pdf_text,
                "authors": metadata["authors"],
                "categories": metadata["categories"],
                "published": metadata["published"],
                "updated": metadata["updated"],
                "pdf_link": metadata["pdf_link"],
            },
        }
    ],
)



    print(f"Caricato: {metadata_file} con il PDF associato.")

print("Caricamento completato!")
