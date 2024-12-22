from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from constanti import *

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Ricrea la collezione con una configurazione valida
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=ENBEDDING_MODEL_NUMERO_PARAMETRI, distance=Distance.COSINE),  # Rimuovi il nome del vettore
)
print(f"Collezione '{COLLECTION_NAME}' ricreata con successo!")