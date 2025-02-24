set -a  # Habilita a exportação automática de variáveis
source <(cat .env | grep -v '^#' | sed 's/\r$//')
set +a  # Desabilita a exportação automática