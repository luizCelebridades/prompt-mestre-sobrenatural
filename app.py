from datetime import datetime
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Prompt Mestre Sobrenatural", page_icon="👻", layout="centered"
)

st.title("👻 Prompt Mestre Sobrenatural")
st.write(
    "Gerador de roteiros e ideias para criadores de conteúdo do nicho dark e"
    " sobrenatural."
)

# Inicializa o controle de uso na sessão
if "uso_diario" not in st.session_state:
  st.session_state["uso_diario"] = {}

data_hoje = datetime.now().strftime("%Y-%m-%d")


def verificar_e_atualizar_limite_hibrido(usuario_chave: str, eh_assinante: bool):
  """Controla o limite diário:

  - 25 gerações para assinantes.
  - 5 gerações para testes gratuitos.
  """
  limite_diario = 25 if eh_assinante else 5
  controle_id = f"{usuario_chave}_{data_hoje}"

  if controle_id not in st.session_state["uso_diario"]:
    st.session_state["uso_diario"][controle_id] = 0

  if st.session_state["uso_diario"][controle_id] >= limite_diario:
    return False, limite_diario

  return True, limite_diario


def registrar_uso(usuario_chave: str):
  """Incrementa mais 1 uso no contador do dia."""
  controle_id = f"{usuario_chave}_{data_hoje}"
  if controle_id in st.session_state["uso_diario"]:
    st.session_state["uso_diario"][controle_id] += 1
  else:
    st.session_state["uso_diario"][controle_id] = 1


# --- SIMULAÇÃO DE LOGIN / STATUS (Pode adaptar com a sua autenticação atual) ---
# Na sua versão final, 'usuario_atual' e 'eh_assinante' virão da validação da chave do usuário.
usuario_atual = st.text_input(
    "Digite sua Chave de Acesso (ou deixe 'visitante' para testar):",
    "visitante_teste",
)
eh_assinante = st.toggle(
    "Marcar como Assinante (Simula o plano pago R$ 29,90)", value=False
)

st.divider()

# Campo onde o usuário escreve o tema do vídeo
tema_video = st.text_input(
    "Sobre qual lenda ou tema sobrenatural será o vídeo de hoje?"
)

if st.button("Gerar Prompt Sobrenatural"):
  if not tema_video.strip():
    st.warning("Por favor, digite um tema antes de gerar.")
  else:
    # Verifica o limite de acordo com o status (Assinante=25 | Visitante=5)
    pode_usar, limite_maximo = verificar_e_atualizar_limite_hibrido(
        usuario_atual, eh_assinante
    )

    if pode_usar:
      # --- AQUI ENTRA A SUA CHAMADA REAL PARA A API DO GEMINI ---
      # Exemplo simulado de resposta:
      resposta_gerada = f"""[ROTEIRO DARK / SOBRENATURAL]
      Tema: {tema_video}
      - Introdução impactante sobre o mistério...
      - Desenvolvimento com relatos e atmosfera sombria...
      - Chamada para ação (CTA) para o canal.
      """

      # Registra o uso bem-sucedido
      registrar_uso(usuario_atual)

      # Consulta quantos usos já foram feitos hoje
      controle_id = f"{usuario_atual}_{data_hoje}"
      usos_atuais = st.session_state["uso_diario"][controle_id]

      st.success("Prompt gerado com sucesso!")
      st.write(resposta_gerada)
      st.info(f"📊 Uso diário: {usos_atuais} de {limite_maximo} permitidos.")

    else:
      # Mensagens transparentes e focadas na produtividade
      if eh_assinante:
        st.error(
            "⚠️ Você atingiu o seu limite diário de 25 gerações. O seu acesso"
            " será renovado amanhã para você continuar a sua produção!"
        )
      else:
        st.warning(
            "⚠️ Você utilizou as suas 5 gerações de teste gratuito de hoje. O"
            " motor de inteligência artificial é o mesmo, mas para ter o"
            " volume de 25 gerações diárias e acompanhar o ritmo do seu canal,"
            " assine o plano completo por R$ 29,90/mês."
        )
        st.link_button(
            "Quero assinar o plano para criadores (R$ 29,90/mês)",
            "https://pay.hotmart.com/P107727028S",
        )
