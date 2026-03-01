from datetime import datetime
from typing import Optional

class Avaliacao:
    """Representa uma avaliação de um espaço"""
    
    def __init__(self, id: int, reserva_id: int, cliente_id: int, 
                 nota: int, comentario: str):
        self.id = id
        self.reserva_id = reserva_id
        self.cliente_id = cliente_id
        self.nota = nota
        self.comentario = comentario
        self.resposta: Optional[str] = None
        self.data_criacao = datetime.now()
        self.data_resposta: Optional[datetime] = None
    
    def responder(self, resposta: str) -> bool:
        """Adiciona uma resposta à avaliação"""
        self.resposta = resposta
        self.data_resposta = datetime.now()
        return True
    
    def to_dict(self) -> dict:
        """Converte a avaliação para dicionário"""
        return {
            "id": self.id,
            "reserva_id": self.reserva_id,
            "cliente_id": self.cliente_id,
            "nota": self.nota,
            "comentario": self.comentario,
            "resposta": self.resposta,
            "data_criacao": self.data_criacao
        }from datetime import date, datetime
from typing import List, Dict, Any, Optional
from .usuario import Usuario
from .reserva import Reserva
from .avaliacao import Avaliacao

class Cliente(Usuario):
    """Classe que representa um cliente do sistema"""
    
    def __init__(self, id: int, nome: str, email: str, senha: str, telefone: str,
                 data_cadastro: date, cpf: str, data_nascimento: date):
        super().__init__(id, nome, email, senha, telefone, data_cadastro)
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.historico_reservas: List[Reserva] = []
        self.favoritos: List[int] = []
        self.preferencias: Dict[str, Any] = {}
        self.avaliacoes_feitas: List[int] = []

    def buscar_espacos(self, filtro_dict: Dict[str, Any]) -> List['Espaco']:
        """Busca espaços com base nos filtros fornecidos"""
        from .espaco import Espaco
        # Em produção, consultaria um repositório
        return []

    def favoritar_espaco(self, espaco_id: int) -> bool:
        """Adiciona um espaço à lista de favoritos"""
        if espaco_id not in self.favoritos:
            self.favoritos.append(espaco_id)
            return True
        return False

    def desfavoritar_espaco(self, espaco_id: int) -> bool:
        """Remove um espaço da lista de favoritos"""
        if espaco_id in self.favoritos:
            self.favoritos.remove(espaco_id)
            return True
        return False

    def avaliar_espaco(self, reserva_id: int, nota: int, comentario: str) -> Avaliacao:
        """Cria uma nova avaliação para um espaço"""
        if nota < 1 or nota > 5:
            raise ValueError("Nota deve estar entre 1 e 5")
        
        avaliacao = Avaliacao(
            id=len(self.avaliacoes_feitas) + 1,
            reserva_id=reserva_id,
            cliente_id=self.id,
            nota=nota,
            comentario=comentario
        )
        self.avaliacoes_feitas.append(avaliacao.id)
        return avaliacao

    def visualizar_historico(self) -> List[Dict[str, Any]]:
        """Retorna o histórico de reservas do cliente"""
        return [r.to_dict() for r in self.historico_reservas]

    def solicitar_reserva(self, espaco_id: int, dados_dict: Dict[str, Any]) -> Reserva:
        """Solicita uma nova reserva"""
        if 'data_inicio' not in dados_dict or 'data_fim' not in dados_dict:
            raise ValueError("Data de início e fim são obrigatórias")
        
        nova_reserva = Reserva(
            id=len(self.historico_reservas) + 1,
            espaco_id=espaco_id,
            cliente_id=self.id,
            data_inicio=dados_dict['data_inicio'],
            data_fim=dados_dict['data_fim']
        )
        self.historico_reservas.append(nova_reserva)
        return nova_reserva

    def cancelar_reserva(self, reserva_id: int) -> bool:
        """Cancela uma reserva existente"""
        for reserva in self.historico_reservas:
            if reserva.id == reserva_id:
                return reserva.cancelar()
        return False

    def validar_cpf(self) -> bool:
        """Valida o CPF do cliente"""
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            return False
        return True

    def calcular_gastos_total(self) -> float:
        """Calcula o total gasto em reservas confirmadas"""
        total = 0.0
        for reserva in self.historico_reservas:
            if reserva.status == "confirmada" and reserva.valor_total:
                total += reserva.valor_total
        return totalfrom datetime import datetime
