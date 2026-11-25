import math


def validar_produto(codigo, nome, preco, estoque_minimo):
    codigo = codigo.strip()
    nome = nome.strip()
    if not codigo:
        raise ValueError("Informe o código do produto.")
    if not nome:
        raise ValueError("Informe o nome do produto.")
    try:
        preco = float(preco.replace(",", "."))
        estoque_minimo = int(estoque_minimo)
    except (ValueError, AttributeError) as erro:
        raise ValueError("Preço e estoque mínimo devem ser números válidos.") from erro
    if not math.isfinite(preco) or preco < 0:
        raise ValueError("O preço não pode ser negativo.")
    if estoque_minimo < 0:
        raise ValueError("O estoque mínimo não pode ser negativo.")
    return codigo, nome, preco, estoque_minimo


def validar_movimentacao(quantidade):
    try:
        quantidade = int(quantidade)
    except (ValueError, TypeError) as erro:
        raise ValueError("A quantidade deve ser um número inteiro.") from erro
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    return quantidade
