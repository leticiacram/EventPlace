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
        }