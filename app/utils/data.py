import pickle

def multiplex_dicts(primary_list: list[dict], secondary_list: list[dict]) -> list[dict]:
    """
    Combina cada dicionário da lista primária com cada dicionário da lista secundária.

    :param primary_list: Lista de dicionários com informações primárias.
    :param secondary_list: Lista de dicionários com informações secundárias.
    :return: Lista de dicionários combinados.
    """
    # Usa compreensão de listas para fundir cada par com desempacotamento de dicionários
    return [{**p, **s} for p in primary_list for s in secondary_list]


def combine_primary_with_secondary(primary: dict, secondary_list: list[dict]) -> list[dict]:
    """
    Combina o dicionário primário com cada dicionário da lista secundária.

    :param primary: Dicionário com informações primárias.
    :param secondary_list: Lista de dicionários com informações secundárias.
    :return: Lista de dicionários combinados.
    """
    return [{**primary, **secondary} for secondary in secondary_list]


def get_or_create_cache(path, default={}):
    """
    Obtém ou cria um cache para armazenar dados persistentes.

    Args:
        path (str): Caminho do arquivo de cache.
        default: Valor padrão a ser retornado se o cache não existir.

    Returns:
        dict: Dicionário com os dados do cache.
    """
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return default if default is not None else {}


def save_cache(path, data):
    """
    Salva os dados no cache.

    Args:
        path (str): Caminho do arquivo de cache.
        data (dict): Dados a serem salvos no cache.
    """
    with open(path, 'wb') as f:
        pickle.dump(data, f)
