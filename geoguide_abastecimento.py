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
st.title("⛽ Consulta de Geoguide v2.0")

# Configurações iniciais de sessão
if "data_ini" not in st.session_state:
    st.session_state["data_ini"] = date.today()
if "data_fim" not in st.session_state:
    st.session_state["data_fim"] = date.today()
if "comboio" not in st.session_state:
    st.session_state["comboio"] = ""
if "bomba" not in st.session_state:
    st.session_state["bomba"] = ""

st.sidebar.header("🧭 Fonte de Dados")
fonte_dados = st.sidebar.selectbox("Escolha a origem dos dados:", options=["Abastecimento", "Estoque"])

# Filtros
with st.sidebar:
    st.header("📅 Filtros")

    data_ini = st.date_input("Data Inicial", value=st.session_state["data_ini"])
    data_fim = st.date_input("Data Final", value=st.session_state["data_fim"])

    if fonte_dados == "Abastecimento":
        comboio = st.text_input("Comboio (Opcional)", value=st.session_state["comboio"])

        bomba = st.text_input("Bomba (Opcional)", value=st.session_state["bomba"])
        bomba = bomba.upper()
        st.session_state["bomba"] = bomba

        codigo_material = None

    if fonte_dados == "Estoque":
        comboio = ""
        bomba = ""
        opcoes_material = {
            "Diesel": "637577",
            "ARLA": "637578",     
        }
        material_selecionado = st.selectbox("Material", options=list(opcoes_material.keys()))
        codigo_material = opcoes_material[material_selecionado]

    if st.button("Salvar Filtros"):
        st.session_state["data_ini"] = data_ini
        st.session_state["data_fim"] = data_fim
        st.session_state["comboio"] = comboio
        st.session_state["bomba"] = bomba
        st.success("Filtros salvos na sessão.")

# Consulta
if st.button("Consultar Dados"):
    with st.spinner("Consultando base ..."):
        try:
            conn = get_connection()

            # Opção A - Abastecimento
            if fonte_dados == "Abastecimento":

                query = """
                    SELECT instante, frota, quantidade, motorista,
                        frentista, odometro, horimetro,
                        encerrante, bomba, comboio,qt_arla,
                            integrado, log_integracao
                    FROM usa.ggabastecimentos
                    WHERE data BETWEEN %s AND %s
                """

                params = [data_ini, data_fim]

                if comboio.strip():
                    query += " AND comboio = %s"
                    params.append(comboio.strip())

                if bomba.strip():
                    query += " AND bomba = %s"
                    params.append(bomba.strip())

                query += " ORDER BY data DESC, hora DESC"
            
            elif fonte_dados == "Estoque":
                query = '''
                SELECT A.data, A.deposito, 
                       B.equipe, B.descricao, B.frota,
                       A.quantidade
                FROM usa.estoque AS A
                LEFT JOIN usa.equipe_abastecimento AS B
                     ON A.deposito = B.deposito
                WHERE material = %s
                    AND "data" BETWEEN %s AND %s
                ORDER BY "data" DESC
            '''
                params = [codigo_material, data_ini, data_fim]

            df = pd.read_sql(query, conn, params=params)
            conn.close()

            if fonte_dados == "Abastecimento" and "instante" in df.columns:
                df["instante"] = pd.to_datetime(df["instante"], errors="coerce")

            if fonte_dados == "Estoque":
                df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")

            if df.empty:
                st.warning("Nenhum registro encontrado.")
            else:
                st.success(f"{len(df)} registros encontrados.")
                st.dataframe(
                    df,
                    column_config={
                        "instante": st.column_config.DatetimeColumn(
                            "instante", format="DD/MM/YYYY HH:mm:ss"
                        ),
                        
                    },
                    use_container_width=True,    
                )

                if fonte_dados == "Abastecimento" and "quantidade" in df.columns:
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

                    if fonte_dados == "Abastecimento":
                        sheet_name = "Abastecimentos"
                        file_stub = "abastecimentos"
                    
                    else:
                        sheet_name = f"Estoque - {material_selecionado}"
                        file_stub = f"estoque_{material_selecionado.lower()}"

                    file_name = f"{file_stub}_{data_ini.strftime('%Y%m%d')}_{data_fim.strftime('%Y%m%d')}.xlsx"

                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name=sheet_name)
                        ws = writer.sheets[sheet_name]
                        
                        def apply_number_format(col_name, fmt):
                            if col_name in df.columns:
                                cidx = df.columns.get_loc(col_name) + 1
                                for r in range(2, len(df) + 2):
                                    ws.cell(row=r, column=cidx).number_format = fmt

                        apply_number_format("instante", "dd/mm/yyyy hh:mm:ss")

                       

                    output.seek(0)

                    st.download_button(
                        label="📤 Baixar .xlsx",
                        data=output,
                        file_name=file_name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        except Exception as e:
            st.error("Erro ao conectar ou consultar o banco.")
            st.exception(e)