from typing import List, Dict, Any, Optional
from .reserva import Reserva

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

    def calcular_preco(self, tempo: float, tipo: str) -> str:
        """
        Calcula o preço baseado no tempo e tipo
        tipo: 'hora', 'diaria', 'base'
        """
        if tipo == "hora":
            valor = tempo * self.preco_hora
        elif tipo == "diaria":
            valor = tempo * self.preco_diaria
        else:
            valor = self.preco_base
        
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def verificar_disponibilidade(self, data: datetime) -> bool:
        """Verifica se o espaço está disponível em uma data específica"""
        for reserva in self.reservas:
            if reserva.status in ["confirmada", "pendente"]:
                if reserva.data_inicio <= data <= reserva.data_fim:
                    return False
        return True

    def get_avaliacao_media(self) -> float:
        """Calcula a média das avaliações do espaço"""
        # Em produção, calcularia a partir das avaliações
        return 4.5

    def adicionar_foto(self, url_foto: str) -> bool:
        """Adiciona uma foto ao espaço"""
        if url_foto not in self.fotos:
            self.fotos.append(url_foto)
            return True
        return False

    def remover_foto(self, url_foto: str) -> bool:
        """Remove uma foto do espaço"""
        if url_foto in self.fotos:
            self.fotos.remove(url_foto)
            return True
        return False

    def _validar_capacidade(self, convidados: int) -> bool:
        """Valida se o número de convidados é compatível"""
        return convidados <= self.capacidade_pessoas

    def get_info_completa(self) -> Dict[str, Any]:
        """Retorna todas as informações do espaço"""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "capacidade": self.capacidade_pessoas,
            "area": self.area_m2,
            "precos": {
                "base": self.preco_base,
                "hora": self.preco_hora,
                "diaria": self.preco_diaria
            },
            "regras": self.regras,
            "status": self.status,
            "data_cadastro": self.data_cadastro,
            "fotos": self.fotos,
            "videos": self.videos,
            "avaliacao_media": self.get_avaliacao_media()
        }

    def is_disponivel(self) -> bool:
        """Verifica se o espaço está disponível para reservas"""
        return self.status == "ativo"

    def atualizar(self, dados: Dict[str, Any]) -> bool:
        """Atualiza dados do espaço"""
        campos_permitidos = ['nome', 'descricao', 'capacidade_pessoas', 'area_m2',
                            'preco_base', 'preco_hora', 'preco_diaria', 'regras', 'status']
        for chave, valor in dados.items():
            if chave in campos_permitidos:
                setattr(self, chave, valor)
        return Truefrom datetime import date, datetime
from typing import List, Dict, Any, Optional
from .usuario import Usuario
from .espaco import Espaco
from .salao_festa import SalaoFesta
from .sala_reuniao import SalaReuniao
from .reserva import Reserva

