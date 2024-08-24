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


cursor = conexao.cursor()
cursor.execute("USE teste")

name = input("qual seu nome?")

age = input("qual sua idade?")

cursor.execute("INSERT INTO pessoa(nome, idade) VALUES (%s, %s)",(name, age))

conexao.commit()



