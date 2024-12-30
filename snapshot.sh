#!/bin/bash

# Creazione della cartella 'dataset' se non esiste
mkdir -p dataset

# Esecuzione del comando curl per scaricare il file nella cartella 'dataset'
curl -L -o ./dataset/arxiv.zip \
  https://www.kaggle.com/api/v1/datasets/download/Cornell-University/arxiv

# Verifica del completamento del download
if [[ $? -eq 0 ]]; then
  echo "Download completato con successo. Il file è stato salvato in './dataset/arxiv.zip'."
else
  echo "Errore durante il download."
fi

# Estrazione del file ZIP
unzip -o ./dataset/arxiv.zip -d ./dataset