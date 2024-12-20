from qdrant_client import QdrantClient
from constanti import *

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)  # Assicurati che HOST_DATABASE e PORT_DATABASE siano definiti

# Recupera i dettagli della collezione
collection_info = client.get_collection(collection_name=COLLECTION_NAME)
print(collection_info)