from qdrant_client import QdrantClient
from arXiv.constanti import *


client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

points = client.scroll(collection_name=COLLECTION_NAME, limit=10)

# Stampa i dettagli dei punti
for point in points[0]:  # `points` è una tupla (risultati, next_page_token)
    print(f"ID: {point.id}")
    print(f"Title: {point.payload['title']}")
    print(f"Summary: {point.payload['summary']}")
    print(f"Text (first 500 chars): {point.payload['text'][:500]}...")  # Mostra i primi 500 caratteri del testo
    print("-" * 40)