from PyQt5 import uic, QtWidgets
from functools import lru_cache
import mysql.connector

numero_id = 0

try:
    connection = mysql.connector.connect(
        host="aws-sa-east-1.connect.psdb.cloud",
        database="opencrm",
        user="pdt3ik0qpkan4zhiookr",
        password="pscale_pw_XIn6qQslKG0t3fBFQL28tUCM2m1EvfcIO2iAkJdTMnB",
    )

except mysql.connector.Error as error:
    print("erro ao conectar com o banco de dados", error)

@lru_cache(maxsize=1)
def funcao_principal():
    nome = formulario.lineEdit.text()
    cpfcnpj = formulario.lineEdit_2.text()
    endereco = formulario.lineEdit_3.text()
    telefone = formulario.lineEdit_4.text()
    email = formulario.lineEdit_5.text()
    intermediador = formulario.lineEdit_6.text()

    print("NOME:",nome)
    print("CPF/CNPJ:",cpfcnpj)
    print("ENDEREÇO:",endereco)
    print("TELEFONE:",telefone)
    print("E-MAIL:",email)
    print("INTERMEDIADOR:",intermediador)

    cursor = connection.cursor()
    sql_query = "INSERT INTO clientes (nome,cpfcnpj,endereco,telefone,email,intermediador) VALUES (%s,%s,%s,%s,%s,%s)"
    dados = (str(nome),str(cpfcnpj),str(endereco),str(telefone),str(email),str(intermediador))
    cursor.execute(sql_query,dados)
    connection.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")
    formulario.lineEdit_5.setText("")
    formulario.lineEdit_6.setText("")
    print("dados inseridos.")

def cadastrou():
    sucesso.show()

def ok_cadastrou():
    sucesso.close()

def sucesso_editado():
    sucesso_edicao.show()

def ok_sucesso_editado():
    sucesso_edicao.close()

def chama_segunda_tela():
    segunda_tela.show()

    cursor = connection.cursor()
    sql_query = "SELECT * FROM clientes"
    cursor.execute(sql_query)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(7)

    for i in range(0,len(dados_lidos)):
        for j in range(0, 7):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            segunda_tela.lineEdit.textChanged.connect(filtrar_dados)

@lru_cache(maxsize=500)
def filtrar_dados(texto_pesquisado):
    cursor = connection.cursor()
    sql_query = "SELECT * FROM clientes WHERE nome LIKE %s OR endereco LIKE %s OR telefone LIKE %s OR cpfcnpj LIKE %s OR email LIKE %s OR intermediador LIKE %s"
    cursor.execute(sql_query, (f"%{texto_pesquisado}%", f"%{texto_pesquisado}%", f"%{texto_pesquisado}%", f"%{texto_pesquisado}%", f"%{texto_pesquisado}%", f"%{texto_pesquisado}%"))
    dados_filtrados = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_filtrados))
    segunda_tela.tableWidget.setColumnCount(7)

    for i in range(0,len(dados_filtrados)):
        for j in range(0, 7):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_filtrados[i][j])))

def editar_dados_da_pesquisa():
    global numero_id
    linha_selecionada = segunda_tela.tableWidget.currentRow()
    
    numero_id = segunda_tela.tableWidget.item(linha_selecionada, 0).text()
    nome = segunda_tela.tableWidget.item(linha_selecionada, 1).text()
    cpfcnpj = segunda_tela.tableWidget.item(linha_selecionada, 2).text()
    endereco = segunda_tela.tableWidget.item(linha_selecionada, 3).text()
    telefone = segunda_tela.tableWidget.item(linha_selecionada, 4).text()
    email = segunda_tela.tableWidget.item(linha_selecionada, 5).text()
    intermediador = segunda_tela.tableWidget.item(linha_selecionada, 6).text()
    
    tela_editar.lineEdit_2.setText(nome)
    tela_editar.lineEdit_3.setText(cpfcnpj)
    tela_editar.lineEdit_4.setText(endereco)
    tela_editar.lineEdit_5.setText(telefone)
    tela_editar.lineEdit_6.setText(email)
    tela_editar.lineEdit_7.setText(intermediador)
    
    tela_editar.show()

