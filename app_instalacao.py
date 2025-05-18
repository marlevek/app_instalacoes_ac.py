import streamlit as st
import pandas as pd
from fpdf import FPDF
from sqlalchemy import create_engine

st.set_page_config('Instalação Ar-condicionado', page_icon=':male-mechanic:')
st.title('Dados Instalação AC :male-mechanic:')

# Nome do cliente
cliente = st.text_input('Cliente')
endereco = st.text_input('Endereço')

# Quantidade de aparelhos
qtd_aparelhos = st.selectbox('Quantidade de aparelhos', list(range(1, 11)))

aparelhos = []

for i in range(qtd_aparelhos):
    st.markdown(f'### Aparelho {i + 1}')
    marca_modelo = st.text_input(f'Marca e Modelo AC', key=f'marca_modelo_{i}')
    capacidade_aparelho = st.text_input(f'Capacidade do aparelho (BTU/h)', key=f'capacidade_aparelho_{i}')

    st.subheader('EVAPORADORA')
    ambiente = st.text_input("Ambiente de instalação", key=f"ambiente_{i}")
    dist_chao_evap = st.number_input("Distância do chão (m)", key=f"dist_chao_evap_{i}", min_value=0.0, step=0.01)
    dist_teto_evap = st.number_input("Distância do teto (m)", key=f"dist_teto_evap_{i}", min_value=0.0, step=0.01)
    dist_paredes_lateral_direita = st.number_input('Distância paredes lateral direita (cm)', key=f'dist_paredes_lateral_direita_{i}', min_value=0.0, step=0.01)
    dist_paredes_lateral_esquerda = st.number_input('Distância paredes lateral esquerda (cm)', key=f'dist_paredes_lateral_esquerda_{i}', min_value=0.0, step=0.01)
    tipo_parede_evap = st.selectbox("Tipo de parede (Evaporadora)", ["Concreto", "Alvenaria", "Drywall", "Madeira"], key=f"tipo_parede_evap_{i}")

    st.subheader("CONDENSADORA")
    local_condensadora = st.selectbox("Local da instalação", ["Parede", "Área Técnica", "Chão", "Telhado"], key=f"local_condensadora_{i}")
    tipo_telhado = ''
    tipo_parede_cond = ''
    area_tecnica = 0
    dist_chao_cond = 0.0

    if local_condensadora == 'Telhado':
        tipo_telhado = st.text_input("Tipo de telhado", key=f"tipo_telhado_{i}")
        dist_chao_cond = st.number_input("Distância do chão (m)", key=f"dist_chao_cond_{i}", min_value=0.0, step=0.01)
    elif local_condensadora == 'Parede':
        tipo_parede_cond = st.text_input("Tipo de parede (Condensadora)", key=f"tipo_parede_cond_{i}")
        dist_chao_cond = st.number_input("Distância do chão (m)",  key=f"dist_chao_cond_{i}", min_value=0.0, step=0.01)
    elif local_condensadora == 'Área Técnica':
        area_tecnica = st.number_input("Área Técnica (m²)", key=f"area_tecnica_{i}", min_value=0.0, step=0.01)

    st.subheader("DIVERSOS")
    metros_tubulacao = st.number_input("Metros de tubulação", key=f"metros_tubulacao_{i}", min_value=0.0, step=0.01)

    uso_guindaste = st.selectbox(f"Usou guindaste no Aparelho {i+1}?", options=["Não", "Sim"], key=f"uso_guindaste_{i}")
    ponto_dreno = st.selectbox(f"Ponto de dreno disponível no Aparelho {i+1}?", options=["Não", "Sim"], key=f"ponto_dreno_{i}")
    ponto_220v = st.selectbox(f"Ponto 220v disponível no Aparelho {i+1}?", options=["Não", "Sim"], key=f"ponto_220v_{i}")
    disjuntor_sep = st.selectbox(f"Disjuntor separado no Aparelho {i+1}?", options=["Não", "Sim"], key=f"disjuntor_sep_{i}")
    capacidade_disjuntor = st.text_input(f"Capacidade do disjuntor do Aparelho {i+1}", key=f"capacidade_disjuntor_{i}") if disjuntor_sep == "Sim" else ""

    observacoes = st.text_area(f"Observações do Aparelho {i+1}", key=f"observacoes_{i}")

    aparelhos.append({
        "cliente": cliente,
        "endereço": endereco,
        "aparelho": i + 1,
        "marca_modelo": marca_modelo,
        "capacidade_aparelho": capacidade_aparelho,
        "ambiente": ambiente,
        "dist_chao_evap": dist_chao_evap,
        "dist_teto_evap": dist_teto_evap,
        "dist_paredes_lateral_direita": dist_paredes_lateral_direita,
        "dist_paredes_lateral_esquerda": dist_paredes_lateral_esquerda,
        "tipo_parede_evap": tipo_parede_evap,
        "local_condensadora": local_condensadora,
        "dist_chao_cond": dist_chao_cond,
        "tipo_telhado": tipo_telhado,
        "tipo_parede_cond": tipo_parede_cond,
        "area_tecnica": area_tecnica,
        "metros_tubulacao": metros_tubulacao,
        "uso_guindaste": 1 if uso_guindaste == "Sim" else 0,
        "ponto_dreno": 1 if ponto_dreno == "Sim" else 0,
        "ponto_220v": 1 if ponto_220v == "Sim" else 0,
        "disjuntor_sep": 1 if disjuntor_sep == "Sim" else 0,
        "capacidade_disjuntor": capacidade_disjuntor,
        "observacoes": observacoes
    })

