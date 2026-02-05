from datetime import datetime, timedelta, timezone


def assert_iso_datetime_close(
    value: str,
    expected: datetime,
    *,
    delta: timedelta = timedelta(milliseconds=500),
) -> None:
    """
    Compara um datetime em ISO-8601 (string) com um datetime esperado,
    normalizando ambos para UTC e permitindo um pequeno delta.

    - value: string ISO retornada pela API (ex: '2026-02-05T12:00:00+00:00')
    - expected: datetime (FakeDatetime ou datetime real)
    - delta: tolerância máxima aceitável
    """

    # 1️⃣ Parse seguro da string ISO
    try:
        actual = datetime.fromisoformat(value)
    except ValueError as exc:
        raise AssertionError(
            f"Valor não é um datetime ISO válido: {value}"
        ) from exc

    # 2️⃣ Garantir timezone (defensivo)
    if actual.tzinfo is None:
        actual = actual.replace(tzinfo=timezone.utc)

    if expected.tzinfo is None:
        expected = expected.replace(tzinfo=timezone.utc)

    # 3️⃣ Normalizar ambos para UTC
    actual = actual.astimezone(timezone.utc)
    expected = expected.astimezone(timezone.utc)

    # 4️⃣ Comparar com tolerância
    diff = abs(actual - expected)

    assert diff <= delta, (
        "Datetimes não são próximos o suficiente:\n"
        f"  actual:   {actual.isoformat()}\n"
        f"  expected: {expected.isoformat()}\n"
        f"  diff:     {diff}\n"
        f"  allowed:  {delta}"
    )
