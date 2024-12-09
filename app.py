from flask import Flask, render_template, request, redirect, session, send_from_directory
from mysql.connector import Error # Biblioteca que imprimi o erro na tela para uma mehor debug
from config import *
import os
from db_functions import * #Funções do banco de dados

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER']='uploads/'

#Rota da página inicial, todos acessam
@app.route('/')
def index():
    if session:
        if 'adm' in session:
            login = 'adm'
        else:
            login = 'empresa'
    else:
        login = False

    try:
        comandoSQL = '''
        SELECT vaga.*, empresa.nome_empresa 
        FROM vaga 
        JOIN empresa ON vaga.id_empresa = empresa.id_empresa
        WHERE vaga.status = 'ativa'
        ORDER BY vaga.id_vaga DESC;
        '''
        conexao, cursor = conectar_db()
        cursor.execute(comandoSQL)
        vagas = cursor.fetchall()
        return render_template('index.html', vagas=vagas, login=login)
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)

#Rota da página login
# ROTA DA PÁGINA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        if 'adm' in session:
            return redirect('/adm')
        else:
            return redirect('/empresa')

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        if not email or not senha:  # Corrigi aqui para verificar ambos os campos corretamente
            erro = "Os campos precisam estar preenchidos!"
            return render_template('login.html', msg_erro=erro)

        if email == MASTER_EMAIL and senha == MASTER_PASSWORD:
            session['adm'] = True
            return redirect('/adm')

        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'SELECT * FROM empresa WHERE email = %s AND senha = %s'
            cursor.execute(comandoSQL, (email, senha))
            empresa = cursor.fetchone()

            if not empresa:
                return render_template('login.html', msgerro='E-mail e/ou senha estão errados!')

            # Acessar os dados como dicionário
            if empresa['status'] == 'inativa':
                return render_template('login.html', msgerro='Empresa desativada! Procure o administrador!')

            session['id_empresa'] = empresa['id_empresa']
            session['nome_empresa'] = empresa['nome_empresa']
            return redirect('/empresa')
        
        except Error as erro:
            return f"ERRO! Erro de Banco de Dados: {erro}"
        except Exception as erro:
            return f"ERRO! Outros erros: {erro}"
        finally:
            encerrar_db(cursor, conexao)

#ROTA DA PÁGINA DO ADMIN
@app.route('/adm')
def adm():
    #Se não houver sessão ativa
    if not session:
        return redirect('/login')
    #Se não for o administrador
    if not 'adm' in session:
        return redirect('/empresa')
  
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT * FROM Empresa WHERE status = "ativa"'
        cursor.execute(comandoSQL)
        empresas_ativas = cursor.fetchall()

        comandoSQL = 'SELECT * FROM Empresa WHERE status = "inativa"'
        cursor.execute(comandoSQL)
        empresas_inativas = cursor.fetchall()

        return render_template('adm.html', empresas_ativas=empresas_ativas, empresas_inativas=empresas_inativas)
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)

@app.route('/cadastrar_empresa', methods=['POST','GET'])
def cadastrar_empresa():
    # Verifica se tem uma sessão
    if not session:
        return redirect('/login')
    # Se não for o ADM (Deve ser alguma empresa)
    if not 'adm' in session:
        return redirect('/empresa')

    # Acesso ao formulário de cadastro
    if request.method == 'GET':
        return render_template('cadastrar_empresa.html')
    
    # Tratando os dados vindos do formulário
    if request.method == 'POST':
        nome_empresa = request.form['nome_empresa']
        cnpj = limpar_input(request.form['cnpj'])
        telefone = limpar_input(request.form['telefone'])
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se todos os campos estão preenchidos (Em uma situação real seriam adicionados verificações para os campos)
        if not nome_empresa or not cnpj or not telefone or not email or not senha:
            return render_template('cadastro_empresa.html', 
            msg_erro="Todos os campos são obrigatórios")
        
        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'INSERT INTO empresa (nome_empresa,cnpj,telefone,email,senha) VALUES (%s,%s,%s,%s,%s)' # Trata a falha de segurança 'sql injection'
            cursor.execute(comandoSQL, (nome_empresa,cnpj,telefone,email,senha))
            conexao.commit() # Quando usamos comando DML presisa-se usar o commit no BackEnd
            return redirect('/adm')
        except Error as erro:
            if erro.errno == 1062:
                return render_template('cadastrar_empresa.html', msg_erro="Esse E-mail já existe!")
            else:
                return f"Erro de BD: {erro}"
        except Exception as erro:
            return f"Erro de BackEnd: {erro}"
        finally:
            encerrar_db(cursor,conexao)

