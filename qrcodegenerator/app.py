import io
import base64
import os
import qrcode
import qrcode.constants
from PIL import Image
import streamlit as st
from streamlit import components as st_components

# Carregar logo para header
_script_dir = os.path.dirname(os.path.abspath(__file__))
_logo_path = os.path.join(_script_dir, "logo.png")
_logo_img = Image.open(_logo_path).convert("RGBA")
_logo_buf = io.BytesIO()
_logo_img.save(_logo_buf, format="PNG")
_logo_b64 = base64.b64encode(_logo_buf.getvalue()).decode()
# Versão pequena para favicon
_logo_small = Image.open(_logo_path).convert("RGBA")
_logo_small.thumbnail((32, 32))
_logo_small_buf = io.BytesIO()
_logo_small.save(_logo_small_buf, format="PNG")
_logo_b64_icon = base64.b64encode(_logo_small_buf.getvalue()).decode()

st.set_page_config(
    page_title="Gerador de QR Code",
    page_icon=f"data:image/png;base64,{_logo_b64_icon}",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS para centralizar o conteúdo principal
st.markdown(
    """
    <style>
    /* Esconder header do Streamlit */
    #header, [data-testid="stHeader"] {display: none !important;}
    /* Esconder link "Back to top" e barra superior */
    .stHeader {display: none !important;}
    header.st-emotion-cache-1kyxreq {display: none !important;}
    header {display: none !important;}
    .block-container {
        max-width: 70% !important;
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header: logo + título centralizado
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
        <img src="data:image/png;base64,{_logo_b64}" style="width: 64px; margin-right: 16px;" />
        <h1 style="margin: 0;">Gerador de QR Code</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tema personalizado - CSS básico
st.markdown(
    """
    <style>
    /* Botão principal */
    .stButton>button {
        background-color: #033936;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: 600;
        min-height: 44px;
    }
    .stButton>button:hover {
        background-color: #054f4b;
    }
    .stButton>button:active {
        background-color: #033936;
    }
    /* Input de texto */
    div.stTextInput>div>div>input {
        border-color: #033936;
    }
    /* Botões de download */
    .stDownloadButton>button {
        background-color: #033936;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: 600;
        min-height: 44px;
    }
    .stDownloadButton>button:hover {
        background-color: #054f4b;
    }
    /* Upload button */
    .stFileUploader>div>div>div>button {
        background-color: #033936 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Configurações ---
with st.container():
    link = st.text_input(
        "Link",
        value="https://wa.me/551121895197?text=Olá! Como posso ajudar?",
        help="URL, texto, telefone, etc.",
    )

    col1, col2 = st.columns(2)
    with col1:
        size = st.number_input(
            "Tamanho (px)", min_value=200, max_value=10000, value=2000, step=100,
        )
    with col2:
        logo_pct = st.slider(
            "Logo (%)", min_value=10, max_value=40, value=30,
        )

    logo_file = st.file_uploader("Logo (opcional)", type=["png", "jpg", "jpeg", "gif", "webp"])

    if st.button("Gerar QR Code", type="primary", use_container_width=True, key="gen_btn"):
        if not link.strip():
            st.error("Insira um link!")
            st.stop()

        # --- Gerar QR Code ---
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        target_size = max(size, 200)
        img = img.resize((target_size, target_size), Image.LANCZOS)

        if logo_file is not None:
            logo_img = Image.open(logo_file).convert("RGBA")

            logo_size = int(target_size * logo_pct / 100)
            cx = (target_size - logo_size) // 2
            cy = (target_size - logo_size) // 2

            ratio = min(logo_size / logo_img.width, logo_size / logo_img.height)
            new_w = int(logo_img.width * ratio)
            new_h = int(logo_img.height * ratio)
            logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS)

            paste_x = cx + (logo_size - new_w) // 2
            paste_y = cy + (logo_size - new_h) // 2

            img.paste(logo_img, (paste_x, paste_y), logo_img)

        # --- Preview (versão menor para visualização) ---
        preview_img = img.resize((400, 400), Image.LANCZOS)

        col_preview = st.columns([3, 4, 3])
        with col_preview[1]:
            st.image(preview_img, caption=f"QR Code {target_size}x{target_size}px", use_container_width=False)

        # --- Download (versão original alta resolução) ---
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        st.download_button(
            label="Baixar QR Code.png",
            data=buf.getvalue(),
            file_name="qrcode.png",
            mime="image/png",
            use_container_width=True,
        )

st.markdown("")
st.caption("Feito por Michele Gomes")