def salvar_dados_editados_2():
    global numero_id
    
    nome = formulario_edicao.lineEdit_2.text()
    cpfcnpj = formulario_edicao.lineEdit_3.text()   
    endereco = formulario_edicao.lineEdit_4.text()
    telefone = formulario_edicao.lineEdit_5.text()
    email = formulario_edicao.lineEdit_6.text()
    intermediador = formulario_edicao.lineEdit_7.text()

    cursor = connection.cursor()
    cursor.execute("UPDATE clientes SET nome ='{}', cpfcnpj = '{}', endereco = '{}', telefone = '{}', email = '{}', intermediador = '{}' WHERE id = {}".format(nome,cpfcnpj,endereco,telefone,email,intermediador,numero_id))
    connection.commit()
    
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()

def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = connection.cursor()
    cursor.execute("SELECT id FROM clientes")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM clientes WHERE id="+ str(valor_id))
    connection.commit()
  
def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = connection.cursor()
    cursor.execute("SELECT id FROM clientes")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM clientes WHERE id="+ str(valor_id))
    cliente = cursor.fetchall()
    tela_editar.show()

    numero_id = valor_id

    tela_editar.lineEdit_2.setText(str(cliente[0][1]))
    tela_editar.lineEdit_3.setText(str(cliente[0][2]))
    tela_editar.lineEdit_4.setText(str(cliente[0][3]))
    tela_editar.lineEdit_5.setText(str(cliente[0][4]))
    tela_editar.lineEdit_6.setText(str(cliente[0][5]))
    tela_editar.lineEdit_7.setText(str(cliente[0][6]))
    connection.commit()

def salvar_dados_editados():
    global numero_id
    
    nome = tela_editar.lineEdit_2.text()
    cpfcnpj = tela_editar.lineEdit_3.text()
    endereco = tela_editar.lineEdit_4.text()
    telefone = tela_editar.lineEdit_5.text()
    email = tela_editar.lineEdit_6.text()
    intermediador = tela_editar.lineEdit_7.text()

    cursor = connection.cursor()
    cursor.execute("UPDATE clientes SET nome ='{}', cpfcnpj = '{}', endereco = '{}', telefone = '{}', email = '{}', intermediador = '{}' WHERE id = {}".format(nome,cpfcnpj,endereco,telefone,email,intermediador,numero_id))
    connection.commit()
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()

app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("lista_de_clientes.ui")
sucesso=uic.loadUi("sucesso.ui")
tela_editar=uic.loadUi("menu_editar.ui")
formulario_edicao=uic.loadUi("menu_editar_2.ui")
sucesso_edicao=uic.loadUi("sucesso_edicao.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton.clicked.connect(cadastrou)
sucesso.pushButton.clicked.connect(ok_cadastrou)
sucesso_edicao.pushButton.clicked.connect(ok_sucesso_editado)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados_da_pesquisa)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)
tela_editar.pushButton.clicked.connect(sucesso_editado)
formulario_edicao.pushButton.clicked.connect(salvar_dados_editados_2)
formulario_edicao.pushButton.clicked.connect(sucesso_editado)
formulario_edicao.pushButton.clicked.connect(ok_sucesso_editado)
formulario.show()
app.exec()











"""
codigo para criar banco de dados no planetscale

CREATE TABLE clientes(
id INT NOT NULL AUTO_INCREMENT,
nome VARCHAR(100),
cpfcnpj VARCHAR(100),
endereco VARCHAR(100),
telefone VARCHAR(100),
email VARCHAR(100),
intermediador VARCHAR(100),
PRIMARY KEY (id)
);


"""


""" 
codigo para inserir o primeiro dado

INSERT INTO clientes (nome,cpfcnpj,endereco,telefone,email,intermediador)
VALUES ('Nome','123.321/333-21','Rua teste,00','(00) 9999-9999','teste@teste.com','intermediador teste'); 

"""


#MADE BY THEBITT#