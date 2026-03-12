# src/logica.py
def filtrar_por_tipo(espacos, tipo):
    return [e for e in espacos if e["tipo"].lower() == tipo.lower()]

def filtrar_por_capacidade(espacos, capacidade_minima):
    return [e for e in espacos if e["capacidade"] >= capacidade_minima]

def filtrar_por_preco(espacos, preco_maximo):
    return [e for e in espacos if e["preco_base"] <= preco_maximo]