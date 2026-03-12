import json
import os

# Caminho robusto para o JSON
DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_ARQUIVO = os.path.join(DIRETORIO_RAIZ, 'data', 'dados.json')

def ler_dados():
    try:
        if not os.path.exists(CAMINHO_ARQUIVO):
            return {"proprietarios": [], "espacos": []}
        with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"proprietarios": [], "espacos": []}

def salvar_dados(dados):
    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)