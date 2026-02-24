from datetime import datetime, timezone


# O "Clock" padrão que será usado em produção
def get_current_time() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def extrair_data(item):
    val = None

    if hasattr(item, "data_visita"):
        val = getattr(item, "data_visita", None)

    elif isinstance(item, dict):
        val = item.get("data_visita")

    if isinstance(val, datetime):
        return val  # ← NÃO converta para date

    if isinstance(val, str):
        try:
            return datetime.fromisoformat(val)
        except ValueError:
            return None

    return None
