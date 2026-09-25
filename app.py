import datetime
import json
import os
import streamlit as st

# Título do App
st.title("Prompt Mestre Sobrenatural")
st.markdown(
    "Gerador de roteiros e ideias para criadores de conteúdo do nicho dark e"
    " sobrenatural."
)

ARQUIVO_CONTROLE = "controle_chaves.json"


# Função para carregar os dados persistentes
def carregar_dados():
  hoje_str = str(datetime.date.today())
  chaves_padrao = {
      "adm_juliana_XYZ": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_camila_LKT": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_beatriz_MQP": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_fernanda_JVR": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_patricia_WSD": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_larissa_HGF": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_mariana_BVC": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_caroline_PLM": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_gabriela_ZXC": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
      "adm_renata_KJH": {
          "usos_hoje": 0,
          "data_ultimo_uso": hoje_str,
      },
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
chave_digitada = st.text_input(
    "Digite sua Chave de Acesso (ou 'visitante_teste'):", value="visitante_teste"
)

# Checkbox útil para suporte / simulação de assinante pago
simular_assinante = st.checkbox(
    "Marcar como Assinante (Simula o plano pago R$ 29,90)"
)

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
    salvar_dados(st.session_state.chaves_bonus)
    acesso_liberado = True
    mensagem_status = (
        f"Chave bônus ativa! (Uso {dados_chave['usos_hoje']}/"
        f"{MAX_ACESSOS_DIARIOS} de hoje)"
    )
  else:
    acesso_liberado = False
    mensagem_status = (
        "Esta chave atingiu o limite de utilizações de hoje. Garanta acesso"
        " ilimitado na Kiwify!"
    )
else:
  acesso_liberado = False
  mensagem_status = "Chave inválida."

# Exibe o status e a interface do aprofundada do gerador
if acesso_liberado:
  if chave_digitada != "visitante_teste" and not simular_assinante:
    st.success(mensagem_status)
  elif simular_assinante:
    st.info(mensagem_status)

 tema = st.text_input("Sobre qual lenda ou tema sobrenatural será o vídeo de hoje?")

  if st.button("Gerar Prompt Sobrenatural"):
    if tema:
      st.markdown(f"### Roteiro e Estrutura Dark para: {tema}")
      
      st.markdown("#### 1. Gancho (Hook - Primeiros 5 segundos)")
      st.markdown(f"> *E se eu te dissesse que o que contam sobre **{tema}** esconde um segredo que as autoridades tentam apagar? Ouça até o final se tiver coragem...*")
      
      st.markdown("#### 2. Atmosfera e Ambientação")
      st.markdown("Trilha sonora de fundo: Baixa frequência (drone sombrio) com ruídos estáticos de rádio antigo. Efeitos visuais em tons dessaturados (preto, branco e vermelho escuro).")
      
      st.markdown("#### 3. Desenvolvimento da Narrativa")
      st.markdown(f"Exploração profunda dos mitos, relatos de testemunhas oculares e os recantos mais escuros associados a **{tema}**. Construção gradual de tensão psicológica e mistério.")
      
      st.markdown("#### 4. Chamada para Ação (CTA)")
      st.markdown(f"*Você teria coragem de investigar **{tema}** sozinho? Deixe nos comentários e compartilhe este vídeo com alguém que ama um bom mistério.*")
      
    else:
      st.warning("Por favor, digite um tema.")
else:
  st.error(mensagem_status)
  st.markdown("---")
  st.markdown("### Quer acesso ilimitado sem se preocupar com limites?")
  st.markdown(
      "Tenha o **Prompt Mestre Sobrenatural** liberado 24 horas por dia para"
      " escalar o seu canal dark."
  )
  st.markdown(
      "[👉 Clique aqui para assinar o plano completo na"
      " Kiwify](https://pay.kiwify.com.br/rHfgxUR)"
  )
