import pymysql
from flask import Flask, render_template, request, redirect, url_for, session

# conectando mysql ao python
conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='admin',
    database='consultorio_bianca',
)

conexao_dict = pymysql.connect(
    host='localhost',
    user='root',
    password='admin',
    database='consultorio_bianca',
    cursorclass=pymysql.cursors.DictCursor
)


# criando uma instancia do Flask e secretkey do session
app = Flask(__name__)
cursor_dict = conexao_dict.cursor()

# criando a rota pra tela de login + validação de login com informações do banco de dados pra prosseguir nas prox paginas


@app.route("/", methods=['GET', 'POST'])
def validacao_login():

    # verficando se o request da pagina eh post ou get pra que ele consiga dar as informações e nao bugar o codigo
    if request.method == 'POST':
        # peganndo o user e pass do input do form html
        user = request.form.get('username')
        password = request.form.get('password')

        # debugando p ver se ta tudo certo
        print(f"Usuário: {user}")
        print(f"Senha: {password}")

        # criando conexao com o bd pra usar codigo mysql
        cursor = conexao.cursor()

        cursor.execute("SELECT pass FROM login WHERE usario = %s", (user,))
        result_pass = cursor.fetchone()

        if result_pass and result_pass[0] == password:
            return redirect(url_for('pagina_inicial'))
        else:
            return render_template("tela_de_login.html", error='usuario ou senha incorretos')
    return render_template("tela_de_login.html")

# rota para pagina inicial que contém as caixas com todas as opções do site


@app.route("/pagina_inicial",  methods=['POST', 'GET'])
def pagina_inicial():
    return render_template("pagina_inicial.html")

# rota para a pagina de cadastro do cliente


@app.route("/cadastrar", methods=['POST', 'GET'])
def tela_cadastro():

    # pegando valores do input do paciente pra jogar no bd
    nome = request.form.get('name')
    data_nasc = request.form.get('dob')
    genero = request.form.get('gender')
    contato = request.form.get('contact')
    endereco = request.form.get('address')
    queixa_principal = request.form.get('chief-complaint')
    historico_doenca = request.form.get('disease-history')
    medicacao_em_uso = request.form.get('medications')
    atv_fisica = request.form.get('physical-activity')
    antec_cirurgico = request.form.get('surgical-history')

    if not nome:
        print("o nome nao pode estar vazio")
    else:
        # codigo mysql pra realizar o armazenamento dos dados de cadastro no bf
        cursor = conexao.cursor()
        # lembrar de deixar essa linha mas dinamica dps
        cursor.execute("INSERT INTO cadastro_pacientes (nome, data_nasc, genero, contato, endereco, queixa_principal,historico_doenca, medicacao_em_uso, atv_fisica, antec_cirurgico) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)",
                       (nome, data_nasc, genero, contato, endereco, queixa_principal, historico_doenca, medicacao_em_uso, atv_fisica, antec_cirurgico))
        conexao.commit()

    # carregamento do html da pagina
    return render_template("tela_de_cadastro.html")


@app.route("/listar", methods=['POST', 'GET'])
def listagem_pacientes():

    cursor = conexao_dict.cursor()
    cursor.execute("SELECT * FROM cadastro_pacientes;")
    listagem = cursor.fetchall()
    conexao_dict.commit()

    return render_template("listagem_dos_pacientes.html", listagem=listagem)


@app.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    cursor = conexao_dict.cursor()
    cursor.execute("DELETE FROM cadastro_pacientes WHERE id = %s", (id))
    conexao_dict.commit()
    return redirect(url_for('pagina_inicial'))


# rota para pagina de visualização dos cadastros especificos
@app.route("/visualizar_cadastro/<int:id>", methods=['POST', 'GET'])
def visualizar(id):
    cursor = conexao_dict.cursor()
    cursor.execute('SELECT * FROM cadastro_pacientes WHERE id = %s', (id,))
    paciente = cursor.fetchone()
    conexao_dict.commit()

    return render_template("visualizar_cadastro.html", paciente=paciente)


# rota pra visualizar pagamentos dos dados cadastrados
@app.route("/pagamentos", methods=['POST', 'GET'])
def pagamentos():
    cursor_dict.execute('SELECT id, nome FROM cadastro_pacientes;')
    cadastros = cursor_dict.fetchall()
    cursor_dict.execute("SELECT id FROM pagamento")
    pagamentos = cursor_dict.fetchall()

    for cadastro in cadastros:
        paciente_id = cadastro['id']
        nome_cadastro = cadastro['nome']

        cursor_dict.execute(
            "SELECT cadastro_id FROM pagamento WHERE cadastro_id = %s", (paciente_id,))
        pagamentos_cadastrados = cursor_dict.fetchall()

        if not pagamentos_cadastrados:
            cursor_dict.execute("""INSERT INTO pagamento (nome_cadastro, cadastro_id)
                    VALUES(%s, %s)""", (nome_cadastro, paciente_id))

    conexao_dict.commit()
    cursor_dict.execute("SELECT * FROM pagamento")
    pagamentos = cursor_dict.fetchall()

    return render_template("tela_de_pagamentos.html", pagamentos=pagamentos)

# rota  pra visualizar a edição de pagamentos


@app.route("/editar_pagamento/<int:cadastro_id>", methods=['POST', 'GET'])
def editar_pagamento(cadastro_id):

    cursor_dict.execute(
        "SELECT * FROM pagamento WHERE cadastro_id = %s", (cadastro_id))
    pagamento = cursor_dict.fetchone()
    return render_template('editar_pagamentos.html', pagamento=pagamento)


@app.route("/atualizar_pagamento/<int:cadastro_id>", methods=['POST'])
def atualizar_pagamento(cadastro_id):

    data_consulta = request.form.get('data_consulta')
    valor_consulta = request.form.get('valor_consulta')
    pagamento_feito = request.form.get('pagamento_feito')
    print(valor_consulta)
    print(data_consulta)
    print(pagamento_feito)
    print(cadastro_id)

    cursor_dict.execute("""UPDATE pagamento SET data_consulta = %s,
                        valor_consulta = %s,
                        pagamento_feito = %s
                        WHERE cadastro_id = %s""", (data_consulta, valor_consulta, pagamento_feito, cadastro_id))
    conexao_dict.commit()
    return redirect(url_for('pagamentos'))


app.run(debug=True)
