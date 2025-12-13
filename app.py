import streamlit as st
import os
from dotenv import load_dotenv
import random
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from prompts_mulher import PACKS as PACKS_MULHER

load_dotenv()

st.set_page_config(
    page_title="🎁 Presente Especial para Gabi", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado para visual premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffd700, #ff6b9d, #c44fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(255, 107, 157, 0.3);
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .message-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 107, 157, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .message-text {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        color: #ffffff;
        line-height: 1.8;
        text-align: center;
    }
    
    .heart-emoji {
        font-size: 2rem;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .stButton > button {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #ff6b9d 0%, #c44fff 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(255, 107, 157, 0.4);
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(255, 107, 157, 0.6);
    }
    
    .gift-icon {
        font-size: 4rem;
        text-align: center;
        display: block;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .image-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(255, 107, 157, 0.3);
        margin: 2rem 0;
    }
    
    .style-badge {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #ffd700 0%, #ff6b9d 100%);
        color: #1a1a2e;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        text-align: center;
        margin: 1rem auto;
        display: inline-block;
    }
    
    .footer-text {
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.5);
        text-align: center;
        margin-top: 3rem;
    }
    
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Carregar as fotos da Gabi
@st.cache_data
def carregar_fotos_gabi():
    fotos = []
    for i in range(1, 4):
        path = f"gabi{i}.jpg"
        if os.path.exists(path):
            with open(path, "rb") as f:
                fotos.append(f.read())
    return fotos

# Coletar todos os prompts de todos os packs
def obter_todos_prompts():
    todos_prompts = []
    for pack_id, pack_info in PACKS_MULHER.items():
        for nome_estilo, dados in pack_info["prompts"].items():
            todos_prompts.append({
                "nome": nome_estilo,
                "descricao": dados["descricao"],
                "pack": pack_info["nome"]
            })
    return todos_prompts

# PROMPT GERAL
prompt_geral = """
Sua missão é transformar uma selfie em uma obra de arte fotorrealista, seguindo rigorosamente as seções abaixo. A fidelidade facial da pessoa na imagem de entrada é a prioridade número um.

== SESSÃO 1: FIDELIDADE FACIAL (PRIORIDADE MÁXIMA) ==
Esta é a regra mais importante e não-negociável.
1.  **Preservação Exata:** Transfira com 100% de exatidão todas as características faciais da pessoa na foto original para a imagem gerada. Isso inclui o formato exato dos olhos, nariz, boca, queixo e sobrancelhas.
2.  **Estrutura e Proporções:** Mantenha a estrutura óssea facial, as dimensões e as proporções idênticas. A distância entre os olhos, o comprimento do nariz e a posição da boca não devem ser alterados.
3.  **Etnia e Traços Únicos:** Preserve completamente a etnia e quaisquer traços únicos, como pintas, cicatrizes sutis ou assimetrias leves, para garantir a autenticidade.

== SESSÃO 2: QUALIDADE FOTOGRÁFICA E ESTILO ==
A imagem final deve ter a qualidade de uma fotografia profissional de alta resolução.
1.  **Realismo Absoluto:** O resultado deve ser indistinguível de uma foto real tirada com equipamento de ponta. Evite qualquer aspecto de 'arte digital', 'desenho' ou 'renderização 3D'.
2.  **Equipamento Simulado:** Emule o resultado de uma câmera DSLR ou Mirrorless full-frame, preferencialmente com uma lente prime (ex: 85mm f/1.4) para criar uma profundidade de campo natural e um desfoque de fundo suave (bokeh), quando aplicável ao cenário.
3.  **Textura e Detalhes:** Renderize detalhes finos, como a textura real da pele (incluindo poros), o brilho nos olhos e os fios de cabelo individuais. A imagem deve ser nítida e rica em detalhes.

== SESSÃO 3: APLICAÇÃO DO TEMA ESPECÍFICO ==
As regras das Seções 1 e 2 são a base sobre a qual o seguinte tema criativo deve ser aplicado. A pessoa da foto é a 'atriz', e o tema abaixo é o seu 'papel e cenário'.
- **Execute o seguinte tema:** "{prompt_especifico}"

== SESSÃO 4: INSTRUÇÃO DE SAÍDA ==
1.  **Formato Final:** A saída deve ser exclusivamente a imagem gerada.
2.  **Restrição Absoluta:** NÃO inclua texto, descrições, explicações ou qualquer caractere antes ou depois da imagem.

IMAGE OUTPUT ONLY.
"""

def gerar_imagem(prompt, fotos_bytes_lista, nome_estilo):
    """Gera imagem usando as fotos de referência."""
    try:
        # Converter todas as fotos para objetos PIL Image
        fotos_originais = [Image.open(BytesIO(fb)) for fb in fotos_bytes_lista]
        prompt_completo = prompt_geral.format(prompt_especifico=prompt)
        
        # Montar conteúdo: todas as fotos + prompt
        contents = fotos_originais + [prompt_completo]
        
        client = genai.Client(api_key=st.secrets["gemini_api_key"])
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="4:5",
                    image_size="2K"
                ),
            )
        )
        
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                imagem_resultado = Image.open(BytesIO(part.inline_data.data))
                return imagem_resultado
        
        return None
        
    except Exception as e:
        st.error(f"Erro ao gerar imagem: {e}")
        return None

