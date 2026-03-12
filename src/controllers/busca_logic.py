# Importa a função de leitura do nosso banco de dados JSON
from ..database import ler_dados


def buscar_espacos(preco_max=None, localizacao=None, tipo=None):
    """
    Busca espaços aplicando filtros opcionais.
    Se um filtro for None (vazio), ele é ignorado na busca.
    """
    dados = ler_dados()
    todos_espacos = dados.get("espacos", [])

    resultados = []

    for espaco in todos_espacos:
        # 1. Filtro de Preço: verifica se o preço do espaço é MAIOR que o máximo que o cliente quer pagar
        if preco_max is not None and espaco["preco"] > preco_max:
            continue  # Se for mais caro, pula este espaço e vai para o próximo

        # 2. Filtro de Localização: verifica se o texto digitado está dentro do nome da cidade/bairro
        # Usamos .lower() para que "Indaiatuba" e "indaiatuba" sejam considerados iguais
        if localizacao is not None and localizacao.lower() not in espaco["localizacao"].lower():
            continue  # Se não for na mesma localização, pula

        # 3. Filtro de Tipo: verifica se o tipo do local bate com o que o cliente quer (Ex: "Chácara")
        if tipo is not None and tipo.lower() != espaco["tipo"].lower():
            continue  # Se for de outro tipo, pula

        # Se o espaço não caiu em nenhum dos 'continue' acima, significa que ele passou em todos os filtros!
        resultados.append(espaco)

    return resultados


def exibir_resultados(resultados):
    """
    Função auxiliar apenas para imprimir os resultados de forma bonita no terminal.
    """
    if not resultados:
        print("Nenhum espaço encontrado com esses filtros. 😔")
        return

    print(f"🎉 Encontramos {len(resultados)} espaço(s):")
    for espaco in resultados:
        print("-" * 30)
        print(f"Nome: {espaco['nome']} ({espaco['tipo']})")
        print(f"Local: {espaco['localizacao']}")
        print(f"Preço: R$ {espaco['preco']:.2f}")
        print(f"Capacidade: {espaco['capacidade']} pessoas")
        print(f"Diferenciais: {', '.join(espaco['diferenciais'])}")
    print("-" * 30)
