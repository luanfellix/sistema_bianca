from flask import Flask, render_template
import pymysql


conexao = pymysql.connect(
    host='localhost',
    database='teste',
    user='root',
    password='admin'
)

'''
cursor.execute("USE teste")
cursor.execute("INSERT INTO pessoa(nome, idade) values ('joao', '15')")

conexao.commit()'''





