from datetime import datetime
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
        return True