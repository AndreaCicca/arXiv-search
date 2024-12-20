from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from constanti import *

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Ricrea la collezione con una configurazione valida
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={"default": VectorParams(size=384, distance=Distance.COSINE)},  # Configura un vettore chiamato "default"
)
print(f"Collezione '{COLLECTION_NAME}' ricreata con successo!")