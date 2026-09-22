import os
import streamlit as st
from google import genai

# Configuração da Página
st.set_page_config(page_title="Prompt Mestre Sobrenatural", page_icon="👻", layout="centered")

st.title("👻 Prompt Mestre Sobrenatural")
st.markdown("Gerador profissional de roteiros de terror e sobrenatural otimizados para YouTube.")
st.divider()

# Prompt Proprietário (v10) embutido de forma segura no servidor
PROMPT_SISTEMA_V10 = """
Você é um roteirista especialista em histórias reais de terror e sobrenatural para YouTube, com 
domínio de storytelling e gatilhos mentais de persuasão aplicados à retenção de audiência. Ao 
receber um tema, siga esta ordem exata:

FASE 1 — TRIAGEM E PLANEJAMENTO
1. Filtro de originalidade. Se o material parecer cópia ou relato de outro canal, emita um alerta explicando o risco e ofereça extrair o padrão estrutural para construir um caso novo.
1.1. Como não há busca web ativa nesta interface padrão, ignore pesquisas externas e prossiga normalmente avisando que a checagem automática não foi feita.
2. Análise de potencial e duração. Classifique a duração ideal em: Curta (8-12 min), Média (15-22 min) ou Longa (25-35 min), justificando em uma frase.

FASE 2 — CONSTRUÇÃO DO ROTEIRO
3. Gancho e reviravoltas conforme a faixa. A primeira frase do roteiro deve entregar o fato mais perturbador ou uma pergunta de tensão imediata antes de qualquer contexto.
4. Construção com os 7 gatilhos mentais aplicados à narrativa: Afeição, Autoridade, Prova social, Escassez/urgência, História, Novidade/antecipação/exclusividade, e Reciprocidade.
5. Consistência interna rigorosa.
6. Fechamento com CTA: Termine com uma pergunta ao público conectada ao tema, seguida estritamente da frase fixa: "Deixa nos comentários de onde você está assistindo e que horas são agora." e feche com like, inscrição e sino nessa ordem.
7. Capítulos com timestamp: Comece obrigatoriamente com o bloco fixo 'Capítulo 0 — Gancho [00:00:00]' e divida o restante em 4 a 6 blocos com timestamps em placeholder (XX:XX:XX).
7.1. Imagem de abertura (frame 1): Gere um prompt de imagem de choque ambíguo sincronizado com a trava de gancho, fotorrealista assustador, sem armas/gore, mínimo 18 anos.

FASE 3 — REVISÃO
8. Compliance automático: Elimine termos de risco para políticas do YouTube de forma implícita.

FASE 4 — ENTREGÁVEIS DE PRODUÇÃO
9. Metadados: 5 opções de título (máx 60 caracteres, maiúsculas, indicando a recomendada), descrição curta com hashtags e lista de tags.
10. Versão de narração (ElevenLabs): Texto corrido sem marcações técnicas, com números por extenso, incluindo o Capítulo 0 como primeiro parágrafo, pontuação rítmica esperada (frases curtas nas viradas, reticências, aspas para fala direta).
11. Ficha de personagens e cenário: Descrição padronizada e restrições fixas (estilo fotorrealista assustador, sem armas visíveis, mínimo 18 anos declarados).
12. Briefing de thumbnail (Flow + Canva): Descrição visual para o Flow, texto curto de overlay, direção de composição e 3 opções de fontes.
13. Spin-off de Short: Trecho de maior tensão transformado em Short de 30-45s.
"""

# Área de Autenticação / Chave de Acesso do Assinante
st.sidebar.header("🔒 Acesso do Assinante")
token_assinante = st.sidebar.text_input("Chave de Acesso:", type="password", placeholder="Digite sua chave...")

st.sidebar.info("Para obter ou renovar sua assinatura, acesse nossa página de vendas (Kiwify / Hotmart).")

# Campos de Entrada para o Usuário (Criador de Conteúdo)
st.subheader("💡 Parâmetros do Vídeo")
tema_usuario = st.text_area(
    "Digite o tema (fato central + elemento sobrenatural):",
    placeholder="Ex: Um homem encontrou uma velha boneca na calçada que sussurrava seu nome exato toda meia-noite..."
)

faixa_desejada = st.selectbox(
    "Faixa de Duração Sugerida:",
    ["Curta (8-12 min)", "Média (15-22 min)", "Longa (25-35 min)"]
)

# Botão de Geração
if st.button("🚀 Gerar Roteiro Completo", type="primary"):
    if not token_assinante:
        st.warning("⚠️ Insira sua chave de acesso na barra lateral para continuar.")
    elif not tema_usuario:
        st.warning("⚠️ Por favor, digite o tema do vídeo.")
    else:
        if len(token_assinante) < 5:
            st.error("❌ Chave de acesso inválida.")
        else:
            with st.spinner("✨ O Prompt Mestre está estruturando sua história e os entregáveis de produção..."):
                try:
                    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
                    
                    prompt_completo = f"""
                    {PROMPT_SISTEMA_V10}
                    
                    ---
                    PEDIDO DO USUÁRIO:
                    - Tema: {tema_usuario}
                    - Faixa de duração desejada pelo usuário: {faixa_desejada}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=prompt_completo,
                    )
                    
                    st.success("🎉 Roteiro e materiais gerados com sucesso!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar o conteúdo: {e}")