@app.route('/editar_empresa/<int:id_empresa>', methods=['GET','POST'])
def editar_empresa(id_empresa):
    if not session:
        return redirect('/login')
    
    if not session['adm']:
        return redirect('/login')

    if request.method == 'GET':
        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'SELECT * FROM empresa WHERE id_empresa = %s'
            cursor.execute(comandoSQL, (id_empresa,))
            empresa = cursor.fetchone()
            return render_template('editar_empresa.html',empresa=empresa)
        except Error as erro:
            return f"Erro de BD: {erro}"
        except Exception as erro:
            return f"Erro de BackEnd: {erro}"
        finally:
            encerrar_db(cursor, conexao)
    
        # Tratando os dados vindos do formulário
    if request.method == 'POST':
        nome_empresa = request.form['nome_empresa']
        cnpj = limpar_input(request.form['cnpj'])
        telefone = limpar_input(request.form['telefone'])
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se todos os campos estão preenchidos (Em uma situação real seriam adicionados verificações para os campos)
        if not nome_empresa or not cnpj or not telefone or not email or not senha:
            return render_template('editar_empresa.html', 
            msg_erro="Todos os campos são obrigatórios")
        
        try:
            conexao, cursor = conectar_db()
            comandoSQL = '''
            UPDATE empresa
            SET nome_empresa=%s, cnpj=%s, telefone=%s, email=%s, senha=%s
            WHERE id_empresa = %s;
            '''
            cursor.execute(comandoSQL, (nome_empresa,cnpj,telefone,email,senha,id_empresa))
            conexao.commit() # Quando usamos comando DML presisa-se usar o commit no BackEnd
            return redirect('/adm')
        except Error as erro:
            if erro.errno == 1062:
                return render_template('editar_empresa.html', msg_erro="Esse E-mail já existe!")
            else:
                return f"Erro de BD: {erro}"
        except Exception as erro:
            return f"Erro de BackEnd: {erro}"
        finally:
            encerrar_db(cursor,conexao)

# Rota para ativa/desativar empresa
@app.route('/status_empresa/<int:id_empresa>')
def status(id_empresa):
    if not session:
        return redirect('/login')
    if not session['adm']:
        return redirect('/login')
    
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT status FROM empresa WHERE id_empresa = %s'
        cursor.execute(comandoSQL, (id_empresa,))
        status_empresa = cursor.fetchone()
        if status_empresa['status'] == 'ativa':
            novo_status = 'inativa'
        else:
            novo_status = 'ativa'
        
        comandoSQL = 'UPDATE empresa SET status=%s WHERE id_empresa = %s'
        cursor.execute(comandoSQL, (novo_status, id_empresa))
        conexao.commit()

        # Se a empresa estiver sendo desativada, as vagas também serão
        if novo_status == 'inativa':
            comandoSQL = 'UPDATE vaga SET status = %s WHERE id_empresa = %s'
            cursor.execute(comandoSQL, (novo_status,id_empresa))
            conexao.commit()
        return redirect('/adm')
    except Error as erro:  
        return f"Erro de BD: {erro}"
    except Exception as erro:
        return f"Erro de BackEnd: {erro}"
    finally:
        encerrar_db(cursor, conexao)

@app.route('/excluir_empresa/<int:id_empresa>')
def excluir_empresa(id_empresa):
    #validar sessão
    if not session:
        return redirect('/login')
    if not session['adm']:
        return redirect('/login')
    
    try:
        conexao, cursor = conectar_db()
        #Excluindo as vagas vinculadas a empresa excluida
        comandoSQL = 'DELETE FROM vaga WHERE id_empresa=%s'
        cursor.execute(comandoSQL, (id_empresa,))
        conexao.commit()

        #Excluir cadastro da empresa
        comandoSQL = 'DELETE FROM empresa WHERE id_empresa=%s'
        cursor.execute(comandoSQL, (id_empresa,))
        conexao.commit()
        return redirect('/adm')
    except Error as erro:  
        return f"Erro de BD: {erro}"
    except Exception as erro:
        return f"Erro de BackEnd: {erro}"
    finally:
        encerrar_db(cursor, conexao)

# Rota página da empresa
#ROTA DA PÁGINA DE GESTÃO DAS EMPRESAS
@app.route('/empresa')
def empresa():
    #Verifica se não tem sessão ativa
    if not session:
        return redirect('/login')
    #Verifica se o adm está tentando acessar indevidamente
    if 'adm' in session:
        return redirect('/adm')

    id_empresa = session['id_empresa']
    nome_empresa = session['nome_empresa']

    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT * FROM vaga WHERE id_empresa = %s AND status = "ativa" ORDER BY id_vaga DESC'
        cursor.execute(comandoSQL, (id_empresa,))
        vagas_ativas = cursor.fetchall()

        comandoSQL = 'SELECT * FROM vaga WHERE id_empresa = %s AND status = "inativa" ORDER BY id_vaga DESC'
        cursor.execute(comandoSQL, (id_empresa,))
        vagas_inativas = cursor.fetchall()

        return render_template('empresa.html', nome_empresa=nome_empresa, vagas_ativas=vagas_ativas, vagas_inativas=vagas_inativas)         
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)