def gerar_pdf(cliente, endereco, aparelhos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Instalação de Ar-condicionado", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Cliente: {cliente}", ln=True)
    pdf.cell(0, 10, f"Endereço: {endereco}", ln=True)
    pdf.ln(5)

    for a in aparelhos:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"Aparelho {a['aparelho']}: {a['marca_modelo']} ({a['capacidade_aparelho']} BTU/h)", ln=True)
        pdf.set_font("Arial", "", 11)

        info_text = [
            f"Ambiente: {a['ambiente']}",
            f"Evaporadora: Chão: {a['dist_chao_evap']} m | Teto: {a['dist_teto_evap']} m | Lateral Dir: {a['dist_paredes_lateral_direita']} cm | Lateral Esq: {a['dist_paredes_lateral_esquerda']} cm",
            f"Tipo de parede (Evaporadora): {a['tipo_parede_evap']}",
        ]

        if a['local_condensadora'] == 'Parede':
            info_text.append(f"Condensadora: Local: {a['local_condensadora']} | Tipo parede: {a['tipo_parede_cond']} | Dist chão: {a['dist_chao_cond']} m")
        elif a['local_condensadora'] == 'Telhado':
            info_text.append(f"Condensadora: Local: {a['local_condensadora']} | Tipo telhado: {a['tipo_telhado']} | Dist chão: {a['dist_chao_cond']} m")
        elif a['local_condensadora'] == 'Área Técnica':
            info_text.append(f"Condensadora: Local: {a['local_condensadora']} | Área técnica: {a['area_tecnica']} m²")
        else:
            info_text.append(f"Condensadora: Local: {a['local_condensadora']}")

        info_text.extend([
            f"Tubulação: {a['metros_tubulacao']} m",
            f"Guindaste: {'Sim' if a['uso_guindaste'] else 'Não'} | Dreno: {'Sim' if a['ponto_dreno'] else 'Não'} | 220v: {'Sim' if a['ponto_220v'] else 'Não'} | Disjuntor: {'Sim' if a['disjuntor_sep'] else 'Não'}",
            f"Capacidade Disjuntor: {a['capacidade_disjuntor']}",
            f"Observações: {a['observacoes']}"
        ])

        pdf.multi_cell(0, 7, "\n".join(info_text))
        pdf.ln(2)
        pdf.cell(0, 5, "-"*100, ln=True)
        pdf.ln(2)

    pdf_path = f"instalacao_{cliente.replace(' ', '_').lower()}.pdf"
    pdf.output(pdf_path)
    return pdf_path

if st.button("Salvar e Exportar"):

    if not cliente.strip():
        st.error("Por favor, preencha o nome do cliente.")
    else:
        df_aparelhos = pd.DataFrame(aparelhos)

        # Salvar Excel
        excel_file = f"instalacao_{cliente.replace(' ', '_').lower()}.xlsx"
        df_aparelhos.to_excel(excel_file, index=False)

        # Salvar PDF
        pdf_file = gerar_pdf(cliente, endereco, aparelhos)

        # Salvar no banco SQLite
        engine = create_engine("sqlite:///instalacoes.db")
        df_aparelhos.to_sql("instalacoes", engine, if_exists="append", index=False)

        st.success("Dados salvos com sucesso!")

        # Botões para download
        with open(excel_file, "rb") as f:
            st.download_button("📥 Baixar Excel", data=f, file_name=excel_file)

        with open(pdf_file, "rb") as f:
            st.download_button("📥 Baixar PDF", data=f, file_name=pdf_file)