# visitas/app.py

from museu_scaffoldo.modules.utils.date_util import extrair_data

# Simulação de Banco de Dados
fake_visitas_db = []


def get_visitas(skip: int, limit: int, start_date=None, end_date=None):
    resultados = []

    for v in fake_visitas_db:
        data_do_item = extrair_data(v)
        if data_do_item is None:
            continue

        if start_date and data_do_item < start_date:
            continue

        if end_date and data_do_item > end_date:
            continue

        resultados.append(v)

    return resultados[skip : skip + limit]
