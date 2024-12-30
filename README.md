# Script per la vettorizzazione dei PDF tramite Qdrant

Per la guida a come mettere su un server Qdrant consiglio di visualizzare il Quickstart messo a disposizione dal tool https://qdrant.tech/documentation/quickstart/

Questi script in ordine:
- Permettono di creare una collezione Qdrant
- Permettono di scaricare i PDF dei paper da arXiv sfruttando la loro Api pubblica
- Permettono di embeddare il contenuto dei PDF, insieme ai loro metadati su Qdrant
- Permette di visualizzare il contenuto dei punti/vettori (consiglio comunque di sfruttare la dashboard offrita dal tool  localhost:6333/dashboard)
- Eliminare una collezione quando non più richiesta
