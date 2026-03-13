from flask import Flask, render_template, request, redirect, url_for
from src.controllers.cadastro_logic import cadastrar_proprietario, cadastrar_espaco, excluir_espaco
from src.database import ler_dados
from src.modelos import Espaco, Proprietario, Reserva, TipoEspaco

app = Flask(__name__)

# --- FILTRO PARA FORMATAR MOEDA (R$ 130,00) ---
@app.template_filter('moeda')
def moeda(valor):
    try:
        # Garante 2 casas decimais e troca ponto por vírgula no padrão BR
        return "{:,.2f}".format(float(valor)).replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return valor

# --- ROTA PRINCIPAL (VITRINE) ---
@app.route('/')
def index():
    dados = ler_dados()
    espacos = dados.get("espacos", [])
    
    # Filtros de Busca
    tipo_filtro = request.args.get('tipo')
    preco_max = request.args.get('preco_max')
    
    if tipo_filtro:
        espacos = [e for e in espacos if e['tipo'] == tipo_filtro]
    
    if preco_max:
        try:
            espacos = [e for e in espacos if float(e['preco']) <= float(preco_max)]
        except ValueError:
            pass
            
    return render_template('index.html', espacos=espacos)

# --- ROTA DE CADASTRO ---
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem = None
    if request.method == 'POST':
        tipo_form = request.form.get('tipo_formulario')
        
        # Lógica para Proprietário
        if tipo_form == 'proprietario':
            novo_id = cadastrar_proprietario(
                request.form.get('nome'), 
                request.form.get('email'), 
                request.form.get('telefone')
            )
            mensagem = f"✅ Proprietário #{novo_id} cadastrado com sucesso!"
            
        # Lógica para Espaço (Evento)
        elif tipo_form == 'espaco':
            diferenciais_raw = request.form.get('diferenciais', '')
            difs_lista = [d.strip() for d in diferenciais_raw.split(',') if d.strip()]
            
            sucesso = cadastrar_espaco(
                id_prop=int(request.form.get('id_proprietario')),
                nome=request.form.get('nome'),
                tipo=request.form.get('tipo'),
                local=request.form.get('localizacao'),
                preco=float(request.form.get('preco')),
                capacidade=int(request.form.get('capacidade')),
                diferenciais=difs_lista
            )
            
            if sucesso:
                mensagem = "✅ Espaço cadastrado e disponível para locação!"
            else:
                mensagem = "❌ Erro: ID do Proprietário não encontrado no sistema."
            
    return render_template('cadastro.html', mensagem=mensagem)

# --- ROTA PARA EXCLUIR ---
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    excluir_espaco(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)