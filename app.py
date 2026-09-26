import datetime
import json
import google.generativeai as genai
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(
    page_title="Prompt Mestre Sobrenatural", page_icon="🔮", layout="centered"
)
st.title("Prompt Mestre Sobrenatural")
st.markdown(
    "Gerador profissional de roteiros e ideias para criadores de conteúdo do"
    " nicho dark e sobrenatural."
)

try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GOOGLE_API_KEY = ""

# --- Inicialização do Firebase (uma única vez, compartilhado com o webhook) ---
if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["FIREBASE_CREDENTIALS_JSON"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Limites diários por tipo de chave
LIMITES = {"bonus": 25, "assinante": 30}

# --- BARRA LATERAL ---
st.sidebar.header("Painel de Acesso")
chave_digitada = (
    st.sidebar.text_input(
        "Digite sua Chave de Acesso (e-mail usado na compra ou chave bônus):"
    )
    .strip()
    .lower()
)

# --- VALIDAÇÃO (única porta de entrada, sem atalhos) ---
acesso_liberado = False
mensagem_status = ""

if chave_digitada:
    doc_ref = db.collection("chaves").document(chave_digitada)
    doc = doc_ref.get()

    if doc.exists:
        dados_chave = doc.to_dict()
        tipo = dados_chave.get("tipo", "bonus")
        status = dados_chave.get("status", "ativa")
        limite = LIMITES.get(tipo, 25)
        hoje_str = str(datetime.date.today())

        if status != "ativa":
            mensagem_status = (
                "Sua assinatura não está ativa no momento. Verifique seu"
                " pagamento na Kiwify."
            )
        else:
            if dados_chave.get("data_ultimo_uso") != hoje_str:
                dados_chave["usos_hoje"] = 0
                dados_chave["data_ultimo_uso"] = hoje_str

            if dados_chave["usos_hoje"] < limite:
                dados_chave["usos_hoje"] += 1
                doc_ref.set(dados_chave, merge=True)
                acesso_liberado = True
                mensagem_status = (
                    f"Chave {tipo} ativa! (Uso {dados_chave['usos_hoje']}/"
                    f"{limite} hoje)"
                )
            else:
                if tipo == "bonus":
                    mensagem_status = (
                        "Esta chave bônus atingiu o limite de hoje. Garanta"
                        " acesso ilimitado assinando na Kiwify!"
                    )
                else:
                    mensagem_status = (
                        f"Você atingiu seu limite diário de {limite}"
                        " gerações. Volta amanhã!"
                    )
    else:
        mensagem_status = (
            "Chave inválida ou não encontrada. Assine na Kiwify para receber"
            " acesso."
        )
else:
    mensagem_status = "Digite sua chave de acesso ao lado para começar."

# --- INTERFACE PRINCIPAL ---
if acesso_liberado:
    st.success(mensagem_status)
    st.markdown("---")
    tema = st.text_input(
        "Sobre qual lenda ou tema sobrenatural será o vídeo de hoje?"
    )

    if st.button("Gerar Roteiro Mestre Sobrenatural", type="primary"):
        if tema:
            if not GOOGLE_API_KEY:
                st.error(
                    "A chave da API do Gemini (GEMINI_API_KEY) não foi"
                    " configurada nos Secrets do Streamlit Cloud."
                )
            else:
                with st.spinner(
                    "A Inteligência Artificial está estruturando o seu"
                    " roteiro dark, gatilhos mentais e metadados..."
                ):
                    try:
                        genai.configure(api_key=GOOGLE_API_KEY)
                        prompt_sistema = """
                        Você é um roteirista especialista em histórias reais de terror e sobrenatural para YouTube, com domínio de storytelling e gatilhos mentais de persuasão aplicados à retenção de audiência. Ao receber um tema, siga rigorosamente esta ordem de entrega dividida em fases:
                        1. Análise de potencial e duração (Curta, Média ou Longa).
                        2. Construção do roteiro completo com os 7 gatilhos mentais (Afeição, Autoridade, Prova social, Escassez/urgência, História, Novidade, Reciprocidade).
                        3. Capítulo 0 — Gancho [00:00:00] obrigatório e independente, seguido de blocos com timestamps (XX:XX:XX).
                        4. Prompt de imagem de choque ambíguo (frame 1) com estilo fotorrealista assustador (hyperrealistic skin texture, analog horror aesthetic, gritty, sinister, shot on 35mm film, cinematic lighting, 8k).
                        5. Metadados (5 opções de título com o recomendado em maiúsculas, descrição curta com hashtags otimizadas para engajamento e tags).
                        6. Versão de narração (ElevenLabs) em texto corrido com pontuação de ritmo (reticências, frases curtas, aspas).
                        7. Ficha de personagens/cenário e Briefing de thumbnail (Flow + Canva).
                        8. Spin-off de Short (30-45s).
                        """

                        modelo_ia = genai.GenerativeModel(
                            model_name="gemini-3.8-flash",
                            system_instruction=prompt_sistema,
                        )
                        resposta = modelo_ia.generate_content(
                            f"Tema do vídeo: {tema}"
                        )

                        st.markdown(
                            f"### Roteiro Gerado com Sucesso para: {tema}"
                        )
                        st.markdown(resposta.text)

                    except Exception as e:
                        st.error(
                            f"Ocorreu um erro ao comunicar com a API da IA: {e}"
                        )
        else:
            st.warning("Por favor, digite um tema válido.")
else:
    st.error(mensagem_status)
    st.markdown("---")
    st.markdown("### Quer acesso ilimitado sem se preocupar com limites?")
    st.markdown(
        "[👉 Clique aqui para assinar o plano completo na"
        " Kiwify](https://pay.kiwify.com.br/rHfgxUR)"
    )