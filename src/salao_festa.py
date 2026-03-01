from datetime import datetime
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
        return info