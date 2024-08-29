from flask import Flask, render_template
import pymysql


conexao = pymysql.connect(
    host='localhost',
    database='consultorio_bianca',
    user='root',
    password='admin'
)

cursor = conexao.cursor()
cursor.execute("SELECT * FROM cadastro_pacientes")
cadastros = cursor.fetchall()
#print(cadastros)

for cadastro in cadastros:
    paciente_id = cadastro[0]
    nome_cadastro = cadastro[1]
    data_consulta = '1.1.1000'
    valor_consulta= 100
    pagamento_feito =  0



    
    

    cursor.execute("""INSERT INTO pagamento (nome_cadastro, data_consulta, valor_consulta, pagamento_feito, cadastro_id)
               VALUES(%s, %s, %s, %s, %s)""", (nome_cadastro, data_consulta, valor_consulta, pagamento_feito, paciente_id))

conexao.commit()

    






