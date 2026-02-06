import re


def title_case_com_excecoes(text: str) -> str:
    """
    Formata o texto em caixa alta e baixa, ignorando artigos e conectores.

    Exemplo: 'departamento de tecnologia e informações'
    retorna: 'Departamento de Tecnologia e Informações'

    Args:
        text (str): O texto que queremos formatar

    Returns:
        str: A string formatada
    """
    ignorar = [
        "e",
        "de",
        "do",
        "da",
        "em",
        "a",
        "o",
        "as",
        "os",
        "que",
        "mas",
        "desde",
    ]
    # Divide, capitaliza, mas ignora as exceções
    word_list = re.split(" ", text.lower())
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in ignorar else word.capitalize())
    return " ".join(final)
