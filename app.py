import streamlit as st
import json
import os
import datetime
import google.generativeai as genai

# Título do App
st.title("Prompt Mestre Sobrenatural")
st.markdown("Gerador de roteiros e ideias para criadores de conteúdo do nicho dark e sobrenatural.")

# Configuração da API (Pode puxar dos Secrets do Streamlit ou inserir diretamente)
# Recomendamos configurar no st.secrets["GEMINI_API_KEY"] para segurança máxima
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GOOGLE_API_KEY = ""

ARQUIVO_CONTROLE = "controle_chaves.json"

# Função para carregar os dados persistentes
def carregar_dados():
    hoje_str = str(datetime.date.today())
    chaves_padrao = {
        "adm_juliana_XYZ": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_camila_LKT": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_beatriz_MQP": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_fernanda_JVR": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_patricia_WSD": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_larissa_HGF": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_mariana_BVC": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_caroline_PLM": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_gabriela_ZXC": {"usos_hoje": 0, "data_ultimo_uso": hoje_str},
        "adm_renata_KJH": {"usos_hoje": 0, "data_ultimo_uso": hoje_str}
    }
    
    if os.path.exists(ARQUIVO_CONTROLE):
        try:
            with open(ARQUIVO_CONTROLE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for k, v in chaves_padrao.items():
                    if k not in dados:
                        dados[k] = v
                return dados
        except Exception:
            return chaves_padrao
    return chaves_padrao

# Função para salvar os dados persistentes
def salvar_dados(dados):
    with open(ARQUIVO_CONTROLE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Inicializa os dados na sessão
if "chaves_bonus" not in st.session_state:
    st.session_state.chaves_bonus = carregar_dados()

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
    
    if dados_chave["data_ultimo_uso"] != hoje_str:
        dados_chave["usos_hoje"] = 0
        dados_chave["data_ultimo_uso"] = hoje_str
        
    if dados_chave["usos_hoje"] < MAX_ACESSOS_DIARIOS:
        dados_chave["usos_hoje"] += 1
        salvar_dados(st.session_state.chaves_bonus)
        acesso_liberado = True
        mensagem_status = f"Chave bônus ativa! (Uso {dados_chave['usos_hoje']}/{MAX_ACESSOS_DIARIOS} de hoje)"
    else:
        acesso_liberado = False
        mensagem_status = "Esta chave atingiu o limite de utilizações de hoje. Garanta acesso ilimitado na Kiwify!"
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
            if not GOOGLE_API_KEY:
                st.error("Chave da API do Google Gemini não configurada nos Segredos (Secrets) do Streamlit.")
            else:
                with st.spinner("A IA está estruturando o seu roteiro dark e os metadados..."):
                    try:
                        genai.configure(api_key=GOOGLE_API_KEY)
                        
                        # Prompt de Sistema (Prompt-Mestre v10 incorporado)
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
    model_name="gemini-1.5-flash", system_instruction=prompt_sistema
                        )
                        
                        resposta = modelo_ia.generate_content(f"Tema do vídeo: {tema}")
                        
                        st.markdown(f"### Roteiro Gerado para: {tema}")
                        st.markdown(resposta.text)
                        
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao gerar o roteiro com a IA: {e}")
        else:
            st.warning("Por favor, digite um tema.")
else:
    st.error(mensagem_status)
    st.markdown("---")
    st.markdown("### Quer acesso ilimitado sem se preocupar com limites?")
    st.markdown("Tenha o **Prompt Mestre Sobrenatural** liberado 24 horas por dia para escalar o seu canal dark.")
    st.markdown("[👉 Clique aqui para assinar o plano completo na Kiwify](https://pay.kiwify.com.br/rHfgxUR)")
