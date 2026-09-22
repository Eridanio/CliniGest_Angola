import base64
import os
import sys
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Lógica essencial para o PyInstaller localizar as pastas HTML e CSS dentro do executável
if getattr(sys, 'frozen', False):
    # Se o app estiver rodando como executável (.exe)
    base_dir = sys._MEIPASS
else:
    # Se o app estiver rodando como script Python normal
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Cria o Flask apontando explicitamente para os caminhos dinâmicos das pastas
app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, 'templates'),
    static_folder=os.path.join(base_dir, 'static')
)
app.secret_key = os.getenv("FLASK_SECRET", "clinigest_angola_secret_key")

# ... O resto da sua função obter_conexao() e rotas continua exatamente igual abaixo


# Configuração Otimizada e Protegida de Conexão com o PostgreSQL
def obter_conexao():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "cadastro_pacientes"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"), # Lê diretamente da máquina, sem expor no código!
        port=os.getenv("DB_PORT", "5432")
    )

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return None

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/lista')
def lista_pacientes():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT codigo, nome_paciente, bi_identidade, telemovel_principal, municipio, provincia, seguro_saude, foto_paciente 
        FROM pacientes 
        ORDER BY codigo DESC
    """)
    lista = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template('lista.html', pacientes=lista)

@app.route('/salvar', methods=['POST'])
def salvar_paciente():
    if request.method == 'POST':
        nome = request.form['nome_paciente']
        sexo = request.form['sexo']
        data_nasc = request.form['data_nascimento'] or None
        bi = request.form['bi_identidade']
        nif = request.form['nif'] or None
        seguro = request.form['seguro_saude'] or None
        tel_1 = request.form['telemovel_principal'] or None
        tel_2 = request.form['telemovel_alternativo'] or None
        nome_pai = request.form['nome_pai'] or None
        nome_mae = request.form['nome_mae'] or None
        bairro = request.form['bairro'] or None
        municipio = request.form['municipio'] or None
        provincia = request.form['provincia'] or None
        obs = request.form['observacoes_medicas'] or None
        
        foto_arquivo = request.files.get('foto_paciente')
        foto_bytes = foto_arquivo.read() if foto_arquivo and foto_arquivo.filename != '' else None

        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO pacientes (
                nome_paciente, sexo, data_nascimento, bi_identidade, nif, seguro_saude, 
                telemovel_principal, telemovel_alternativo, nome_pai, nome_mae, bairro, municipio, provincia, 
                observacoes_medicas, foto_paciente
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, sexo, data_nasc, bi, nif, seguro, tel_1, tel_2, nome_pai, nome_mae, bairro, municipio, provincia, obs, foto_bytes))
        
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('lista_pacientes'))

# NOVA ROTA: Abrir a tela de edição preenchida
@app.route('/editar/<int:codigo>')
def editar_paciente(codigo):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT codigo, nome_paciente, sexo, data_nascimento, bi_identidade, nif, seguro_saude, 
               telemovel_principal, telemovel_alternativo, nome_pai, nome_mae, bairro, municipio, provincia, observacoes_medicas
        FROM pacientes WHERE codigo = %s
    """, (codigo,))
    paciente = cursor.fetchone()
    cursor.close()
    conexao.close()
    return render_template('editar.html', p=paciente)

# NOVA ROTA: Gravar as alterações feitas na edição
@app.route('/atualizar/<int:codigo>', methods=['POST'])
def atualizar_paciente(codigo):
    nome = request.form['nome_paciente']
    sexo = request.form['sexo']
    data_nasc = request.form['data_nascimento'] or None
    bi = request.form['bi_identidade']
    nif = request.form['nif'] or None
    seguro = request.form['seguro_saude'] or None
    tel_1 = request.form['telemovel_principal'] or None
    tel_2 = request.form['telemovel_alternativo'] or None
    nome_pai = request.form['nome_pai'] or None
    nome_mae = request.form['nome_mae'] or None
    bairro = request.form['bairro'] or None
    municipio = request.form['municipio'] or None
    provincia = request.form['provincia'] or None
    obs = request.form['observacoes_medicas'] or None

    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    # Verifica se uma nova foto foi enviada
    foto_arquivo = request.files.get('foto_paciente')
    if foto_arquivo and foto_arquivo.filename != '':
        foto_bytes = foto_arquivo.read()
        cursor.execute("""
            UPDATE pacientes SET 
                nome_paciente=%s, sexo=%s, data_nascimento=%s, bi_identidade=%s, nif=%s, seguro_saude=%s, 
                telemovel_principal=%s, telemovel_alternativo=%s, nome_pai=%s, nome_mae=%s, bairro=%s, municipio=%s, provincia=%s, 
                observacoes_medicas=%s, foto_paciente=%s
            WHERE codigo=%s
        """, (nome, sexo, data_nasc, bi, nif, seguro, tel_1, tel_2, nome_pai, nome_mae, bairro, municipio, provincia, obs, foto_bytes, codigo))
    else:
        cursor.execute("""
            UPDATE pacientes SET 
                nome_paciente=%s, sexo=%s, data_nascimento=%s, bi_identidade=%s, nif=%s, seguro_saude=%s, 
                telemovel_principal=%s, telemovel_alternativo=%s, nome_pai=%s, nome_mae=%s, bairro=%s, municipio=%s, provincia=%s, 
                observacoes_medicas=%s
            WHERE codigo=%s
        """, (nome, sexo, data_nasc, bi, nif, seguro, tel_1, tel_2, nome_pai, nome_mae, bairro, municipio, provincia, obs, codigo))
        
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect(url_for('lista_pacientes'))

@app.route('/eliminar/<int:codigo>')
def eliminar_paciente(codigo):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pacientes WHERE codigo = %s", (codigo,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect(url_for('lista_pacientes'))

if __name__ == '__main__':
    import webbrowser
    from threading import Timer

    def abrir_navegador():
        webbrowser.open_new("http://127.0.0.1:5000")

    Timer(1.5, abrir_navegador).start()
    app.run(debug=False) # Garanta que está False aqui!