# Carregar fotos
fotos_gabi = carregar_fotos_gabi()
todos_prompts = obter_todos_prompts()

# Interface
st.markdown('<span class="gift-icon">🎁</span>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Presente Especial</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Um programa especial para você!</p>', unsafe_allow_html=True)

# Recado
st.markdown("""
<div class="message-card">
    <p class="message-text">
        <span class="heart-emoji">✨</span><br><br>
        Gabi!<br><br>
        Preparei essa surpresa especial pra você! 🎁<br>
        Cada vez que você clicar no botão, uma versão única sua 
        vai aparecer em um cenário mágico e diferente! 🌟<br><br>
        É uma forma divertida de te ver em 
        diferentes situações, lugares e estilos.<br><br>
        Aproveita! 😄
    </p>
</div>
""", unsafe_allow_html=True)

# Inicializar estado
if "imagem_gerada" not in st.session_state:
    st.session_state.imagem_gerada = None
if "estilo_atual" not in st.session_state:
    st.session_state.estilo_atual = None
if "pack_atual" not in st.session_state:
    st.session_state.pack_atual = None

# Centralizar botão - 3 colunas iguais com botão no meio
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    # Verificar se há fotos carregadas
    if len(fotos_gabi) == 0:
        st.error("⚠️ Fotos não encontradas! Certifique-se de que gabi1.jpg, gabi2.jpg e gabi3.jpg estão na pasta.")
    else:
        # Botão principal ou de gerar outro
        botao_texto = "🎁 Gerar Presente" if st.session_state.imagem_gerada is None else "🎁 Gerar Outro Presente"
        
        if st.button(botao_texto, type="primary", width='stretch'):
            with st.spinner("✨ Criando sua surpresa mágica...", show_time=True):
                # Escolher prompt aleatório
                prompt_escolhido = random.choice(todos_prompts)
                
                # Gerar imagem
                imagem = gerar_imagem(
                    prompt_escolhido["descricao"],
                    fotos_gabi,
                    prompt_escolhido["nome"]
                )
                
                if imagem:
                    st.session_state.imagem_gerada = imagem
                    st.session_state.estilo_atual = prompt_escolhido["nome"]
                    st.session_state.pack_atual = prompt_escolhido["pack"]
                    st.rerun()

# Mostrar imagem gerada
if st.session_state.imagem_gerada is not None:
    st.markdown("---")
    
    # Badge do estilo
    st.markdown(f"""
    <div style="text-align: center;">
        <span class="style-badge">{st.session_state.pack_atual} • {st.session_state.estilo_atual}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Imagem
    st.image(st.session_state.imagem_gerada, use_container_width=True)
    
    # Botão de download
    img_buffer = BytesIO()
    st.session_state.imagem_gerada.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="💾 Salvar Presente",
            data=img_buffer.getvalue(),
            file_name=f"presente_gabi_{st.session_state.estilo_atual.replace(' ', '_').lower()}.png",
            mime="image/png"
        )
