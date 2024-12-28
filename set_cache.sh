#!/usr/bin/env bash

# set_cache.sh
# Imposta la variabile HF_HOME nella cartella corrente, in una sottocartella chiamata 'cache'.

CACHE_DIR="$(pwd)/cache"

# Crea la cartella cache se non esiste già
mkdir -p "$CACHE_DIR"

# Esporta la variabile HF_HOME
export HF_HOME="$CACHE_DIR"

echo "HF_HOME è stato impostato su: $HF_HOME"
