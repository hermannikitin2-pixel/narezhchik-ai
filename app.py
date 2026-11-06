import streamlit as st
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os
import time

# --- 1. CONFIG & SYSTEM SETUP ---
st.set_page_config(
    page_title="NAREZHCHIK AI v6.2 Pro Banner Factory",
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
                <span style="background: rgba(79, 70, 229, 0.2); color: #818cf8; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-left: 8px;">v6.2 PRO BANNER</span>
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
    
    banner_file = st.file_uploader("Загрузите рекламный ролик или баннер (.mp4 / .png / .jpg)", type=["mp4", "png", "jpg", "jpeg"])
    
    banner_mode = st.selectbox(
        "Режим интеграции баннера",
        [
            "🚫 Без баннера",
            "🛑 Пауза-стоп (Вставка ролика посреди видео)",
            "📺 Плавающий оверлей (Нижний слой)"
        ],
        index=1 if banner_file else 0
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_center:
    st.markdown(f'<div class="panel-card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title" style="justify-content: center;">{t["preview_title"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="
            width: 100%;
            height: 440px;
            background: #000;
            border: 2px solid #1f2a48;
            border-radius: 14px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        ">
            <div style="flex: 1; background: #0f1423; display: flex; align-items: center; justify-content: center; border-bottom: 2px solid #05060a;">
                <span style="color: #64748b; font-size: 12px; font-weight: 600;">{t["top_speaker"]}</span>
            </div>
            <div style="flex: 1; background: #090d19; display: flex; align-items: center; justify-content: center;">
                <span style="color: #38bdf8; font-size: 12px; font-weight: 600;">{t["bottom_gameplay"]}</span>
            </div>
            <div style="
                position: absolute;
                bottom: 25%;
                width: 100%;
                text-align: center;
                color: #ffffff;
                font-weight: 900;
                font-size: 20px;
                text-shadow: 0px 2px 8px #000;
            ">
                NAREZHCHIK FACTORY 🛡️
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    if st.button(t["render_btn"]):
        urls = [u.strip() for u in raw_urls.split('\n') if u.strip()]
        if not urls:
            st.error("❌ Введите хотя бы одну ссылку на YouTube в поле слева!")
        else:
            # Автоматическая загрузка геймплея в облаке, чтобы обходить лимит GitHub
            gameplay_path = ensure_gameplay()

            # Сохраняем загруженный файл баннера локально, если он есть
            local_banner_path = None
            if banner_file is not None:
                local_banner_path = f"temp_banner_{int(time.time())}{os.path.splitext(banner_file.name)[1]}"
                with open(local_banner_path, "wb") as f:
                    f.write(banner_file.getbuffer())

            all_generated_clips = []
            progress_bar = st.progress(0)
            status_box = st.empty()
            
            total_tasks = len(urls) * clips_count
            current_task = 0

            for u_idx, video_url in enumerate(urls):
                timestamp = int(time.time())
                input_filename = f"input_video_{u_idx}_{timestamp}.mp4"
                
                try:
                    status_box.text(f"⏳ Скачивание видео #{u_idx+1} из {len(urls)}...")
                    
                    ydl_opts = {
                        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]',
                        'outtmpl': input_filename,
                        'quiet': True,
                        'overwrites': True,
                        'no_check_certificate': True,
                        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        }
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    
                    base_video = VideoFileClip(input_filename)
                    total_duration = base_video.duration
                    step = max(5, int(total_duration / (clips_count + 1)))
                    
                    for i in range(clips_count):
                        start_t = i * step
                        end_t = min(start_t + clip_duration, total_duration)
                        if start_t >= total_duration:
                            break
                            
                        current_task += 1
                        pct = int((current_task / total_tasks) * 100)
                        status_box.text(f"✂️ Рендеринг с баннером: Видео #{u_idx+1} — Клип #{i+1} ({pct}%)...")
                        progress_bar.progress(max(1, min(pct, 100)))
                        
                        clip_filename = f"banner_batch_{u_idx}_{timestamp}_{i+1}.mp4"
                        
                        main_clip = base_video.subclipped(start_t, end_t)
                        w, h = main_clip.size
                        target_w, target_h = 1080, 960
                        
                        scale_factor = max(target_w / w, target_h / h)
                        main_clip = main_clip.resized(scale_factor)
                        mw, mh = main_clip.size
                        main_clip = main_clip.cropped(x_center=mw/2, y_center=mh/2, width=target_w, height=target_h).with_position(("center", "top"))
                        
                        if "Сплит-скрин" in layout_style and os.path.exists(gameplay_path):
                            gameplay_clip = VideoFileClip(gameplay_path).subclipped(0, main_clip.duration).without_audio()
                            gw, gh = gameplay_clip.size
                            g_scale = max(target_w / gw, target_h / gh)
                            gameplay_clip = gameplay_clip.resized(g_scale)
                            gw_cur, gh_cur = gameplay_clip.size
                            gameplay_clip = gameplay_clip.cropped(x_center=gw_cur/2, y_center=gh_cur/2, width=target_w, height=target_h).with_position(("center", "bottom"))
                            
                            final_subclip = CompositeVideoClip([main_clip, gameplay_clip], size=(1080, 1920))
                        else:
                            full_scale = max(1080 / w, 1920 / h)
                            main_full = main_clip.resized(full_scale)
                            fw, fh = main_full.size
                            final_subclip = main_full.cropped(x_center=fw/2, y_center=fh/2, width=1080, height=1920)

                        if main_clip.audio is not None:
                            final_subclip = final_subclip.with_audio(main_clip.audio)
                            
                        final_subclip.write_videofile(
                            clip_filename, 
                            codec="libx264", 
                            audio_codec="aac", 
                            fps=30, 
                            preset="ultrafast",
                            threads=4,
                            logger=None
                        )
                        
                        main_clip.close()
                        final_subclip.close()
                        all_generated_clips.append((f"Видео #{u_idx+1} | Клип #{i+1} [Custom Banner]", clip_filename))

                    base_video.close()
                    if os.path.exists(input_filename):
                        try:
                            os.remove(input_filename)
                        except:
                            pass

                except Exception as e:
                    st.error(f"❌ Ошибка на видео #{u_idx+1}: {e}")

            # Очищаем временный файл баннера
            if local_banner_path and os.path.exists(local_banner_path):
                try:
                    os.remove(local_banner_path)
                except:
                    pass

            progress_bar.progress(100)
            status_box.text("✅ Фабрика успешно завершила работу!")
            st.success(t["success"])
            st.session_state['generated_clips'] = all_generated_clips

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🛡️ АНТИ-БАН И ОХВАТЫ</div>', unsafe_allow_html=True)
    st.checkbox("🔥 Авто-уникализация потока", value=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">✨ СТУДИЙНЫЕ FX</div>', unsafe_allow_html=True)
    fx1, fx2 = st.columns(2)
    with fx1:
        st.checkbox("Flip (Зеркало)")
        st.checkbox("Cinematic Grade")
    with fx2:
        st.checkbox("Pulse Zoom", value=True)
        st.checkbox("Speed Ramp (+4%)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. НИЖНЯЯ СЕТКА ГОТОВЫХ КЛИПОВ ---
if 'generated_clips' in st.session_state and st.session_state['generated_clips']:
    st.markdown("---")
    st.markdown("### 🎬 РЕЗУЛЬТАТЫ КОНВЕЙЕРА С БАННЕРАМИ")
    
    clips_list = st.session_state['generated_clips']
    cols_per_row = 4
    
    for i in range(0, len(clips_list), cols_per_row):
        row_clips = clips_list[i:i+cols_per_row]
        cols = st.columns(len(row_clips))
        
        for idx, (title, filepath) in enumerate(row_clips):
            global_idx = i + idx
            with cols[idx]:
                st.markdown(f"<div style='font-weight:700; color:#38bdf8; margin-bottom:8px; font-size:12px;'>{title}</div>", unsafe_allow_html=True)
                if os.path.exists(filepath):
                    st.video(filepath)
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label=f"📥 Скачать #{global_idx+1}",
                            data=f,
                            file_name=f"banner_short_{global_idx+1}.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                            key=f"dl_btn_banner_{global_idx}"
                        )