class Proprietario(Usuario):
    """Classe que representa um proprietário de espaços"""
    
    def __init__(self, id: int, nome: str, email: str, senha: str, telefone: str,
                 data_cadastro: date, cnpj_cpf: str, documento_verificado: bool = False):
        super().__init__(id, nome, email, senha, telefone, data_cadastro)
        self.cnpj_cpf = cnpj_cpf
        self.documento_verificado = documento_verificado
        self.comissao_contratual: float = 0.10
        self.dados_bancarios: Dict[str, Any] = {}
        self.espacos: List[Espaco] = []
        self.total_reservas: int = 0
        self.receita_total: float = 0.0
        self.avaliacao_media: float = 0.0

    def cadastrar_espaco(self, dados_dict: Dict[str, Any], tipo_espaco: str = "basico") -> bool:
        """Cadastra um novo espaço"""
        from copy import deepcopy
        
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

    def editar_espaco(self, espaco_id: int, dados_dict: Dict[str, Any]) -> bool:
        """Edita um espaço existente"""
        for espaco in self.espacos:
            if espaco.id == espaco_id:
                return espaco.atualizar(dados_dict)
        return False

    def remover_espaco(self, espaco_id: int) -> bool:
        """Remove um espaço (apenas se não houver reservas futuras)"""
        for espaco in self.espacos:
            if espaco.id == espaco_id:
                reservas_futuras = [
                    r for r in espaco.reservas 
                    if r.status in ['pendente', 'confirmada'] and r.data_inicio > datetime.now()
                ]
                if not reservas_futuras:
                    self.espacos.remove(espaco)
                    return True
        return False

    def visualizar_agenda(self, espaco_id: int) -> List[Reserva]:
        """Visualiza a agenda de reservas de um espaço"""
        for espaco in self.espacos:
            if espaco.id == espaco_id:
                return espaco.reservas
        return []

    def responder_avaliacao(self, avaliacao_id: int, resposta: str) -> bool:
        """Responde a uma avaliação"""
        # Em produção, implementar lógica real
        return True

    def ver_relatorio_ocupacao(self, periodo: str) -> Dict[str, Any]:
        """Gera relatório de ocupação"""
        relatorio = {
            "periodo": periodo,
            "total_reservas": self.total_reservas,
            "receita": self.receita_total,
            "espacos": []
        }
        
        for espaco in self.espacos:
            reservas_periodo = [
                r for r in espaco.reservas 
                if r.status == "confirmada"
            ]
            relatorio["espacos"].append({
                "nome": espaco.nome,
                "reservas": len(reservas_periodo),
                "ocupacao": len(reservas_periodo) / 30 * 100 if periodo == "mensal" else 0
            })
        
        return relatorio

    def solicitar_saque(self, valor: float) -> Dict[str, Any]:
        """Solicita um saque dos rendimentos"""
        if valor > self.receita_total:
            raise ValueError("Valor solicitado maior que o saldo disponível")
        
        transacao = {
            "id": hash(f"{self.id}{datetime.now()}"),
            "valor": valor,
            "data": datetime.now(),
            "status": "solicitado",
            "tipo": "saque"
        }
        return transacao

    def get_metricas(self) -> Dict[str, Any]:
        """Retorna métricas do proprietário"""
        return {
            "total_reservas": self.total_reservas,
            "receita_total": self.receita_total,
            "avaliacao_media": self.avaliacao_media,
            "espacos_ativos": len([e for e in self.espacos if e.status == "ativo"])
        }

    def calcular_comissao_devida(self) -> float:
        """Calcula a comissão a ser paga para a plataforma"""
        return self.receita_total * self.comissao_contratual

    def validar_documento(self) -> bool:
        """Valida CPF ou CNPJ"""
        if len(self.cnpj_cpf) == 11:  # CPF
            return len(self.cnpj_cpf) == 11 and self.cnpj_cpf.isdigit()
        elif len(self.cnpj_cpf) == 14:  # CNPJ
            return len(self.cnpj_cpf) == 14 and self.cnpj_cpf.isdigit()
        return Falsefrom datetime import datetime
from typing import Optional

class Reserva:
    """Representa uma reserva de espaço"""
    
    def __init__(self, id: int, espaco_id: int, cliente_id: int, 
                 data_inicio: datetime, data_fim: datetime):
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
        """Confirma a reserva"""
        if self.status == "pendente":
            self.status = "confirmada"
            return True
        return False
    
    def cancelar(self) -> bool:
        """Cancela a reserva"""
        if self.status in ["pendente", "confirmada"]:
            self.status = "cancelada"
            return True
        return False
    
    def concluir(self) -> bool:
        """Marca a reserva como concluída"""
        if self.status == "confirmada" and self.data_fim < datetime.now():
            self.status = "concluida"
            return True
        return False
    
    def to_dict(self) -> dict:
        """Converte a reserva para dicionário"""
        return {
            "id": self.id,
            "espaco_id": self.espaco_id,
            "cliente_id": self.cliente_id,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "status": self.status,
            "valor_total": self.valor_total
        }from datetime import datetime
