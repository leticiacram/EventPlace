from datetime import date, datetime
from typing import List, Dict, Tuple, Any, Optional
import re
import hashlib
from copy import deepcopy

# ==========================================
# 1. CLASSES DE APOIO (Independentes)
# ==========================================

class Endereco:
    """Representa o endereço físico de um espaço"""
    def __init__(self, id: int, cep: str, logradouro: str, numero: int,
                 bairro: str, cidade: str, estado: str, pais: str,
                 latitude: float, longitude: float, zona: str, regiao: str,
                 complemento: str = "", ponto_referencia: str = "", mapa_url: str = ""):
        self.id = id
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.latitude = latitude
        self.longitude = longitude
        self.zona = zona
        self.regiao = regiao
        self.ponto_referencia = ponto_referencia
        self.mapa_url = mapa_url

    def get_endereco_completo(self) -> str:
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"

class Localizacao:
    """Classe que descreve o contexto e acessibilidade da região"""
    def __init__(self, regiao: str, zona: str, acessibilidade_transporte: bool):
        self.regiao = regiao
        self.zona = zona
        self.pontos_referencia: List[str] = []
        self.acessibilidade_transporte = acessibilidade_transporte
        self.estacionamentos_proximos: List[str] = []

class Avaliacao:
    """Representa uma avaliação de um espaço"""
    def __init__(self, id: int, reserva_id: int, cliente_id: int, nota: int, comentario: str):
        self.id = id
        self.reserva_id = reserva_id
        self.cliente_id = cliente_id
        self.nota = nota
        self.comentario = comentario
        self.resposta: Optional[str] = None
        self.data_criacao = datetime.now()
        self.data_resposta: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id, "reserva_id": self.reserva_id, "cliente_id": self.cliente_id,
            "nota": self.nota, "comentario": self.comentario, "resposta": self.resposta
        }

class Reserva:
    """Representa uma reserva de espaço"""
    def __init__(self, id: int, espaco_id: int, cliente_id: int, data_inicio: datetime, data_fim: datetime):
        self.id = id
        self.espaco_id = espaco_id
        self.cliente_id = cliente_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = "pendente"  # pendente, confirmada, cancelada, concluida
        self.data_criacao = datetime.now()
        self.valor_total: Optional[float] = None
        self.forma_pagamento: Optional[str] = None

    def confirmar(self) -> bool:
        if self.status == "pendente":
            self.status = "confirmada"
            return True
        return False

    def cancelar(self) -> bool:
        if self.status in ["pendente", "confirmada"]:
            self.status = "cancelada"
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "id": self.id, "espaco_id": self.espaco_id, "cliente_id": self.cliente_id,
            "data_inicio": self.data_inicio, "data_fim": self.data_fim,
            "status": self.status, "valor_total": self.valor_total
        }

class Pagamento:
    """Representa a gestão financeira de uma reserva"""
    def __init__(self, id: int, reserva: Reserva, valor: float, forma_pagamento: str, status: str, parcelas: int, gateway: str):
        self.id = id
        self.reserva = reserva
        self.valor = valor
        self.forma_pagamento = forma_pagamento
        self.status = status
        self.data_pagamento: Optional[datetime] = None
        self.codigo_transacao: str = f"TRX-{id}{datetime.now().strftime('%M%S')}"
        self.parcelas = parcelas
        self.gateway = gateway


# ==========================================
# 2. HIERARQUIA DE ESPAÇOS
# ==========================================

class Espaco:
    """Classe base para todos os espaços"""
    def __init__(self, id: int, proprietario_id: int, nome: str, descricao: str,
                 capacidade_pessoas: int, area_m2: float, preco_base: float,
                 preco_hora: float, preco_diaria: float, regras: List[str],
                 data_cadastro: Optional[datetime] = None):
        self.id = id
        self.proprietario_id = proprietario_id
        self.nome = nome
        self.descricao = descricao
        self.capacidade_pessoas = capacidade_pessoas
        self.area_m2 = area_m2
        self.preco_base = preco_base
        self.preco_hora = preco_hora
        self.preco_diaria = preco_diaria
        self.regras = regras
        self.status: str = "ativo"
        self.data_cadastro = data_cadastro if data_cadastro else datetime.now()
        self.fotos: List[str] = []
        self.videos: List[str] = []
        self.reservas: List[Reserva] = []
        self.endereco: Optional[Endereco] = None # Conexão com o código do Julio

    def get_info_completa(self) -> Dict[str, Any]:
        return {
            "id": self.id, "nome": self.nome, "descricao": self.descricao,
            "capacidade": self.capacidade_pessoas, "area": self.area_m2,
            "precos": {"base": self.preco_base, "hora": self.preco_hora, "diaria": self.preco_diaria},
            "status": self.status
        }

