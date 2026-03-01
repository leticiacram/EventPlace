from datetime import datetime
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
        }