from typing import List, Optional
from .espaco import Espaco

class SalaoFesta(Espaco):
    """Especialização para salões de festa"""
    
    def __init__(self, id: int, proprietario_id: int, nome: str, descricao: str,
                 capacidade_pessoas: int, area_m2: float, preco_base: float,
                 preco_hora: float, preco_diaria: float, regras: List[str],
                 data_cadastro: Optional[datetime] = None,
                 cozinha_industrial: bool = False, area_kids: bool = False,
                 estacionamento: int = 0, espaco_gourmet: bool = False,
                 piscina: bool = False, som_profissional: bool = False,
                 gerador: bool = False, camarim: bool = False,
                 tipo_evento_permitido: Optional[List[str]] = None,
                 churrasqueira: bool = False, banheiros: bool = True,
                 area_coberta: bool = False, acessibilidade: bool = False):
        
        super().__init__(id, proprietario_id, nome, descricao, capacidade_pessoas,
                         area_m2, preco_base, preco_hora, preco_diaria, regras, data_cadastro)
        
        self.cozinha_industrial = cozinha_industrial
        self.area_kids = area_kids
        self.estacionamento = estacionamento
        self.espaco_gourmet = espaco_gourmet
        self.piscina = piscina
        self.som_profissional = som_profissional
        self.gerador = gerador
        self.camarim = camarim
        self.tipo_evento_permitido = tipo_evento_permitido if tipo_evento_permitido else []
        self.churrasqueira = churrasqueira
        self.banheiros = banheiros
        self.area_coberta = area_coberta
        self.acessibilidade = acessibilidade

    def verificar_estrutura_evento(self, tipo: str) -> bool:
        """Verifica se o salão suporta um tipo específico de evento"""
        return tipo in self.tipo_evento_permitido

    def validar_area_kids(self) -> bool:
        """Valida se a área kids atende requisitos de segurança"""
        if not self.area_kids:
            return False
        return True

    def calcular_preco_casamento(self, convidados: int) -> float:
        """Calcula preço especial para casamentos"""
        if not self.verificar_estrutura_evento("casamento"):
            raise ValueError("Este salão não permite casamentos")
        
        if not self._validar_capacidade(convidados):
            raise ValueError(f"Número de convidados excede a capacidade de {self.capacidade_pessoas}")
        
        adicional = convidados * 15.0
        return self.preco_base + adicional

    def get_info_completa(self) -> dict:
        """Sobrescreve para incluir atributos específicos"""
        info = super().get_info_completa()
        info.update({
            "cozinha_industrial": self.cozinha_industrial,
            "area_kids": self.area_kids,
            "estacionamento": self.estacionamento,
            "piscina": self.piscina,
            "tipo_evento_permitido": self.tipo_evento_permitido,
            "acessibilidade": self.acessibilidade
        })
        return infofrom datetime import datetime
from typing import List, Optional
from .espaco import Espaco

