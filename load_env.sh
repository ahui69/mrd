#!/bin/bash
# Skrypt do ładowania zmiennych z pliku .env dla środowiska runpod

echo "[MRD69] Ładuję zmienne środowiskowe z pliku .env..."

# Sprawdź, czy plik .env istnieje
if [ -f .env ]; then
    # Wczytaj zmienne z pliku .env
    export $(grep -v '^#' .env | xargs)
    echo "[MRD69] Zmienne środowiskowe załadowane pomyślnie"
    
    # Ustaw WORKSPACE na runpod
    export WORKSPACE="/workspace/mrd69"
    export MEM_DB="${WORKSPACE}/mem.db"
    export AUTON_WAL="${WORKSPACE}/data/mem/autonauka.wal"
    
    echo "[MRD69] Ustawiono ścieżki dla runpod:"
    echo "WORKSPACE: $WORKSPACE"
    echo "MEM_DB: $MEM_DB"
    echo "AUTON_WAL: $AUTON_WAL"
    
else
    echo "[MRD69] BŁĄD: Plik .env nie istnieje!"
    exit 1
fi

# Uruchom polecenie przekazane jako argument
if [ $# -gt 0 ]; then
    echo "[MRD69] Uruchamiam: $@"
    exec "$@"
fi