# Rota de logout (encerra a sessão)
@app.route('/logout')
def logout():
    #logout
    session.clear()
    return redirect('/')

@app.route('/cadastrar_vaga', methods=['POST','GET'])
def cadastrar_vaga():
    #Verifica se não tem sessão ativa
    if not session:
        return redirect('/login')
    #Verifica se o adm está tentando acessar indevidamente
    if 'adm' in session:
        return redirect('/adm')
    
    if request.method == 'GET':
        return render_template('cadastrar_vaga.html')
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        formato = request.form['formato']
        tipo = request.form['tipo']
        local = ''
        local = request.form['local']
        salario = ''
        salario = limpar_input(request.form['salario'])
        id_empresa = session['id_empresa']

        if not titulo or not descricao or not formato or not tipo:
            return render_template('cadastrar_vaga.html', msg_erro="Os campos obrigatório precisam estar preenchidos!")
        
        try:
            conexao, cursor = conectar_db()
            comandoSQL = '''
            INSERT INTO Vaga (titulo, descricao, formato, tipo, local, salario, id_empresa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(comandoSQL, (titulo, descricao, formato, tipo, local, salario, id_empresa))
            conexao.commit()
            return redirect('/empresa')
        except Error as erro:
            return f"ERRO! Erro de Banco de Dados: {erro}"
        except Exception as erro:
            return f"ERRO! Outros erros: {erro}"
        finally:
            encerrar_db(cursor, conexao)

#ROTA PARA VER DETALHES DA VAGA
@app.route('/sobre_vaga/<int:id_vaga>')
def sobre_vaga(id_vaga):
    try:
        comandoSQL = '''
        SELECT vaga.*, empresa.nome_empresa 
        FROM vaga 
        JOIN empresa ON vaga.id_empresa = empresa.id_empresa 
        WHERE vaga.id_vaga = %s;
        '''
        conexao, cursor = conectar_db()
        cursor.execute(comandoSQL, (id_vaga,))
        vaga = cursor.fetchone()
        
        if not vaga:
            return redirect('/')
        
        return render_template('sobre_vaga.html', vaga=vaga)
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)

#ROTA PARA EDITAR A VAGA
@app.route('/editar_vaga/<int:id_vaga>', methods=['GET','POST'])
def editarvaga(id_vaga):
    #Verifica se não tem sessão ativa
    if not session:
        return redirect('/login')
    #Verifica se o adm está tentando acessar indevidamente
    if 'adm' in session:
        return redirect('/adm')

    if request.method == 'GET':
        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'SELECT * FROM vaga WHERE id_vaga = %s;'
            cursor.execute(comandoSQL, (id_vaga,))
            vaga = cursor.fetchone()
            return render_template('editar_vaga.html', vaga=vaga)
        except Error as erro:
            return f"ERRO! Erro de Banco de Dados: {erro}"
        except Exception as erro:
            return f"ERRO! Outros erros: {erro}"
        finally:
            encerrar_db(cursor, conexao)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        formato = request.form['formato']
        tipo = request.form['tipo']
        local = request.form['local']
        salario = limpar_input(request.form['salario'])

        if not titulo or not descricao or not formato or not tipo:
            return redirect('/empresa')
        
        try:
            conexao, cursor = conectar_db()
            comandoSQL = '''
            UPDATE vaga SET titulo=%s, descricao=%s, formato=%s, tipo=%s, local=%s, salario=%s
            WHERE id_vaga = %s;
            '''
            cursor.execute(comandoSQL, (titulo, descricao, formato, tipo, local, salario, id_vaga))
            conexao.commit()
            return redirect('/empresa')
        except Error as erro:
            return f"ERRO! Erro de Banco de Dados: {erro}"
        except Exception as erro:
            return f"ERRO! Outros erros: {erro}"
        finally:
            encerrar_db(cursor, conexao)

#ROTA PARA ALTERAR O STATUS DA VAGA
@app.route("/status_vaga/<int:id_vaga>")
def statusvaga(id_vaga):
    #Verifica se não tem sessão ativa
    if not session:
        return redirect('/login')
    #Verifica se o adm está tentando acessar indevidamente
    if 'adm' in session:
        return redirect('/adm')

    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT status FROM vaga WHERE id_vaga = %s;'
        cursor.execute(comandoSQL, (id_vaga,))
        vaga = cursor.fetchone()
        if vaga['status'] == 'ativa':
            status = 'inativa'
        else:
            status = 'ativa'

        comandoSQL = 'UPDATE vaga SET status = %s WHERE id_vaga = %s'
        cursor.execute(comandoSQL, (status, id_vaga))
        conexao.commit()
        return redirect('/empresa')
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)
#ROTA PARA EXCLUIR VAGA
@app.route("/excluir_vaga/<int:id_vaga>")
def excluirvaga(id_vaga):
    #Verifica se não tem sessão ativa
    if not session:
        return redirect('/login')
    #Verifica se o adm está tentando acessar indevidamente
    if 'adm' in session:
        return redirect('/adm')

    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'delete from candidatura where id_vaga = %s'
        cursor.execute(comandoSQL, (id_vaga,))
        conexao.commit()
        comandoSQL = 'DELETE FROM vaga WHERE id_vaga = %s AND status = "inativa"'
        cursor.execute(comandoSQL, (id_vaga,))
        conexao.commit()
        return redirect('/empresa')
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)

@app.route('/procurar_vagas')
def procurar_vagas():
    try:
        word = request.args.get('word')  
        comandoSQL = '''    
        select vaga.*, empresa.nome_empresa 
        from vaga 
        join empresa on vaga.id_empresa = empresa.id_empresa
        where vaga.titulo like %s and vaga.status = 'ativa'
        order by vaga.id_vaga desc;
        '''
        conexao, cursor = conectar_db()
        cursor.execute(comandoSQL, (f"%{word}%",)) 
        vagas_buscadas = cursor.fetchall()
        return render_template('buscar_vaga.html', vagas=vagas_buscadas, word=word)
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)

@app.route('/candidatar_vaga/<int:id_vaga>', methods=['GET', 'POST'])
def candidatar_vaga(id_vaga):
    try:
        conexao, cursor = conectar_db()
        comandoSQL = """SELECT * FROM vaga WHERE id_vaga = %s"""
        cursor.execute(comandoSQL, (id_vaga,))
        vaga = cursor.fetchone()

        if not vaga:
            return "Vaga não encontrada!", 404 # retorna um erro 404 not found

        if request.method == 'GET':
            return render_template('candidatar_vaga.html', id_vaga=id_vaga, vaga=vaga)

        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            telefone = limpar_input(request.form['telefone'])
            file = request.files['curriculo']
            mensagem = request.form['mensagem']

            if not email or not nome or not file or not telefone:
                return render_template('candidatar_vaga.html', msg_erro="Os campos obrigatórios precisam estar preenchidos!", vaga=vaga), 400 # erro 400 bad request

            try:
                nome_arquivo = f"{id_vaga}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))
                comandoSQL = '''INSERT INTO candidatura (nome, email, telefone, curriculo, mensagem, id_vaga, id_empresa) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(comandoSQL, (nome, email, telefone, nome_arquivo, mensagem, id_vaga, vaga['id_empresa']))
                conexao.commit()
                return render_template('confirmacao_candidatura.html')

            except mysql.connector.Error as erro:
                return f"ERRO! Erro de Banco de Dados: {erro}", 500 # erro 500 internal server error
            except IOError as erro:
                return f"ERRO! Erro ao salvar o currículo: {erro}", 500
            except Exception as erro:
                return f"ERRO! Outros erros: {erro}", 500

    except mysql.connector.Error as erro:
        return f"ERRO! Erro de conexão com o banco de dados: {erro}", 500
    except Exception as erro:
        return f"ERRO! Erro inesperado: {erro}", 500
    finally:
        encerrar_db(cursor, conexao)

@app.route('/candidatos/<int:id_vaga>')
def ver_candidatos(id_vaga):
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT * FROM candidatura WHERE id_vaga = %s'
        cursor.execute(comandoSQL, (id_vaga,))
        candidatos = cursor.fetchall()
        return render_template('candidatos.html', candidatura=candidatos)
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)

@app.route('/download/<filename>')
def download_filename(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<int:id_candidatura>')
def delete_file(id_candidatura):
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT curriculo, id_vaga FROM candidatura WHERE id_candidatura = %s'
        cursor.execute(comandoSQL, (id_candidatura,))
        candidatura = cursor.fetchone()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], candidatura['curriculo']))
        comandoSQL = 'DELETE FROM candidatura WHERE id_candidatura = %s'
        cursor.execute(comandoSQL, (id_candidatura,))
        conexao.commit()
        return redirect(f"/candidatos/{candidatura['id_vaga']}")
    except Error as erro:
        return f"ERRO! Erro de Banco de Dados: {erro}"
    except Exception as erro:
        return f"ERRO! Outros erros: {erro}"
    finally:
        encerrar_db(cursor, conexao)
    
# Final do código
if __name__ == '__main__':
    app.run(debug=True)