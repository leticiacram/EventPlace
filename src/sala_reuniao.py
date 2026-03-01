from datetime import datetime
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
        return info