def multiplex_dicts(primary_list: list[dict], secondary_list: list[dict]) -> list[dict]:
    """
    Combina cada dicionário da lista primária com cada dicionário da lista secundária.

    :param primary_list: Lista de dicionários com informações primárias.
    :param secondary_list: Lista de dicionários com informações secundárias.
    :return: Lista de dicionários combinados.
    """
    # Usa compreensão de listas para fundir cada par com desempacotamento de dicionários
    return [{**p, **s} for p in primary_list for s in secondary_list]


def combine_primary_with_secondary(
    primary: dict, secondary_list: list[dict]
) -> list[dict]:
    """
    Combina o dicionário primário com cada dicionário da lista secundária.

    :param primary: Dicionário com informações primárias.
    :param secondary_list: Lista de dicionários com informações secundárias.
    :return: Lista de dicionários combinados.
    """
    return [{**primary, **secondary} for secondary in secondary_list]
