def normalize_json(payload: dict, datetime_fields: set[str]):
    """
    Normalizador do payload JSON para comparação de campos no Pytest
    """
    normalized = payload.copy()
    for field in datetime_fields:
        normalized[field] = None
    return normalized


# Pq não funciona daqui?!? Mistério!
def strip_created_at(item: dict) -> dict:
    """
    Payload sem 'created_at' para evitar confusões pythonicas de
    tempo UTC e tempo naive

    Args:
        item (dict): O dicionário do qual queremos tirar a chave 'created_at'

    Returns:
        dict: _description_
    """
    return {k: v for k, v in item.items() if k != "created_at"}