class SalaoFesta(Espaco):
    """Especialização para salões de festa"""
    def __init__(self, id: int, proprietario_id: int, nome: str, descricao: str,
                 capacidade_pessoas: int, area_m2: float, preco_base: float,
                 preco_hora: float, preco_diaria: float, regras: List[str],
                 data_cadastro: Optional[datetime] = None,
                 cozinha_industrial: bool = False, area_kids: bool = False,
                 estacionamento: int = 0, piscina: bool = False, 
                 tipo_evento_permitido: Optional[List[str]] = None, acessibilidade: bool = False):
        
        super().__init__(id, proprietario_id, nome, descricao, capacidade_pessoas,
                         area_m2, preco_base, preco_hora, preco_diaria, regras, data_cadastro)
        self.cozinha_industrial = cozinha_industrial
        self.area_kids = area_kids
        self.estacionamento = estacionamento
        self.piscina = piscina
        self.tipo_evento_permitido = tipo_evento_permitido if tipo_evento_permitido else []
        self.acessibilidade = acessibilidade

    def get_info_completa(self) -> dict:
        info = super().get_info_completa()
        info.update({
            "cozinha_industrial": self.cozinha_industrial, "area_kids": self.area_kids,
            "piscina": self.piscina, "acessibilidade": self.acessibilidade
        })
        return info

class SalaReuniao(Espaco):
    """Especialização para salas de reunião"""
    def __init__(self, id: int, proprietario_id: int, nome: str, descricao: str,
                 capacidade_pessoas: int, area_m2: float, preco_base: float,
                 preco_hora: float, preco_diaria: float, regras: List[str],
                 data_cadastro: Optional[datetime] = None,
                 wifi: bool = True, projetor: bool = False, video_conferencia: bool = False, 
                 computadores: int = 0, ar_condicionado: bool = False, isolamento_acustico: bool = False):
        
        super().__init__(id, proprietario_id, nome, descricao, capacidade_pessoas,
                         area_m2, preco_base, preco_hora, preco_diaria, regras, data_cadastro)
        self.wifi = wifi
        self.projetor = projetor
        self.video_conferencia = video_conferencia
        self.computadores = computadores
        self.ar_condicionado = ar_condicionado
        self.isolamento_acustico = isolamento_acustico

    def get_info_completa(self) -> dict:
        info = super().get_info_completa()
        info.update({
            "wifi": self.wifi, "projetor": self.projetor, "ar_condicionado": self.ar_condicionado
        })
        return info


# ==========================================
# 3. HIERARQUIA DE USUÁRIOS
# ==========================================

class Usuario:
    """Classe base para todos os usuários do sistema"""
    def __init__(self, id: int, nome: str, email: str, senha: str, telefone: str, data_cadastro: date):
        self.id = id
        self.nome = nome
        self.email = email
        self._senha = senha
        self.telefone = telefone
        self.data_cadastro = data_cadastro
        self.ultimo_acesso: Optional[datetime] = None
        self.status: str = "ativo"
        self.endereco: Optional[Endereco] = None # Conexão com o código do Julio

    def login(self, email: str, senha: str) -> bool:
        if email == self.email and senha == self._senha:
            self.ultimo_acesso = datetime.now()
            return True
        return False

class Cliente(Usuario):
    """Classe que representa um cliente do sistema"""
    def __init__(self, id: int, nome: str, email: str, senha: str, telefone: str,
                 data_cadastro: date, cpf: str, data_nascimento: date):
        super().__init__(id, nome, email, senha, telefone, data_cadastro)
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.historico_reservas: List[Reserva] = []
        self.avaliacoes_feitas: List[int] = []

    def solicitar_reserva(self, espaco_id: int, dados_dict: Dict[str, Any]) -> Reserva:
        nova_reserva = Reserva(
            id=len(self.historico_reservas) + 1, espaco_id=espaco_id,
            cliente_id=self.id, data_inicio=dados_dict['data_inicio'], data_fim=dados_dict['data_fim']
        )
        self.historico_reservas.append(nova_reserva)
        return nova_reserva

class Proprietario(Usuario):
    """Classe que representa um proprietário de espaços"""
    def __init__(self, id: int, nome: str, email: str, senha: str, telefone: str,
                 data_cadastro: date, cnpj_cpf: str, documento_verificado: bool = False):
        super().__init__(id, nome, email, senha, telefone, data_cadastro)
        self.cnpj_cpf = cnpj_cpf
        self.espacos: List[Espaco] = []
        self.receita_total: float = 0.0

    def cadastrar_espaco(self, dados_dict: Dict[str, Any], tipo_espaco: str = "basico") -> bool:
        dados = deepcopy(dados_dict)
        dados['id'] = len(self.espacos) + 1
        dados['proprietario_id'] = self.id
        
        if tipo_espaco == "salao_festa":
            novo_espaco = SalaoFesta(**dados)
        elif tipo_espaco == "sala_reuniao":
            novo_espaco = SalaReuniao(**dados)
        else:
            novo_espaco = Espaco(**dados)
        
        self.espacos.append(novo_espaco)
        return True
    