# src/controllers/reserva_logic.py
from src.database import ler_dados, salvar_dados


def criar_reserva(id_espaco, nome_cliente, email_cliente, telefone_cliente, data_reserva):
    dados = ler_dados()

    # Se a lista de reservas ainda não existir no JSON, cria uma vazia
    if "reservas" not in dados:
        dados["reservas"] = []

    espacos = dados.get("espacos", [])

    # Busca o espaço pelo ID para pegar o preço
    espaco = next((e for e in espacos if e["id"] == id_espaco), None)
    if not espaco:
        return False, "Espaço não encontrado."

    nova_reserva_id = len(dados["reservas"]) + 1

    nova_reserva = {
        "id": nova_reserva_id,
        "id_espaco": id_espaco,
        "nome_cliente": nome_cliente,
        "email_cliente": email_cliente,
        "telefone_cliente": telefone_cliente,
        "data_reserva": data_reserva,
        "valor_total": espaco["preco"],
        "status": "PENDENTE"  # Usando o status do seu modelos.py
    }

    dados["reservas"].append(nova_reserva)
    salvar_dados(dados)

    return True, nova_reserva_id


def buscar_reserva_por_id(id_reserva):
    dados = ler_dados()
    reservas = dados.get("reservas", [])
    espacos = dados.get("espacos", [])

    # Procura a reserva pelo ID
    reserva = next((r for r in reservas if r["id"] == id_reserva), None)

    if not reserva:
        return False, "Reserva não encontrada. Verifique se o número está correto."

    # Busca o nome e local do espaço para mostrar na tela do cliente
    espaco = next(
        (e for e in espacos if e["id"] == reserva["id_espaco"]), None)

    if espaco:
        reserva["nome_espaco"] = espaco["nome"]
        reserva["localizacao_espaco"] = espaco["localizacao"]
    else:
        reserva["nome_espaco"] = "Espaço Indisponível"
        reserva["localizacao_espaco"] = "-"

    return True, reserva
