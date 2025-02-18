# Script per la vettorizzazione dei PDF tramite Qdrant

Per la guida a come mettere su un server Qdrant consiglio di visualizzare il Quickstart messo a disposizione dal tool https://qdrant.tech/documentation/quickstart/.

Di seguito gli script presenti:
- `costanti.py`: contiene le costanti di progetto
- `crea_collezione.py`: crea una collezione Qdrant
- `elimina_collezione.py`: elimina una collezione Qdrant
- `download_script.py`: scarica i PDF dei paper da arXiv sfruttando la loro Api pubblica
- `database.py`: embedda il contenuto dei PDF, insieme ai loro metadati su Qdrant
- `query.py`: effetua una query all'interno del database Qdrant e restituisce i documenti più simili
- `stats.py`: recupera i dettagli della collezione Qdrant
- `recupera_punti.py`: recupera il contenuto dei punti/vettori (consiglio comunque di sfruttare la dashboard offerta dal tool localhost:6333/dashboard)
- `select_computer_science.py`: estrae dal dataset arXiv solo i paper a tema "*computer science*"


# Istruzioni per l'uso

## Clonazione del repository

```bash
git clone https://github.com/AndreaCicca/arXiv-vettorizzazione
cd arXiv-vettorizzazione
```

## Inizializzazione sottomoduli

```bash
git submodule init
git submodule update
```

# Build dell'immagine Docker

```bash
cd docker
docker compose up -d --build
```