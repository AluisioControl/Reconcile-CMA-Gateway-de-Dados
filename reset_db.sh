#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status

#change to the directory of the script
cd "$(dirname "$0")"

# load .env file
set -a
source <(grep -E '^[a-zA-Z_][a-zA-Z0-9_]*=' .env)
set +a

# remove the database file
if [ -f "${SQLITE_MIDDLEWARE_PATH}" ]; then
    rm ${SQLITE_MIDDLEWARE_PATH}
else
    echo "File ${SQLITE_MIDDLEWARE_PATH} does not exist."
fi

uv run python -m app.migrate

echo "Database reset complete."