# 🇦🇴 CliniGest CGE - Sistema de Gestão de Pacientes

O **CliniGest CGE** é um software de gestão e cadastramento clínico desenvolvido de forma nativa e customizada para a realidade do setor de saúde em **Angola**. O sistema oferece uma interface gráfica web moderna, segura e com operação **100% offline**, garantindo alta performance mesmo em ambientes sem conectividade ativa à internet.

---

## 🚀 Funcionalidades Principais (Ciclo CRUD Completo)

- **Cadastro Centralizado CGE:** Captura de dados de identificação padrão de Angola (Bilhete de Identidade - BI, NIF, Províncias e Municípios).
- **Métricas de Efetivos & Consultas:** Campos dedicados para controle de registos de consultas efetuadas, guias médicas solicitadas e data do último atendimento clínico.
- **Perfil do Paciente (Estilo Rede Social):** Visualização individualizada de cada paciente contendo foto em destaque grande, grupo sanguíneo destacado e dados cadastrais unificados.
- **Visualizador de Imagens Nativo:** Miniaturas de fotos dos pacientes integradas na lista com efeito popup modal para expansão em tamanho real ao clicar.
- **Segurança de Credenciais:** Integração protegida via variáveis de ambiente (`.env`) isolando as credenciais de banco de dados do código-fonte.
- **Design 100% Offline:** Layout responsivo otimizado através de Bootstrap embutido localmente nas diretrizes de arquivos estáticos do servidor.

---

## 🛠️ Stack Tecnológica

- **Back-end:** Python 3.11 + Flask (Microframework)
- **Banco de Dados:** PostgreSQL v18 (SGBD Relacional de Alta Performance)
- **Front-end:** HTML5, CSS3 (Estilos customizados e embutidos), JavaScript Puro, Bootstrap 5 (Local/Offline)
- **Conectores e Bibliotecas:** `psycopg2-binary`, `python-dotenv`, `base64`, `webbrowser`
- **Compilador de Distribuição:** PyInstaller (Geração de executáveis portáteis `.exe` independentes)

---

## 🗂️ Estrutura Arquitetural do Projeto

```text
📁 CS_db/
│  ├── 📁 static/
│  │   └── 📄 bootstrap.min.css         # Framework CSS offline integrado
│  ├── 📁 templates/
│  │   ├── 📄 cadastro.html             # Formulário de novos registos
│  │   ├── 📄 editar.html               # Ecrã de atualização de dados
│  │   ├── 📄 lista.html                # Tabela de pacientes com busca e impressão
│  │   └── 📄 perfil.html               # Perfil estendido (Estilo Facebook)
│  ├── 📄 .env                          # Variáveis de ambiente locais (Ignorado pelo Git)
│  ├── 📄 .gitignore                    # Filtros de exclusão para o histórico do Git
│  ├── 📄 app.py                        # Servidor principal, filtros Jinja2 e rotas
│  ├── 📄 criar_banco_angola.sql        # Script DDL de estrutura de tabelas PostgreSQL
│  └── 📄 README.md                     # Documentação oficial do repositório
```

---

## 🔧 Como Rodar em Modo de Desenvolvimento

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com
   cd CliniGest_Angola/CS_db
   ```

2. **Configurar as Variáveis de Ambiente:**
   Crie um arquivo `.env` na raiz da pasta `CS_db` e adicione as suas credenciais:
   ```text
   DB_HOST=localhost
   DB_NAME=cadastro_pacientes
   DB_USER=postgres
   DB_PASSWORD=sua_senha_do_postgresql
   DB_PORT=5432
   FLASK_SECRET=clinigest_angola_secret_key
   ```

3. **Instalar Dependências e Executar:**
   ```bash
   pip install Flask psycopg2-binary python-dotenv
   python app.py
   ```

---

## 📦 Compilação para Distribuição Comercial (.exe)

Para gerar a distribuição autônoma e portátil que esconde a janela do terminal e inicializa o navegador do cliente de forma invisível nos bastidores:

1. Defina `debug=False` no arquivo `app.py`.
2. Execute o comando de compilação no terminal:
   ```bash
   pyinstaller --clean --noconfirm --onedir --windowed --add-data "templates;templates" --add-data "static;static" app.py
   ```
3. Mova o arquivo de produção `.env` do cliente para dentro da pasta gerada em `dist/app/` ao lado do executável `app.exe`.

---

## 📄 Licença e Propriedade

Desenvolvido por **Adilson Eridanio Bernardo Ernesto** [GitHub/Eridanio](https://github.com).  
Todos os direitos reservados. Este software pode ser adaptado, empacotado e comercializado de forma privada sob o modelo de licenciamento local para clínicas e instituições hospitalares.
