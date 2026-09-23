import datetime
import streamlit as st

# Título do App
st.title("Prompt Mestre Sobrenatural")
st.markdown("Gerador de roteiros e ideias para criadores de conteúdo do nicho dark e sobrenatural.")

# Configuração das chaves bônus com padrão humanizado e ancoragem visual
if "chaves_bonus" not in st.session_state:
    st.session_state.chaves_bonus = {
        "adm_juliana_XYZ": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_camila_LKT": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_beatriz_MQP": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_fernanda_JVR": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_patricia_WSD": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_larissa_HGF": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_mariana_BVC": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_caroline_PLM": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_gabriela_ZXC": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
        "adm_renata_KJH": {"usos_hoje": 0, "data_ultimo_uso": str(datetime.date.today())},
    }

MAX_ACESSOS_DIARIOS = 25

# Campo para digitar a chave de acesso
chave_digitada = st.text_input("Digite sua Chave de Acesso (ou 'visitante_teste'):", value="visitante_teste")

# Checkbox útil para suporte / simulação de assinante pago
simular_assinante = st.checkbox("Marcar como Assinante (Simula o plano pago R$ 29,90)")

# Lógica de validação do acesso
acesso_liberado = False
mensagem_status = ""

if simular_assinante:
    acesso_liberado = True
    mensagem_status = "Acesso de assinante simulado com sucesso!"
elif chave_digitada == "visitante_teste":
    acesso_liberado = True
elif chave_digitada in st.session_state.chaves_bonus:
    hoje_str = str(datetime.date.today())
    dados_chave = st.session_state.chaves_bonus[chave_digitada]
    
    # Reseta o contador se mudou o dia
    if dados_chave["data_ultimo_uso"] != hoje_str:
        dados_chave["usos_hoje"] = 0
        dados_chave["data_ultimo_uso"] = hoje_str
        
    # Verifica o limite diário de 25 acessos para esta chave específica
    if dados_chave["usos_hoje"] < MAX_ACESSOS_DIARIOS:
        dados_chave["usos_hoje"] += 1
        acesso_liberado = True
        mensagem_status = f"Chave bônus ativa! (Uso {dados_chave['usos_hoje']}/{MAX_ACESSOS_DIARIOS} de hoje)"
    else:
        acesso_liberado = False
        mensagem_status = "Esta chave atingiu o limite de utilizações de hoje. Garanta acesso ilimitado na Hotmart!"
else:
    acesso_liberado = False
    mensagem_status = "Chave inválida."

# Exibe o status e a interface do app
if acesso_liberado:
    if chave_digitada != "visitante_teste" and not simular_assinante:
        st.success(mensagem_status)
    elif simular_assinante:
        st.info(mensagem_status)
    
    tema = st.text_input("Sobre qual lenda ou tema sobrenatural será o vídeo de hoje?")
    
    if st.button("Gerar Prompt Sobrenatural"):
        if tema:
            st.markdown(f"### Roteiro gerado para: {tema}")
            st.write("Aqui entraria o prompt estruturado de suspense gerado pela IA...")
        else:
            st.warning("Por favor, digite um tema.")
else:
    st.error(mensagem_status)
    st.markdown("---")
    st.markdown("### Quer acesso ilimitado sem se preocupar com limites?")
    st.markdown("Tenha o **Prompt Mestre Sobrenatural** liberado 24 horas por dia para escalar o seu canal dark.")
    st.markdown("[👉 Clique aqui para assinar o plano completo na Hotmart (R$ 29,90/mês)](https://pay.hotmart.com/P107727028S)")
