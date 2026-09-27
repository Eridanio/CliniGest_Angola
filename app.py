import base64
import os
import sys
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, 'templates'),
    static_folder=os.path.join(base_dir, 'static')
)
app.secret_key = os.getenv("FLASK_SECRET", "cliniguest_angola_secret_key")

def obter_conexao():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "cadastro_pacientes"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data:
        if isinstance(data, (bytes, bytearray)):
            return base64.b64encode(data).decode('utf-8')
        elif hasattr(data, 'tobytes'):
            return base64.b64encode(data.tobytes()).decode('utf-8')
    return None

@app.route('/')
def index():
    nome_hospital = os.getenv("CLINICA_NOME", "CliniGuest Angola")
    return render_template('cadastro.html', nome_clinica=nome_hospital)

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
    
    nome_hospital = os.getenv("CLINICA_NOME", "CliniGuest Angola")
    return render_template('lista.html', pacientes=lista, nome_clinica=nome_hospital)

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
        
        tipo_sangue = request.form['tipo_sanguineo'] or None
        consultas = request.form['total_consultas'] or 0
        guias = request.form['guias_solicitadas'] or 0
        data_cons = request.form['data_consulta'] or None
        
        foto_arquivo = request.files.get('foto_paciente')
        foto_bytes = foto_arquivo.read() if foto_arquivo and foto_arquivo.filename != '' else None

        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO pacientes (
                nome_paciente, sexo, data_nascimento, bi_identidade, nif, seguro_saude, 
                telemovel_principal, telemovel_alternativo, nome_pai, nome_mae, bairro, municipio, provincia, 
                observacoes_medicas, foto_paciente, tipo_sanguineo, total_consultas, guias_solicitadas, data_consulta
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, sexo, data_nasc, bi, nif, seguro, tel_1, tel_2, nome_pai, nome_mae, bairro, municipio, provincia, obs, foto_bytes, tipo_sangue, consultas, guias, data_cons))
        
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('lista_pacientes'))

@app.route('/perfil/<int:codigo>')
def perfil_paciente(codigo):
    conexao = obter_conexao()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT codigo, nome_paciente, sexo, data_nascimento, bi_identidade, nif, seguro_saude, 
               telemovel_principal, telemovel_alternativo, nome_pai, nome_mae, bairro, municipio, 
               provincia, observacoes_medicas, foto_paciente, tipo_sanguineo, total_consultas, guias_solicitadas, data_consulta
        FROM pacientes WHERE codigo = %s
    """, (codigo,))
    paciente = cursor.fetchone()
    cursor.close()
    conexao.close()
    
    nome_hospital = os.getenv("CLINICA_NOME", "CliniGuest Angola")
    return render_template('perfil.html', p=paciente, nome_clinica=nome_hospital)

@app.route('/editar/<int:codigo>')
def editar_paciente(codigo):
    conexao = obter_conexao()
    cursor = conexao.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT codigo, nome_paciente, sexo, data_nascimento, bi_identidade, nif, seguro_saude, 
               telemovel_principal, telemovel_alternativo, nome_pai, nome_mae, bairro, municipio, 
               provincia, observacoes_medicas, tipo_sanguineo, total_consultas, guias_solicitadas, data_consulta
        FROM pacientes WHERE codigo = %s
    """, (codigo,))
    paciente = cursor.fetchone()
    cursor.close()
    conexao.close()
    
    nome_hospital = os.getenv("CLINICA_NOME", "CliniGuest Angola")
    return render_template('editar.html', p=paciente, nome_clinica=nome_hospital)

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
    mae = request.form['nome_mae'] or None
    bairro = request.form['bairro'] or None
    municipio = request.form['municipio'] or None
    provincia = request.form['provincia'] or None
    obs = request.form['observacoes_medicas'] or None
    
    tipo_sangue = request.form['tipo_sanguineo'] or None
    consultas = request.form['total_consultas'] or 0
    guias = request.form['guias_solicitadas'] or 0
    data_cons = request.form['data_consulta'] or None

    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    foto_arquivo = request.files.get('foto_paciente')
    if foto_arquivo and foto_arquivo.filename != '':
        foto_bytes = foto_arquivo.read()
        cursor.execute("""
            UPDATE pacientes SET 
                nome_paciente=%s, sexo=%s, data_nascimento=%s, bi_identidade=%s, nif=%s, seguro_saude=%s, 
                telemovel_principal=%s, telemovel_alternativo=%s, nome_pai=%s, nome_mae=%s, bairro=%s, municipio=%s, provincia=%s, 
                observacoes_medicas=%s, foto_paciente=%s, tipo_sanguineo=%s, total_consultas=%s, guias_solicitadas=%s, data_consulta=%s
            WHERE codigo=%s
        """, (nome, sexo, data_nasc, bi, nif, seguro, tel_1, tel_2, nome_pai, mae, bairro, municipio, provincia, obs, foto_bytes, tipo_sangue, consultas, guias, data_cons, codigo))
    else:
        cursor.execute("""
            UPDATE pacientes SET 
                nome_paciente=%s, sexo=%s, data_nascimento=%s, bi_identidade=%s, nif=%s, seguro_saude=%s, 
                telemovel_principal=%s, telemovel_alternativo=%s, nome_pai=%s, nome_mae=%s, bairro=%s, municipio=%s, provincia=%s, 
                observacoes_medicas=%s, tipo_sanguineo=%s, total_consultas=%s, guias_solicitadas=%s, data_consulta=%s
            WHERE codigo=%s
        """, (nome, sexo, data_nasc, bi, nif, seguro, tel_1, tel_2, nome_pai, mae, bairro, municipio, provincia, obs, tipo_sangue, consultas, guias, data_cons, codigo))
        
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

from cryptography.fernet import Fernet
from datetime import datetime
from flask import redirect, url_for, request
import os

# A assinatura secreta tem de ser EXATAMENTE igual à do gerador
CHAVE_MESTRA = b'oOMfM4mgILQkjCcbxA3pX116WOOuwvEaAB5OMBbs0oM='
fernet = Fernet(CHAVE_MESTRA)

@app.before_request
def verificar_licenca():
    if request.endpoint in ['licenca_expirada', 'static']:
        return None
        
    # Agora lemos a CHAVE_LICENCA complexa enviada por si
    chave_licenca = os.getenv("CHAVE_LICENCA")
    
    if not chave_licenca:
        return redirect(url_for('licenca_expirada'))
        
    try:
        # Tenta descriptografar a chave para extrair a data real escondida
        data_descriptografada = fernet.decrypt(chave_licenca.encode('utf-8')).decode('utf-8')
        data_limite = datetime.strptime(data_descriptografada.strip(), "%Y-%m-%d").date()
        data_atual = datetime.now().date()
        
        # Bloqueia se o tempo do contrato terminar
        if data_atual > data_limite:
            return redirect(url_for('licenca_expirada'))
            
    except Exception:
        # Se tentarem alterar o texto da chave ou sabotar, o sistema tranca por segurança
        return redirect(url_for('licenca_expirada'))
        
    return None


if __name__ == '__main__':
    import webbrowser
    from threading import Timer
    def abrir_navegador():
        webbrowser.open_new("http://127.0.0.1:5000")
    Timer(1.5, abrir_navegador).start()
    app.run(debug=False)
