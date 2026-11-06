import streamlit as st
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import os
import time

# --- 1. CONFIG & SYSTEM SETUP ---
st.set_page_config(
    page_title="NAREZHCHIK AI v6.3 Pro Banner Factory",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED CYBERPUNK SAAS DESIGN SYSTEM ---
st.markdown("""
    <style>
    .stApp {
        background-color: #05060a;
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .panel-card {
        background: #0e111a;
        border: 1px solid #1a2238;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: border 0.3s ease;
    }
    .panel-card:hover {
        border-color: #4f46e5;
    }
    .panel-title {
        font-size: 13px;
        font-weight: 800;
        color: #38bdf8;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }
    .warning-box {
        background-color: rgba(245, 158, 11, 0.08);
        border-left: 3px solid #f59e0b;
        color: #fcd34d;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 12px;
        margin-bottom: 14px;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        font-weight: 800;
        font-size: 14px;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.5);
        width: 100%;
        transition: all 0.25s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(147, 51, 234, 0.7);
    }
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #05060a !important;
        border: 1px solid #1e263d !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Функция для авто-скачивания геймплея в облаке, если его нет
def ensure_gameplay():
    gameplay_path = "gameplay.mp4"
    if not os.path.exists(gameplay_path):
        url = "https://www.youtube.com/watch?v=2X_22qe8XRw" 
        ydl_opts = {
            'format': 'bestvideo[height<=720][ext=mp4]/best[height<=720]',
            'outtmpl': gameplay_path,
            'quiet': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except:
            pass
    return gameplay_path

# --- 3. STATE MANAGEMENT FOR LANGUAGE ---
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'RU'

i18n = {
    'RU': {
        'download_title': '📥 МАССОВЫЙ КОНВЕЙЕР ССЫЛОК',
        'warning': '⚠️ **Совет:** Каждую ссылку вставляй с новой строки.',
        'url_label': 'СПИСОК ССЫЛОК НА YOUTUBE / TIKTOK (ПО 1 НА СТРОКУ)',
        'clips_count': 'КЛИПОВ С 1 ВИДЕО',
        'clip_duration': 'ДЛИТЕЛЬНОСТЬ (СЕК)',
        'format_label': 'ФОРМАТ ВИДЕО (МАКЕТ 9:16)',
        'banner_label': '🛡️ ЗАГРУЗКА РЕКЛАМНОГО БАННЕРА / VPN-ФАЙЛА',
        'preview_title': '📱 ЖИВОЙ ПРЕВЬЮ-ХОЛСТ (9:16)',
        'top_speaker': '👤 Верх: Видео блогера (Без черных полос)',
        'bottom_gameplay': '🎮 Низ: Roblox Obby Parkour (Геймплей)',
        'render_btn': '🚀 ЗАПУСТИТЬ ФАБРИКУ С ИНТЕГРАЦИЕЙ БАННЕРА',
        'success': '✅ Массовая фабрика завершила работу! Все клипы с баннером готовы:',
    },
    'EN': {
        'download_title': '📥 MASSIVE BATCH PIPELINE',
        'warning': '⚠️ **Tip:** Put each URL on a new line.',
        'url_label': 'YOUTUBE / TIKTOK URLS (ONE PER LINE)',
        'clips_count': 'CLIPS PER VIDEO',
        'clip_duration': 'DURATION (SEC)',
        'format_label': 'VIDEO FORMAT (9:16 FRAME)',
        'banner_label': '🛡️ UPLOAD BANNER / VPN VIDEO FILE',
        'preview_title': '📱 LIVE PREVIEW CANVAS (9:16)',
        'top_speaker': '👤 Top: Creator Video (No black bars)',
        'bottom_gameplay': '🎮 Bottom: Roblox Obby Parkour',
        'render_btn': '🚀 START BATCH FACTORY WITH BANNER',
        'success': '✅ Batch factory completed! All clips ready below:',
    }
}

t = i18n[st.session_state['lang']]

# --- 4. TOP BRAND BAR WITH LANGUAGE SWITCHER ---
col_logo, col_switcher = st.columns([6, 1])

with col_logo:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 6px 0;">
            <span style="background: linear-gradient(135deg, #4f46e5, #9333ea); color: white; padding: 6px 12px; font-weight: 900; border-radius: 8px; font-size: 15px; box-shadow: 0 4px 15px rgba(79,70,229,0.4);">🛡️</span>
            <div>
                <span style="font-size: 17px; font-weight: 900; letter-spacing: 1px;">NAREZHCHIK AI</span>
                <span style="background: rgba(79, 70, 229, 0.2); color: #818cf8; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-left: 8px;">v6.3 PRO BANNER</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_switcher:
    lang_choice = st.selectbox("Lang", ["RU", "EN"], index=0 if st.session_state['lang']=='RU' else 1, label_visibility="collapsed")
    if lang_choice != st.session_state['lang']:
        st.session_state['lang'] = lang_choice
        st.rerun()

# --- 5. LAYOUT ---
col_left, col_center, col_right = st.columns([1.1, 1.4, 1.1])

with col_left:
    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{t["download_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="warning-box">{t["warning"]}</div>', unsafe_allow_html=True)
    
    raw_urls = st.text_area(t["url_label"], placeholder="https://youtu.be/url1\nhttps://youtu.be/url2", height=90)
    
    cl1, cl2 = st.columns(2)
    with cl1:
        clips_count = st.slider(t["clips_count"], 1, 5, 2)
    with cl2:
        clip_duration = st.slider(t["clip_duration"], 15, 60, 20)
        
    layout_style = st.selectbox(
        t["format_label"], 
        [
            "🔥 Сплит-скрин 50/50 (Сверху блогер / Снизу Roblox Obby)", 
            "📱 Одиночный 9:16 (Классика)"
        ],
        index=0
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Слот для загрузки файла баннера
    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{t["banner_label"]}</div>', unsafe_allow_html=True)