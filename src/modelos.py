from datetime import datetime

# --- ENUMS (Opções fixas) ---
class TipoEspaco:
    SALAO_FESTA = "SALAO_FESTA"
    SALA_REUNIAO = "SALA_REUNIAO"

class StatusReserva:
    PENDENTE = "PENDENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

# --- CLASSES ---
class Usuario:
    def __init__(self, id, nome, email, telefone, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha

class Proprietario(Usuario):
    def __init__(self, id, nome, email, telefone, senha=None, espacos=None):
        super().__init__(id, nome, email, telefone, senha)
        self.espacos = espacos if espacos is not None else []

class Espaco:
    def __init__(self, id, id_proprietario, nome, tipo, localizacao, preco, capacidade, diferenciais):
        self.id = id
        self.id_proprietario = id_proprietario
        self.nome = nome
        self.tipo = tipo
        self.localizacao = localizacao
        self.preco = preco
        self.capacidade = capacidade
        self.diferenciais = diferenciais

class Reserva:
    def __init__(self, id, id_cliente, id_espaco, data_inicio, data_fim, valor_total, status=StatusReserva.PENDENTE):
        self.id = id
        self.id_cliente = id_cliente
        self.id_espaco = id_espaco
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.valor_total = valor_total
        self.status = status