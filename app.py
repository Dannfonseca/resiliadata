from flask import Flask, render_template, request, redirect, url_for, flash
#from dotenv import load_dotenv
import os
import psycopg2 #pip install psycopg2
import psycopg2.extras



app = Flask(__name__)
app.secret_key = "pevehdev"

DB_HOST = "localhost"
DB_NAME = "resiliadata"
DB_USER = "postgres"
DB_PASS = "ravula32"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password = DB_PASS, host=DB_HOST)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
########### ROTA HOME ###########################
@app.route('/')
def home():
    return render_template('home.html')

###########FACILITADOR################
@app.route('/exibirFacilitadores')
def exibirFacilitadores():
    sql = "SELECT * from Facilitadores"
    cursor.execute(sql)
    lista_facilitadores = cursor.fetchall()
    return render_template('facilitadores/facilitadores.html', lista_facilitadores = lista_facilitadores)

@app.route('/add_facilitadores', methods = ['POST'] )
def add_facilitadores():
    if request.method == 'POST':
        # Dados do formulário
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        genero = request.form['genero']
        area = request.form['area']
        horario = request.form['horario']
        localizacao = request.form['localizacao']
        data_contrato = request.form['data_contrato']
        salario = request.form['salario']
        rua = request.form['rua']
        cep = request.form['cep']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        pais = request.form['pais']
        
        # Inserir dados de endereço
        cursor.execute("INSERT INTO Endereco (rua, cep, cidade, bairro, pais) VALUES (%s,%s,%s,%s,%s) RETURNING id", (rua, cep, cidade, bairro, pais))
        endereco_id = cursor.fetchone()[0]  # Obtém o ID do endereço inserido
        
        # Inserir dados de pessoa associando o ID do endereço
        cursor.execute("INSERT INTO Pessoa (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id", (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero))
        Pessoa_id = cursor.fetchone()[0] # Obtém o ID do endereço inserido

        cursor.execute("INSERT INTO Facilitadores(Pessoa_id, area, horario, localizacao, data_contrato, salario) VALUES (%s, %s, %s, %s, %s,%s)", (Pessoa_id,area, horario, localizacao,data_contrato, salario))

        conn.commit()

        flash('Estudante cadastrado com sucesso!')
        return redirect(url_for('exibirFacilitadores'))
    
@app.route('/updateFacilitadores/<id>', methods=['POST'])
def updateFacilitadores(id):
    if request.method == 'POST':
        area = request.form['area']
        horario = request.form['horario']
        localizacao = request.form['localizacao']
        data_contrato = request.form['data_contrato']
        salario = request.form['salario']

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
        UPDATE Facilitadores
        SET area = %s,
            horario = %s,
            localizacao = %s,
            data_contrato = %s,
            salario = %s
        WHERE id = %s
        """, (area, horario, localizacao, data_contrato,salario, id))
        flash('Facilitador foi atualizado com sucesso!')
        conn.commit()
        return redirect(url_for('exibirFacilitadores'))
        
@app.route('/editFacilitadores/<string:id>', methods = ['POST', 'GET'])
def editFacilitadores(id):
    cursor.execute('Select * FROM Facilitadores WHERE id = {0}'.format(id))
    data = cursor.fetchall()
    return render_template('facilitadores/editFacilitadores.html', facilitadores = data[0] )

@app.route('/deleteFacilitadores/<string:id>', methods = ['POST','GET'])
def deleteFacilitadores(id):
    cursor.execute(
        'DELETE FROM Facilitadores Where id = {0}'.format(id)
    )
    cursor.execute(
        'DELETE FROM Pessoa Where id = {0}'.format(id)
    )
    cursor.execute(
        'DELETE FROM Endereco where id = {0}'.format(id)
    )
    conn.commit()
    flash('Funcionario Deletado!')
    return redirect(url_for('exibirFacilitadores'))

###########ESTUDANTE###################
### cADASTRAR ESTUDANTE ###

@app.route('/add_estudante', methods=['POST'])
def add_estudante():
    if request.method == 'POST':
        # Dados do formulário
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        genero = request.form['genero']
        data_matricula = request.form['data_matricula']
        numero_matricula = request.form['numero_matricula']
        status = request.form['status']
        rua = request.form['rua']
        cep = request.form['cep']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        pais = request.form['pais']
        
        # Inserir dados de endereço
        cursor.execute("INSERT INTO Endereco (rua, cep, cidade, bairro, pais) VALUES (%s,%s,%s,%s,%s) RETURNING id", (rua, cep, cidade, bairro, pais))
        endereco_id = cursor.fetchone()[0]  # Obtém o ID do endereço inserido
        
        # Inserir dados de pessoa associando o ID do endereço
        cursor.execute("INSERT INTO Pessoa (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id", (endereco_id, nome, sobrenome, email, telefone, data_nasc, genero))
        Pessoa_id = cursor.fetchone()[0] # Obtém o ID do endereço inserido

        cursor.execute("INSERT INTO Estudantes(Pessoa_id, data_matricula, numero_matricula, status) VALUES (%s, %s, %s, %s)", (Pessoa_id,data_matricula,numero_matricula,status))

        conn.commit()

        flash('Estudante cadastrado com sucesso!')
        return redirect(url_for('exibirEstudantes'))
    
### EXIBIR OS VALORES ESTUDANTES ###    

@app.route('/exibirEstudantes')
def exibirEstudantes():
    sql = "SELECT * FROM Estudantes"
    cursor.execute(sql)
    lista_estudantes = cursor.fetchall()
    
    return render_template('estudante.html', lista_estudantes = lista_estudantes)
### EDIT ESTUDANTE ###

@app.route('/editEstudante/<string:id>', methods = ['POST', 'GET'])

def editEstudante(id):
    cursor.execute('SELECT * FROM Estudantes WHERE id = {0}'.format(id))
    data = cursor.fetchall()
   
    
    return render_template('editEstudante.html', estudante = data[0])

### ATUALIZAR OS DADOS  ###

@app.route('/updateEstudante/<id>', methods=['POST'])
def update_estudante(id):
    if request.method == 'POST': 
        data_matricula = request.form['data_matricula']
        numero_matricula = request.form['numero_matricula']
        status = request.form['status']
      

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
        UPDATE Estudantes
        SET data_matricula = %s,
            numero_matricula=%s,
            status = %s
           
        WHERE id = %s
        """, (data_matricula,numero_matricula, status, id))
        flash('Estudante foi atualiza com sucesso!')
        conn.commit()
        return redirect(url_for('exibirEstudantes'))
        
