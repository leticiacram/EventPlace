import sys
import os

# Ajuste para o Python encontrar as pastas internas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import ler_dados, salvar_dados
from modelos import Proprietario, Espaco

def inicializar_teste():
    print("\n--- EVENTPLACE: TESTE DE INTEGRAÇÃO ---")
    
    # 1. Carrega dados brutos
    dados = ler_dados()
    
    # 2. Transforma dados brutos em Objetos Python (Modelos)
    lista_proprietarios = [Proprietario(**p) for p in dados.get("proprietarios", [])]
    lista_espacos = [Espaco(**e) for e in dados.get("espacos", [])]
    
    print(f"[*] Sistema carregado com {len(lista_proprietarios)} proprietários.")
    
    # 3. Exemplo de lógica de negócio: Verificando espaços caros
    if lista_espacos:
        mais_caro = max(lista_espacos, key=lambda x: x.preco)
        print(f"[!] Espaço de Luxo: {mais_caro.nome} (R$ {mais_caro.preco})")
    else:
        print("[?] Nenhum espaço cadastrado para análise.")

if __name__ == "__main__":
    inicializar_teste()