# ⛽ Consulta de Abastecimentos - Streamlit + PostgreSQL

Este projeto é uma aplicação desenvolvida em **Python** com **Streamlit**, que permite consultar dados de abastecimentos registrados em um banco de dados **PostgreSQL**. A interface é simples, responsiva e permite aplicar filtros, visualizar resultados e exportar os dados para Excel.

---

## 🚀 Funcionalidades

- Filtro por **data inicial** e **data final**
- Filtro opcional por **comboio**
- Apresentação dos dados em formato de tabela
- Ordenação automática por **data e hora decrescentes**
- Exibição do **total de quantidade abastecida**
- Exportação dos dados para **arquivo Excel (.xlsx)**

---

## 🧰 Bibliotecas Utilizadas

| Biblioteca     | Função Principal                                       |
|----------------|--------------------------------------------------------|
| `streamlit`    | Criação da interface web de forma simples e interativa |
| `pandas`       | Manipulação de dados e estrutura tabular               |
| `psycopg2`     | Conexão com banco de dados PostgreSQL                  |
| `openpyxl`     | Exportação de DataFrames para arquivos `.xlsx`         |

Instale todas as dependências com:

```bash
pip install -r requirements.txt
```

---

## 📂 Estrutura do Projeto

```
geoguide_app/
├── main.py                 # Código principal da aplicação
├── requirements.txt        # Lista de dependências do projeto
└── .streamlit/
    └── secrets.toml        # Credenciais do banco (não versionar!)
```

---

## 🔐 Configuração de credenciais

Crie o arquivo `.streamlit/secrets.toml` com suas credenciais PostgreSQL:

```toml
[postgres]
host = "endereço_do_banco"
port = porta do banco
database = "geoguide"
user = "seu_usuario"
password = "sua_senha"
```

> ⚠️ **Importante**: Nunca envie esse arquivo para repositórios públicos.

---

## ▶️ Como executar

No terminal, dentro da pasta do projeto:

```bash
streamlit run geoguide_abastecimento.py
```

A aplicação será iniciada no navegador padrão, geralmente em `http://localhost:8501`.

---

## 📝 Licença

Este projeto é de uso interno da Usina Santo Angelo. 
