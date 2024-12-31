from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa la libreria CORS
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import ScoredPoint
import threading

PORT_DATABASE = 6555
HOST_DATABASE = "172.17.0.1"
COLLECTION_NAME = "Gruppo1_test"
EMBEDDING_MODEL = "all-mpnet-base-v2"
EMBEDDING_MODEL_NUMERO_PARAMETRI = 768

# Inizializza il client Qdrant
client = QdrantClient(host=HOST_DATABASE, port=PORT_DATABASE)

# Inizializza il modello di embedding
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte e tutte le origini

# Variabile per tracciare lo stato del modello
model_ready = False

def download_model():
    global model_ready
    # Scarica il modello di embedding
    embedding_model.encode("test")
    model_ready = True

# Scarica il modello in un thread separato
threading.Thread(target=download_model).start()

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

@app.route('/health', methods=['GET'])
def health_check():
    if model_ready:
        return jsonify({"status": "ready"}), 200
    else:
        return jsonify({"status": "loading"}), 503

@app.route('/query', methods=['POST', 'OPTIONS'])
def handle_query():
    if request.method == 'OPTIONS':
        # Gestisci la preflight request
        return '', 200

    if not model_ready:
        return jsonify({"error": "Il modello è ancora in fase di caricamento"}), 503

    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "Il campo 'query' è obbligatorio"}), 400

    try:
        results = embed_and_search(query, top_k=10)

        if results:
            response = []
            for result in results:
                response.append({
                    "id": result.id,
                    "score": result.score,
                    "title": result.payload.get('title', 'N/A'),
                    "summary": result.payload.get('summary', 'N/A')
                })
            return jsonify(response)
        else:
            return jsonify({"message": "Nessun risultato trovato."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)