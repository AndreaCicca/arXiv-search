from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import ScoredPoint
from costanti import *

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Inizializza il modello di embedding
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def embed_and_search(query: str, top_k: int = 5):
    """
    Embedda una frase e cerca nel database i documenti più simili.

    Args:
        query (str): La frase da embeddare e cercare.
        top_k (int): Il numero di risultati più simili da restituire.

    Returns:
        List[ScoredPoint]: Lista di punti più simili.
    """
    # Genera l'embedding della frase
    query_embedding = embedding_model.encode(query, convert_to_tensor=False).tolist()

    # Esegui la ricerca nel database
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
    )

    return search_results

if __name__ == "__main__":
    print("Benvenuto! Questo script ti permette di cercare frasi all'interno del database.")
    
    while True:
        query = input("Inserisci una frase da cercare (o 'q'/'exit' per terminare): ")
        
        if query.lower() in ['q', 'exit']:
            print("Uscita dal programma.")
            break
        
        try:
            results = embed_and_search(query, top_k=10)

            if results:
                print("\nRisultati trovati:")
                for i, result in enumerate(results):
                    print(f"{i + 1}. ID: {result.id}")
                    print(f"   Punteggio: {result.score}")
                    print(f"   Titolo: {result.payload.get('title', 'N/A')}")
                    print(f"   Sommario: {result.payload.get('summary', 'N/A')[:100]}...")
            else:
                print("\nNessun risultato trovato.")
        except Exception as e:
            print(f"Errore durante la ricerca: {e}")
