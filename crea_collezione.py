from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from constanti import *

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)  # Modifica host/port se necessario

vector_size = 384  # Dimensione del vettore
distance_metric = Distance.COSINE  # Metrica per calcolare la distanza

# Verifica se la collezione esiste
if client.collection_exists(collection_name=COLLECTION_NAME):
    print(f"La collezione '{COLLECTION_NAME}' esiste già.")
else:
    # Crea la collezione se non esiste
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=distance_metric),
    )
    print(f"Collezione '{COLLECTION_NAME}' creata con successo!")
