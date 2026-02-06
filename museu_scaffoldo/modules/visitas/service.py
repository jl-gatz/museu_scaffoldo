# visitas/app.py

from museu_scaffoldo.modules.utils.date_util import extrair_data

# Simulação de Banco de Dados
fake_visitas_db = []


def get_visitas(skip: int, limit: int, start_date=None, end_date=None) -> list:
    """_summary_

    Args:
        skip (int): Um int, indicando quantos registros devem ser ignorados
        limit (int): Um int que estabelece o limite de paginação
        start_date (_type_, optional): A data inicial no caso de pesquisa
        por período. Defaults to None.
        end_date (_type_, optional): A data final no caso de pesquisa
        por período. Defaults to None.

    Returns:
        list: _description_
    """
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
