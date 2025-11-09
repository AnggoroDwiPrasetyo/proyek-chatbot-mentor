import streamlit as st
import google.generativeai as genai
import json 

# --- FUNGSI CSS KUSTOM (DIPERBAIKI) ---
def load_custom_css():
    """Menyuntikkan CSS kustom untuk chat bubble yang lebih menarik."""
    st.markdown("""
        <style>
        /* Style untuk bubble chat bot */
        div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
            background-color: #F0F4F8; /* Abu-abu muda */
            color: #111; /* <-- BARU: Memaksa teks jadi hitam */
            border-radius: 12px;
            padding: 14px;
            border: 1px solid #D1D9E1;
            line-height: 1.6;
        }
        
        /* Style untuk bubble chat user. */
        div[data-testid="stChatMessage"]:has(div[style*="direction: rtl"]) div[data-testid="stMarkdownContainer"] {
            background-color: #E0F7FA; /* Biru muda */
            color: #111; /* <-- BARU: Memaksa teks jadi hitam */
            border-radius: 12px;
            padding: 14px;
            border: 1px solid #B2EBF2;
        }

        /* Perbesar avatar emoji */
        span[data-testid="stChatAvatarIcon"] {
            font-size: 1.8rem; /* Perbesar emoji */
        }
        
        /* Merapikan sidebar */
        [data-testid="stSidebarUserContent"] {
            padding-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --- FUNGSI TOOL 1: PENDAFTARAN (Tetap sama) ---
def enroll_in_course(course_name: str, user_name: str) -> str:
    """Mendaftarkan pengguna ke kursus."""
    print(f"[Memanggil Fungsi: enroll_in_course({course_name}, {user_name})]")
    response = {
        "status": "sukses",
        "user": user_name,
        "course": course_name,
        "confirmation_code": f"MENTOR-DS-{hash(user_name + course_name) % 10000}"
    }
    return json.dumps(response)

# --- DEFINISI TOOL (Tetap sama) ---
enrollment_tool = {
    "function_declarations": [
        {
            "name": "enroll_in_course",
            "description": "Mendaftarkan pengguna untuk kursus Data Science.", 
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "course_name": {"type_": "STRING", "description": "Nama kursus Data Science, misal 'Analisis Data dengan Pandas'"},
                    "user_name": {"type_": "STRING", "description": "Nama pengguna yang mendaftar"}
                },
                "required": ["course_name", "user_name"]
            }
        }
    ]
}

# --- Persona/Instruksi Sistem (Tetap sama) ---
SYSTEM_INSTRUCTION = """
Kamu adalah "Koding Mentor", seorang asisten AI yang berperan sebagai senior developer 
dan ahli Data Science yang ramah, santai, dan suportif.
Tugasmu adalah membantu pengguna yang sedang belajar coding dan data science, dari dasar hingga advance.

Aturanmu:
1.  Gaya Bahasamu: Santai, ramah, dan jangan kaku. Gunakan sapaan seperti "Bro", "Sip", 
    atau "Gini ceritanya...".
2.  Domain Pengetahuan: Fokus utamamu adalah:
    -   Dasar Python & SQL
    -   Data Science (Pandas, NumPy, Scikit-learn)
    -   Visualisasi Data (Matplotlib, Seaborn)
    -   Machine Learning & Deep Learning (TensorFlow, Keras)
    -   Deployment & Tools (Streamlit, Docker)
3.  Menolak dengan Sopan: Jika pengguna bertanya sesuatu yang JAUH di luar domain 
    pengetahuanmu (misalnya resep masakan, politik, dll.), tolak dengan sopan. 
4.  Selalu gunakan Bahasa Indonesia.
5.  TOOL (PENDAFTARAN): Jika pengguna meminta untuk mendaftar kursus, GUNAKAN tool `enroll_in_course`. Selalu minta nama pengguna jika belum diberikan.
"""

# --- Konfigurasi Halaman (Tetap sama) ---
st.set_page_config(
    page_title="Mentor Data Science", 
    page_icon="🧑‍🔬",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Panggil fungsi CSS kustom kita
load_custom_css()

# --- Judul Halaman ---
st.title("🧑‍🔬 Mentor Data Science (Pro)")
st.write(
    "Dari SQL query sampai Deep Learning, tanyain aja ke Mentor! "
    "Ditenagai oleh Google Gemini."
)


# --- SIDEBAR (Tetap sama) ---
with st.sidebar:
    st.header("🧑‍🔬 Tentang Mentor")
    st.write("""
    Mentor ini adalah asisten AI Anda untuk semua hal tentang Data Science. 
    Tanyakan apa saja, dari dasar Python hingga arsitektur Deep Learning.
    """)
    
    st.divider() 

    api_key_provided = bool(st.session_state.get("api_key_input"))

    with st.expander("🔑 Konfigurasi API", expanded=not api_key_provided):
        google_api_key = st.text_input(
            "Google API Key", 
            type="password", 
            key="api_key_input",
            label_visibility="collapsed", 
            placeholder="Masukkan Google API key Anda..."
        )
        if api_key_provided:
            st.success("API Key aktif!", icon="✅")
        elif google_api_key:
             st.rerun() 
        else:
            st.info("Masukkan Google API key Anda untuk memulai.", icon="🗝️")
    
    st.divider() 
    
    if st.button("Mulai Obrolan Baru", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun() 

# =========================================================


# === Logika Utama Aplikasi (Tetap sama) ===
session_api_key = st.session_state.get("api_key_input", "")

if not session_api_key:
    st.info("Silakan masukkan Google API key Anda di sidebar kiri untuk melanjutkan.", icon="👈")
else:
    genai.configure(api_key=session_api_key)

    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=enrollment_tool
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🧑‍🔬"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ada yang bisa dibantu, Bro?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        google_messages_history = []
        for msg in st.session_state.messages:
            role = "model" if msg["role"] == "assistant" else msg["role"]
            google_messages_history.append({"role": role, "parts": [msg["content"]]})

        with st.spinner("Mentor sedang berpikir... 🤔"):
            try:
                response = model.generate_content(google_messages_history)
                
                part = response.candidates[0].content.parts[0]
                
                if part.function_call:
                    fc = part.function_call
                    
                    with st.chat_message("assistant", avatar="🧑‍🔬"):
                        st.markdown(f"Oke, sedang memproses: `{fc.name}`...")
                    
                    model_response_content = response.candidates[0].content
                    google_messages_history.append({
                        "role": model_response_content.role,
                        "parts": model_response_content.parts
                    })

                    show_balloons = False 
                    
                    if fc.name == "enroll_in_course":
                        args = fc.args
                        user_name = args.get("user_name", "Siswa") 
                        course_name = args.get("course_name", "Kursus Data Science")
                        function_result = enroll_in_course(course_name, user_name)
                        show_balloons = True 
                    
                    else:
                        function_result = json.dumps({"status": "error", "message": "Tool tidak dikenal"})

                    function_response_part = {
                        "function_response": {
                            "name": fc.name,
                            "response": {"content": function_result},
                        }
                    }
                    google_messages_history.append(function_response_part)
                    
                    second_response = model.generate_content(google_messages_history)
                    final_text = second_response.text

                else:
                    final_text = response.text
                    show_balloons = False

                st.session_state.messages.append({"role": "assistant", "content": final_text})
                with st.chat_message("assistant", avatar="🧑‍🔬"):
                    st.markdown(final_text)
                
                if show_balloons:
                    st.balloons()

            except Exception as e:
                st.error(f"Terjadi error: {e}")
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()