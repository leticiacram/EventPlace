from datetime import date, datetime
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
        return total