### DELETAR DADOS ###
@app.route('/deleteEstudantes/<string:id>', methods = ['POST', 'GET'])
def deleteEstudantes(id):
    cursor.execute(
        'DELETE FROM Estudantes Where id = {0}'.format(id)
    
    )
    cursor.execute(
        'DELETE FROM Pessoa Where id = {0}'.format(id)
    )

    cursor.execute(
        'DELETE FROM Endereco Where id = {0}'.format(id)
    )
    conn.commit()
    flash('Estudante Deletado')
    return redirect(url_for('exibirEstudantes'))
########### ROTA PESSOA #########################


### MOSTRAR DADOS NA TELA ###
@app.route('/exibirPessoa')
def Index():
    cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    sql = "SELECT * FROM Pessoa"
    cursor.execute(sql) #Executar a query do SQL
    lista_pessoa = cursor.fetchall()
    
    return render_template('pessoa.html', lista_pessoa = lista_pessoa)

######  INSERIR DADOS #######

@app.route('/add_pessoa', methods=['POST'])
def add_pessoa():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        genero = request.form['genero']
        cursor.execute("INSERT INTO Pessoa (nome, sobrenome,email, telefone, data_nasc,genero) VALUES (%s,%s,%s,%s,%s,%s)", (nome, sobrenome, email,telefone,data_nasc,genero))
        conn.commit()
        flash('Pessoa cadastrada com sucesso!')
        return redirect(url_for('Index'))
    
### EDITAR DADOS ###

@app.route('/edit/<id>', methods = ['POST', 'GET'])

def get_pessoa(id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM Pessoa WHERE id = %s', (id))
    data = cursor.fetchall()
    print(data[0])
    return render_template('editPessoa.html', pessoa = data[0])

### ATUALIZAR OS DADOS  ###

@app.route('/update/<id>', methods=['POST'])
def update_pessoa(id):
    if request.method == 'POST': 
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        genero = request.form['genero']

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
        UPDATE Pessoa
        SET nome = %s,
            sobrenome=%s,
            email = %s,
            telefone = %s,
            data_nasc = %s,
            genero = %s
        WHERE id = %s
        """, (nome,sobrenome,email,telefone,data_nasc,genero,id))
        flash('Pessoa foi atualiza com sucesso!')
        conn.commit()
        return redirect(url_for('exibirPessoa'))
        
### DELETE ###

@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def delete_student(id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        'DELETE FROM Pessoa Where id = {0}'.format(id)
       
    )
    conn.commit()
    flash('Pessoa Deletada')
    return redirect(url_for('exibirPessoa'))

if __name__ == "__main__":
    app.run(debug=True)
