from qdrant_client import QdrantClient
from arXiv.constanti import *

# Configura il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Verifica se la collezione esiste
if client.collection_exists(collection_name=COLLECTION_NAME):
    # Elimina tutti i punti nella collezione
    client.delete_collection(collection_name=COLLECTION_NAME)
    print(f"Tutti i dati nella collezione '{COLLECTION_NAME}' sono stati eliminati.")
else:
    print(f"La collezione '{COLLECTION_NAME}' non esiste.")
