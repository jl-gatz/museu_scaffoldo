def normalize_json(payload: dict, datetime_fields: set[str]):
    """
    Normalizador do payload JSON para comparação de campos no Pytest
    """
    normalized = payload.copy()
    for field in datetime_fields:
        normalized[field] = None
    return normalized
