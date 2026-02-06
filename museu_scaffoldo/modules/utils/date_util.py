from datetime import datetime, timezone


# O "Clock" padrão que será usado em produção
def get_current_time() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def extrair_data(item):
    val = None

    # 1. Se for um Objeto Pydantic (VisitaDB/VisitaBase)
    if hasattr(item, "data_visita"):
        val = getattr(item, "data_visita", None)

    # 2. Se for um Dicionário
    # (caso tenha sobrado algum dict antigo no teste)
    elif isinstance(item, dict):
        val = item.get("data_visita")

    # --- Lógica de conversão (igual a anterior) ---
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, str):
        try:
            return datetime.fromisoformat(val).date()
        except ValueError:
            return None
    return None
