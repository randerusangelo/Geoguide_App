import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import date
import io

# Conexão
def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        dbname=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )

# Interface
st.set_page_config(page_title="Consulta Geoguide", layout="wide")
st.title("⛽ Consulta de Abastecimentos Geoguide")

# Configurações iniciais de sessão
if "data_ini" not in st.session_state:
    st.session_state["data_ini"] = date.today().replace(day=1)
if "data_fim" not in st.session_state:
    st.session_state["data_fim"] = date.today()
if "comboio" not in st.session_state:
    st.session_state["comboio"] = ""

# Filtros
with st.sidebar:
    st.header("📅 Filtros")

    data_ini = st.date_input("Data Inicial", value=date.today().replace(day=1))
    data_fim = st.date_input("Data Final", value=date.today())
    comboio = st.text_input("Comboio (Opcional)", value=st.session_state["comboio"])

    if st.button("Salvar Filtros"):
        st.session_state["data_ini"] = data_ini
        st.session_state["data_fim"] = data_fim
        st.session_state["comboio"] = comboio
        st.success("Filtros salvos na sessão.")

# Consulta
if st.button("Consultar Dados"):
    with st.spinner("Consultando base ..."):
        try:
            conn = get_connection()
            query = """
                SELECT data, hora, frota, quantidade, motorista,
                       frentista, odometro, horimetro,
                       encerrante, bomba, comboio, log_integracao
                FROM usa.ggabastecimentos
                WHERE data BETWEEN %s AND %s
            """

            params = [data_ini, data_fim]

            if comboio.strip():
                query += " AND comboio = %s"
                params.append(comboio.strip())

            query += " ORDER BY data DESC, hora DESC"

            df = pd.read_sql(query, conn, params=params)
            conn.close()

            df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")

            if df.empty:
                st.warning("Nenhum registro encontrado.")
            else:
                st.success(f"{len(df)} registros encontrados.")
                st.dataframe(df)
                if "quantidade" in df.columns:
                    try:
                        total_quant = pd.to_numeric(df["quantidade"], errors="coerce").sum()
                        st.markdown(f"""
                        <div style="text-align:right; font-size:18px; padding-top:10px;">
                            <b>📦 Total de quantidade:</b> {total_quant:,.2f} L
                        </div>
                        """, unsafe_allow_html=True)
                    except:
                        pass

                with st.expander("📥 Exportar para Excel"):
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Abastecimentos")
                    output.seek(0)

                    st.download_button(
                        label="📤 Baixar .xlsx",
                        data=output,
                        file_name="abastecimentos.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        except Exception as e:
            st.error("Erro ao conectar ou consultar o banco.")
            st.exception(e)
