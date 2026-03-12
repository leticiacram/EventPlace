from src.database import ler_dados, salvar_dados
from src.modelos import Espaco, Proprietario

def cadastrar_proprietario(nome, email, telefone, senha="123"):
    dados = ler_dados()
    novo_id = len(dados["proprietarios"]) + 1
    
    novo = {
        "id": novo_id,
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "senha": senha,
        "espacos": []
    }
    
    dados["proprietarios"].append(novo)
    salvar_dados(dados)
    return novo_id

def cadastrar_espaco(id_prop, nome, tipo, local, preco, capacidade, diferenciais):
    dados = ler_dados()
    
    if not any(p["id"] == id_prop for p in dados["proprietarios"]):
        return None

    novo_id = len(dados["espacos"]) + 1
    
    novo_espaco = {
        "id": novo_id,
        "id_proprietario": id_prop,
        "nome": nome,
        "tipo": tipo,
        "localizacao": local,
        "preco": preco,
        "capacidade": capacidade,
        "diferenciais": diferenciais 
    }
    
    dados["espacos"].append(novo_espaco)
    salvar_dados(dados)
    return novo_id

def excluir_espaco(id_espaco):
    dados = ler_dados()
    dados["espacos"] = [e for e in dados["espacos"] if e["id"] != id_espaco]
    salvar_dados(dados)