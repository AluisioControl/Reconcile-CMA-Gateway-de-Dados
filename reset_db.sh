#!/bin/bash
#cp -f CMA_Gateway_original.db CMA_Gateway.db
rm CMA_Gateway.db
uv run python -m app.migrations.0001_initial_db
uv run python -m app.migrations.0002_add_field