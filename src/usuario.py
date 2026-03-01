from datetime import date, datetime
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