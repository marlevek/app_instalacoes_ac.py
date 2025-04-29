import streamlit as st
import pandas as pd
from fpdf import FPDF
from sqlalchemy import create_engine 

st.set_page_config('instalacao-ar-condicionado', page_icon=':memo:')
st.title('Dados Instalação AC :male-mechanic:')

# Nome do cliente
cliente = st.text_input('Cliente')

# Qtde aparelhos
qtd_aparelhos = st.selectbox('Quantidade de aparelhos', list(range(1, 11)))

# Lista para armazenar dados
aparelhos = []

# Formulário dinâmico
for i in range(qtd_aparelhos):
    st.markdown(f'### Aparelho {i + 1}')
    marca_modelo = st.text_input(f'Marca e Modelo AC', key=f'marca_modelo_{i}')
    
    st.subheader('EVAPORADORA')
    ambiente = st.text_input("Ambiente de instalação", key=f"ambiente_{i}")
    dist_chao_evap = st.number_input("Distância do chão (m)", key=f"dist_chao_evap_{i}")
    dist_teto_evap = st.number_input("Distância do teto (m)", key=f"dist_teto_evap_{i}")
    tipo_parede_evap = st.selectbox(
        "Tipo de parede (Evaporadora)",
        ["Concreto", "Alvenaria", "Drywall", "Madeira"],
        key=f"tipo_parede_evap_{i}"
    )
    espessura_parede = st.number_input("Espessura da parede (cm)", key=f"espessura_{i}")

    st.subheader("CONDENSADORA")
    local_condensadora = st.selectbox(
        "Local da instalação",
        ["Telhado", "Parede", "Área Técnica", "Chão"],
        key=f"local_condensadora_{i}"
    )
    dist_chao_cond = st.number_input("Distância do chão (m)", key=f"dist_chao_cond_{i}")
    tipo_telhado = st.text_input("Tipo de telhado", key=f"tipo_telhado_{i}")
    tipo_parede_cond = st.text_input("Tipo de parede (Condensadora)", key=f"tipo_parede_cond_{i}")
    area_tecnica = st.number_input("Área Técnica (m²)", key=f"area_tecnica_{i}")

    st.subheader("DIVERSOS")
    metros_tubulacao = st.number_input("Metros de tubulação", key=f"tubulacao_{i}")
    uso_guindaste = st.checkbox("Uso de guindaste ou andaimes", key=f"guindaste_{i}")
    ponto_dreno = st.radio("Ponto de dreno", ["Sim", "Não"], key=f"dreno_{i}") == "Sim"
    ponto_220v = st.radio("Possui ponto 220 V?", ["Sim", "Não"], key=f"ponto220_{i}") == "Sim"
    disjuntor_sep = st.radio("Disjuntor separado?", ["Sim", "Não"], key=f"disjuntor_{i}") == "Sim"
    capacidade_disjuntor = st.text_input("Capacidade do disjuntor", key=f"capacidade_{i}")
    observacoes = st.text_area("Outras observações", key=f"obs_{i}")
    
    aparelhos.append({
        "cliente": cliente,
        "aparelho": i + 1,
        "marca_modelo": marca_modelo,
        "ambiente": ambiente,
        "dist_chao_evap": dist_chao_evap,
        "dist_teto_evap": dist_teto_evap,
        "tipo_parede_evap": tipo_parede_evap,
        "espessura_parede": espessura_parede,
        "local_condensadora": local_condensadora,
        "dist_chao_cond": dist_chao_cond,
        "tipo_telhado": tipo_telhado,
        "tipo_parede_cond": tipo_parede_cond,
        "area_tecnica": area_tecnica,
        "metros_tubulacao": metros_tubulacao,
        "uso_guindaste": uso_guindaste,
        "ponto_dreno": ponto_dreno,
        "ponto_220v": ponto_220v,
        "disjuntor_sep": disjuntor_sep,
        "capacidade_disjuntor": capacidade_disjuntor,
        "observacoes": observacoes
    })
    

# Função para gerar PDF
def gerar_pdf(cliente, aparelhos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Instalação Ar-condicionado - Cliente: {cliente}", ln=True)

    for a in aparelhos:
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, txt=f"Aparelho {a['aparelho']}: {a['marca_modelo']}", ln=True)
        pdf.multi_cell(0, 8, txt=f"""
Ambiente: {a['ambiente']} | Dist chão: {a['dist_chao_evap']}m | Teto: {a['dist_teto_evap']}m
Condensadora: {a['local_condensadora']} | Parede: {a['tipo_parede_cond']} | Área técnica: {a['area_tecnica']}m²
Tubulação: {a['metros_tubulacao']}m | Ponto 220V: {"Sim" if a['ponto_220v'] else "Não"} | Disjuntor: {a['capacidade_disjuntor']}
Obs: {a['observacoes']}
        """)
        pdf.cell(0, 10, txt="-----------------------------", ln=True)

    pdf_path = f"instalacao_{cliente.replace(' ', '_')}.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Botão de salvar dados
if st.button("Salvar e Exportar"):

    # DataFrame
    df_aparelhos = pd.DataFrame(aparelhos)


 # Salva Excel
    excel_file = f"instalacao_{cliente.replace(' ', '_')}.xlsx"
    df_aparelhos.to_excel(excel_file, index=False)

    # Salva PDF
    pdf_file = gerar_pdf(cliente, aparelhos)

    # Banco de dados
    engine = create_engine("sqlite:///instalacoes.db")
    df_aparelhos.to_sql("instalacoes", engine, if_exists="append", index=False)

    st.success("Dados salvos com sucesso!")

    # Botões para download
    st.download_button("📥 Baixar Excel", data=open(excel_file, "rb"), file_name=excel_file)
    st.download_button("📄 Baixar PDF", data=open(pdf_file, "rb"), file_name=pdf_file)