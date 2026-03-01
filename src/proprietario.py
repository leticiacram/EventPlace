from datetime import date, datetime
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
        return False