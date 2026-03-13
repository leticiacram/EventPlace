from flask import Flask, render_template, request, redirect, url_for
from src.controllers.cadastro_logic import cadastrar_proprietario, cadastrar_espaco, excluir_espaco
from src.database import ler_dados
from src.modelos import Espaco, Proprietario, Reserva, TipoEspaco
from src.controllers.reserva_logic import criar_reserva
from src.controllers.reserva_logic import criar_reserva, buscar_reserva_por_id

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
            espacos = [e for e in espacos if float(
                e['preco']) <= float(preco_max)]
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
            mensagem = f"✅ Proprietário: {novo_id} cadastrado com sucesso!"

        # Lógica para Espaço (Evento)
        elif tipo_form == 'espaco':
            diferenciais_raw = request.form.get('diferenciais', '')
            difs_lista = [d.strip()
                          for d in diferenciais_raw.split(',') if d.strip()]

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

# --- ROTA PARA RESERVAR ESPAÇO ---


@app.route('/reservar/<int:id_espaco>', methods=['GET', 'POST'])
def reservar(id_espaco):
    dados = ler_dados()
    espacos = dados.get("espacos", [])

    # Busca os detalhes do espaço para mostrar na tela
    espaco = next((e for e in espacos if e["id"] == id_espaco), None)

    if not espaco:
        return "Espaço não encontrado!", 404

    mensagem = None

    if request.method == 'POST':
        nome = request.form.get('nome_cliente')
        email = request.form.get('email_cliente')
        telefone = request.form.get('telefone_cliente')
        data = request.form.get('data_reserva')

        sucesso, resultado = criar_reserva(
            id_espaco, nome, email, telefone, data)

        if sucesso:
            mensagem = f"Pedido de reserva #{resultado} enviado com sucesso! O proprietário entrará em contato."
        else:
            mensagem = f"❌ Erro: {resultado}"

    return render_template('reserva.html', espaco=espaco, mensagem=mensagem)

# --- ROTA PARA CONSULTAR RESERVA (CLIENTE) ---


@app.route('/minha-reserva', methods=['GET', 'POST'])
def minha_reserva():
    reserva = None
    erro = None

    if request.method == 'POST':
        try:
            id_busca = int(request.form.get('id_reserva'))
            sucesso, resultado = buscar_reserva_por_id(id_busca)

            if sucesso:
                reserva = resultado
            else:
                erro = resultado
        except (ValueError, TypeError):
            erro = "Por favor, digite um número de ID válido."

    return render_template('minha_reserva.html', reserva=reserva, erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
