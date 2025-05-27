
# ⛽ Consulta Geoguide v2.0

Aplicação web em Python com Streamlit para consultar e exportar dados de **abastecimentos** e **estoques** a partir de um banco de dados PostgreSQL.

---

## 🔧 Funcionalidades

- Consulta por **Data Inicial** e **Data Final**
- Filtros opcionais por **Comboio** e **Bomba** (apenas para abastecimento)
- Consulta de estoque por **material** (Diesel ou ARLA)
- Exibição dos resultados em tabela
- Exportação dos dados para **Excel (.xlsx)** com botão de download

---

## 🧱 Requisitos

- Python 3.9 ou superior
- Banco de dados PostgreSQL com as tabelas:
  - `usa.ggabastecimentos`
  - `usa.estoque`
- Dependências Python (instale com `pip` abaixo)

---

## 📦 Instalação

Clone este repositório e instale os pacotes necessários:

```bash
git clone https://github.com/seuusuario/consulta-geoguide.git
cd consulta-geoguide

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

Crie o arquivo `.streamlit/secrets.toml` com as credenciais do banco:

```toml
[postgres]
host = "seu_host"
port = 5432
database = "nome_do_banco"
user = "seu_usuario"
password = "sua_senha"
```

---

## ▶️ Execução

Inicie o app com:

```bash
streamlit run nome_do_arquivo.py
```

Exemplo:

```bash
streamlit run geoguide_abastecimento.py

```
É possível também executar via GeoGuide.bat (preferencial)
---

## 🖥️ Interface

### 🔍 Fonte de Dados

- `Abastecimento`: mostra os campos comboio e bomba (opcionais)
- `Estoque`: permite escolher entre Diesel (637577) ou ARLA (637578)

### 📅 Filtros

- **Data Inicial / Final**: obrigatórios para ambas as consultas

### 📤 Exportação

- Resultados podem ser baixados como `.xlsx`

---

## 📁 Estrutura esperada do banco

### Tabela `usa.ggabastecimentos`

| Coluna        | Tipo esperado      |
|---------------|--------------------|
| data          | DATE               |
| hora          | TIME or VARCHAR    |
| frota         | VARCHAR            |
| quantidade    | NUMERIC            |
| motorista     | VARCHAR            |
| frentista     | VARCHAR            |
| odometro      | NUMERIC            |
| horimetro     | NUMERIC            |
| encerrante    | VARCHAR            |
| bomba         | VARCHAR            |
| comboio       | VARCHAR            |
| qt_arla       | NUMERIC            |
| integrado     | BOOLEAN / CHAR     |
| log_integracao| TEXT               |

### Tabela `usa.estoque`

| Coluna     | Tipo esperado      |
|------------|--------------------|
| id         | SERIAL / INT       |
| material   | VARCHAR / NUMERIC  |
| deposito   | VARCHAR            |
| data       | DATE               |
| quantidade | NUMERIC            |

---

## 🛠️ Dependências

```text
streamlit
pandas
psycopg2-binary
openpyxl
```

Crie um `requirements.txt` com:

```txt
streamlit
pandas
psycopg2-binary
openpyxl
```

---

---

## 🙋‍♂️ Suporte

Em caso de dúvidas, entre em contato com [randerpaula2@gmail.com].
