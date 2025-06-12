#!/bin/bash

echo "Resetting database and running migrations..."
./reset_db.sh

echo "Reconcile2 with Gateway BM1..."
cp data_gwmb1.json data.json
PYTHONPATH=$(pwd) uv run python -m app.reconcile2.main

echo "Pausing for 60 seconds..."
sleep 60

echo "Reconcile2 with Gateway BM2..."
cp data_gwmb2.json data.json
PYTHONPATH=$(pwd) uv run python -m app.reconcile2.main