class SalaReuniao(Espaco):
    """Especialização para salas de reunião"""
    
    def __init__(self, id: int, proprietario_id: int, nome: str, descricao: str,
                 capacidade_pessoas: int, area_m2: float, preco_base: float,
                 preco_hora: float, preco_diaria: float, regras: List[str],
                 data_cadastro: Optional[datetime] = None,
                 wifi: bool = True, projetor: bool = False, quadro_branco: bool = False,
                 video_conferencia: bool = False, computadores: int = 0,
                 recepcao: bool = False, mesas: int = 1, cadeiras: int = 0,
                 tomadas: int = 0, tomadas_rede: int = 0, ar_condicionado: bool = False,
                 isolamento_acustico: bool = False):
        
        super().__init__(id, proprietario_id, nome, descricao, capacidade_pessoas,
                         area_m2, preco_base, preco_hora, preco_diaria, regras, data_cadastro)
        
        self.wifi = wifi
        self.projetor = projetor
        self.quadro_branco = quadro_branco
        self.video_conferencia = video_conferencia
        self.computadores = computadores
        self.recepcao = recepcao
        self.mesas = mesas
        self.cadeiras = cadeiras
        self.tomadas = tomadas
        self.tomadas_rede = tomadas_rede
        self.ar_condicionado = ar_condicionado
        self.isolamento_acustico = isolamento_acustico

    def calcular_diaria_corporativa(self, dias: int) -> float:
        """Calcula diária com desconto corporativo"""
        if dias < 1:
            raise ValueError("Número de dias deve ser positivo")
        return dias * self.preco_diaria * 0.9

    def verificar_equipamentos(self, necessidades: List[str]) -> bool:
        """Verifica se todos os equipamentos necessários estão disponíveis"""
        equipamentos = {
            "wifi": self.wifi,
            "projetor": self.projetor,
            "quadro_branco": self.quadro_branco,
            "video_conferencia": self.video_conferencia,
            "computadores": self.computadores > 0,
            "ar_condicionado": self.ar_condicionado
        }
        
        return all(equipamentos.get(nec, False) for nec in necessidades)

    def configurar_layout(self, tipo: str) -> bool:
        """Configura o layout da sala"""
        layouts_validos = ['u', 'escola', 'teatro', 'circular', 'ilhas']
        return tipo in layouts_validos

    def calcular_capacidade_sala(self) -> int:
        """Calcula a capacidade real baseada no layout atual"""
        return self.capacidade_pessoas

    def get_info_completa(self) -> dict:
        """Sobrescreve para incluir atributos específicos"""
        info = super().get_info_completa()
        info.update({
            "wifi": self.wifi,
            "projetor": self.projetor,
            "video_conferencia": self.video_conferencia,
            "computadores": self.computadores,
            "ar_condicionado": self.ar_condicionado,
            "isolamento_acustico": self.isolamento_acustico
        })
        return infofrom datetime import date, datetime
from typing import Dict, Any, Optional
import re
import hashlib

class Usuario:
    """Classe base para todos os usuários do sistema"""
    
    def __init__(self, id: int, nome: str, email: str, senha: str, 
                 telefone: str, data_cadastro: date):
        self.id = id
        self.nome = nome
        self.email = email
        self._senha = senha
        self.telefone = telefone
        self.data_cadastro = data_cadastro
        self.ultimo_acesso: Optional[datetime] = None
        self.status: str = "ativo"

    def login(self, email: str, senha: str) -> bool:
        """Realiza o login do usuário"""
        if email == self.email and senha == self._senha:
            self.ultimo_acesso = datetime.now()
            return True
        return False

    def logout(self) -> None:
        """Realiza o logout do usuário"""
        pass

    def atualizar_perfil(self, dados: Dict[str, Any]) -> bool:
        """Atualiza os dados do perfil"""
        campos_permitidos = ['nome', 'email', 'telefone']
        for chave, valor in dados.items():
            if chave in campos_permitidos:
                setattr(self, chave, valor)
        return True

    def alterar_senha(self, senha_antiga: str, senha_nova: str) -> bool:
        """Altera a senha do usuário"""
        if senha_antiga == self._senha:
            self._senha = senha_nova
            return True
        return False

    def recuperar_senha(self) -> str:
        """Gera e retorna uma nova senha temporária"""
        nova_senha = f"temp{self.id}{datetime.now().strftime('%d%m')}"
        self._senha = nova_senha
        return nova_senha

    def get_info_basica(self) -> Dict[str, Any]:
        """Retorna informações básicas do usuário"""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "data_cadastro": self.data_cadastro,
            "ultimo_acesso": self.ultimo_acesso,
            "status": self.status
        }

    def _validar_email(self) -> bool:
        """Valida o formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, self.email) is not None

    def _criptografar_senha(self) -> str:
        """Criptografa a senha"""
        return hashlib.sha256(self._senha.encode()).hexdigest()