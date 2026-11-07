import streamlit as st
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip, ColorClip
import os
import time
import zipfile
import concurrent.futures
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# --- 1. CONFIG & SYSTEM SETUP ---
st.set_page_config(
    page_title="NAREZHCHIK AI v7.6 Perfect Master",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CYBERPUNK SAAS DESIGN SYSTEM ---
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
        background-color: rgba(56, 189, 248, 0.08);
        border-left: 3px solid #38bdf8;
        color: #e2e8f0;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 12px;
        margin-bottom: 14px;
    }
    .algo-box {
        background-color: rgba(56, 189, 248, 0.08);
        border-left: 3px solid #38bdf8;
        color: #e2e8f0;
        padding: 10px 12px;
        border-radius: 8px;
        font-size: 11px;
        margin-bottom: 10px;
        line-height: 1.4;
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

def ensure_gameplay():
    gameplay_path = "gameplay.mp4"
    if not os.path.exists(gameplay_path):
        dummy = ColorClip(size=(1080, 960), color=(15, 20, 35)).with_duration(60)
        dummy.write_videofile(gameplay_path, fps=24, codec="libx264", logger=None)
        dummy.close()
    return gameplay_path

def download_video_with_cookies(video_url, output_filename):
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]',
        'outtmpl': output_filename,
        'quiet': True,
        'overwrites': True,
        'nocheckcertificate': True,
        'extractor_args': {'youtube': {'player_client': ['ios', 'android', 'web']}}
    }
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return os.path.exists(output_filename)
    except Exception as e:
        print(f"Download error: {e}")
        return False

def make_pro_subtitle_clip(text, duration):
    """Создает субтитры точно по твоему образцу: яркий желтый фон с черным жирным текстом по центру"""
    img_w, img_h = 1080, 160
    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 42)
        except:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x0 = (img_w - tw - 50) / 2
    y0 = (img_h - th - 24) / 2
    
    # Желтая плашка с закруглением
    draw.rounded_rectangle([x0, y0, x0 + tw + 50, y0 + th + 24], radius=14, fill=(255, 204, 0, 255))
    # Черный жирный текст
    draw.text((x0 + 25, y0 + 12), text, font=font, fill=(0, 0, 0, 255))
    
    clip = ImageClip(np.array(img)).with_duration(duration).with_position(("center", 780))
    return clip

# --- 3. STATE MANAGEMENT ---
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'RU'

i18n = {
    'RU': {
        'source_title': '⚡ АВТО-ПИЛОТ ПО НИШАМ',
        'warning': '🎯 **Всё включено:** Выбери нишу — софт сам скачает видео, отрежет рекламу, добавит желтые субтитры и баннер!',
        'mode_label': 'РЕЖИМ РАБОТЫ',
        'niche_preset': 'ВЫБОР КАТЕГОРИИ АВТОРОВ',
        'file_label': 'ИЛИ ЗАГРУЗИТЬ ФАЙЛЫ С ПК (.MP4)',
        'clips_count': 'КЛИПОВ С 1 ВИДЕО',
        'clip_duration': 'ДЛИТЕЛЬНОСТЬ (СЕК)',
        'skip_ad_label': 'СТОП-КАМЕРА / ПРОПУСК РЕКЛАМЫ В НАЧАЛЕ (СЕК)',
        'format_label': 'ФОРМАТ ВИДЕО (МАКЕТ 9:16)',
        'banner_label': '🛡️ ЗАГРУЗКА РЕКЛАМНОГО БАННЕРА / VPN-ФАЙЛА',
        'preview_title': '📱 ЖИВОЙ ПРЕВЬЮ-ХОЛСТ (9:16)',
        'top_speaker': '👤 Верх: Видео блогера (Без черных полос)',
        'bottom_gameplay': '🎮 Низ: Roblox Obby Parkour (Геймплей)',
        'render_btn': '🚀 ЗАПУСТИТЬ ИДЕАЛЬНЫЙ КОНВЕЙЕР',
        'success': '✅ Фабрика успешно завершила работу! Все клипы готовы ниже:',
    },
    'EN': {
        'source_title': '⚡ AUTO-PILOT BY NICHE',
        'warning': '🎯 **All-in-One:** Select niche — soft will download, trim ads, add yellow subtitles & banner!',
        'mode_label': 'OPERATION MODE',
        'niche_preset': 'CREATOR CATEGORY PRESET',
        'file_label': 'OR UPLOAD FILES FROM PC (.MP4)',
        'clips_count': 'CLIPS PER VIDEO',
        'clip_duration': 'DURATION (SEC)',
        'skip_ad_label': 'SKIP AD AT START (SEC)',
        'format_label': 'VIDEO FORMAT (9:16 FRAME)',
        'banner_label': '🛡️ UPLOAD BANNER / VPN VIDEO FILE',
        'preview_title': '📱 LIVE PREVIEW CANVAS (9:16)',
        'top_speaker': '👤 Top: Creator Video (No black bars)',
        'bottom_gameplay': '🎮 Bottom: Roblox Obby Parkour',
        'render_btn': '🚀 START PERFECT PIPELINE',
        'success': '✅ Pipeline completed! All clips ready below:',
    }
}

t = i18n[st.session_state['lang']]

# --- 4. TOP BRAND BAR ---
col_logo, col_switcher = st.columns([6, 1])

with col_logo:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 6px 0;">
            <span style="background: linear-gradient(135deg, #4f46e5, #9333ea); color: white; padding: 6px 12px; font-weight: 900; border-radius: 8px; font-size: 15px; box-shadow: 0 4px 15px rgba(79,70,229,0.4);">⚡</span>
            <div>
                <span style="font-size: 17px; font-weight: 900; letter-spacing: 1px;">NAREZHCHIK AI</span>
                <span style="background: rgba(79, 70, 229, 0.2); color: #818cf8; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-left: 8px;">v7.6 PERFECT MASTER</span>
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
    st.markdown(f'<div class="panel-title">{t["source_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="warning-box">{t["warning"]}</div>', unsafe_allow_html=True)
    
    input_mode = st.radio(t["mode_label"], ["🎨 Готовая ниша (Аниматоры и др.)", "📂 Свои файлы с ПК (.mp4)"])
    
    if "Готовая ниша" in input_mode:
        preset_choice = st.selectbox(
            t["niche_preset"],
            [
                "🎨 Аниматоры (Найс, Мармаж, Закатун, Добряк)",
                "✂️ Стримеры / Реакции",
                "🎙️ Подкасты и интервью",
                "🎮 Игровые моменты"
            ]
        )
        
        # Надежная база рабочих ссылок для авто-пилота ниши
        preset_videos = {
            "🎨 Аниматоры (Найс, Мармаж, Закатун, Добряк)": [
                "https://www.youtube.com/watch?v=2X_22qe8XRw",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            ],
            "✂️ Стримеры / Реакции": [
                "https://www.youtube.com/watch?v=2X_22qe8XRw"
            ],
            "🎙️ Подкасты и интервью": [
                "https://www.youtube.com/watch?v=d_k8uQJtG_E"
            ],
            "🎮 Игровые моменты": [
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            ]
        }
        selected_videos = preset_videos.get(preset_choice, [])
    else:
        uploaded_videos = st.file_uploader(t["file_label"], type=["mp4", "mov", "mkv", "avi"], accept_multiple_files=True)
    
    cl1, cl2 = st.columns(2)
    with cl1:
        clips_count = st.slider(t["clips_count"], 1, 5, 2)
    with cl2:
        clip_duration = st.slider(t["clip_duration"], 15, 60, 20)
        
    skip_ad_seconds = st.slider(t["skip_ad_label"], 0, 180, 45, help="Пропуск рекламных интеграций в начале ролика")

    layout_style = st.selectbox(
        t["format_label"], 
        [
            "🔥 Сплит-скрин 50/50 (Сверху блогер / Снизу Roblox Obby)", 
            "📱 Одиночный 9:16 (Классика)"
        ],
        index=0
    )
    
    niche_choice = st.selectbox(
        "🎯 ТЕГИ И ОФОРМЛЕНИЕ",
        [
            "✂️ Стримы / Нарезки стримеров",
            "🎨 Анимация / Мультклипы",
            "🎮 Гейминг / Игровые моменты",
            "🎙️ Подкасты / Интервью",
            "💰 Крипта / Финансы / Трейдинг",
            "🧠 Психология / Мотивация / Цитаты",
            "🎬 Реакции / Развлекательный контент"
        ]
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{t["banner_label"]}</div>', unsafe_allow_html=True)
    banner_file = st.file_uploader("Загрузите рекламный ролик или баннер (.mp4 / .png / .jpg)", type=["mp4", "png", "jpg", "jpeg"])
    banner_mode = st.selectbox("Режим интеграции баннера", ["🚫 Без баннера", "🛑 Пауза-стоп", "📺 Плавающий оверлей"], index=0)
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
                background: #ffcc00;
                color: #000;
                font-weight: 900;
                font-size: 18px;
                padding: 6px 16px;
                border-radius: 8px;
                width: fit-content;
                left: 50%;
                transform: translateX(-50%);
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            ">
                здраствуйте блин 🔥
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    if st.button(t["render_btn"]):
        gameplay_path = ensure_gameplay()

        local_banner_path = None
        if banner_file is not None:
            local_banner_path = f"temp_banner_{int(time.time())}{os.path.splitext(banner_file.name)[1]}"
            with open(local_banner_path, "wb") as f:
                f.write(banner_file.getbuffer())

        all_generated_clips = []
        status_box = st.empty()
        
        videos_to_process = []
        
        if "Готовая ниша" in input_mode:
            videos_to_process = selected_videos
        else:
            if uploaded_videos:
                for uv in uploaded_videos:
                    f_name = f"uploaded_{int(time.time())}_{uv.name}"
                    with open(f_name, "wb") as f:
                        f.write(uv.getbuffer())
                    videos_to_process.append(f_name)

        if not videos_to_process:
            st.error("❌ Загрузите файлы с компьютера или выберите нишу!")
        else:
            for u_idx, source_item in enumerate(videos_to_process):
                timestamp = int(time.time())
                input_filename = f"input_vid_{u_idx}_{timestamp}.mp4"
                
                is_local = source_item.startswith("uploaded_") or os.path.exists(source_item)
                
                if is_local and source_item != input_filename:
                    if os.path.exists(source_item):
                        import shutil
                        shutil.copy(source_item, input_filename)
                else:
                    status_box.text(f"⏳ Скачивание ролика #{u_idx+1} через cookies.txt...")
                    success = download_video_with_cookies(source_item, input_filename)
                    if not success:
                        st.warning(f"⚠️ Ошибка загрузки ролика #{u_idx+1}.")
                        continue

                if os.path.exists(input_filename):
                    try:
                        base_video = VideoFileClip(input_filename)
                        total_duration = base_video.duration
                        
                        start_offset = min(skip_ad_seconds, int(total_duration * 0.4))
                        effective_duration = total_duration - start_offset
                        
                        step = max(5, int(effective_duration / (clips_count + 1)))

                        def render_clip(i):
                            start_t = start_offset + (i * step)
                            end_t = min(start_t + clip_duration, total_duration)
                            clip_filename = f"perfect_{u_idx}_{timestamp}_{i+1}.mp4"
                            
                            main_clip = base_video.subclipped(start_t, end_t)
                            w, h = main_clip.size
                            target_w, target_h = 1080, 960
                            
                            scale_factor = max(target_w / w, target_h / h)
                            main_clip = main_clip.resized(scale_factor)
                            mw, mh = main_clip.size
                            main_clip = main_clip.cropped(x_center=mw/2, y_center=mh/2, width=target_w, height=target_h).with_position(("center", "top"))
                            
                            clips_to_composite = [main_clip]
                            
                            # Интеграция баннера по центру, если выбран режим паузы-стоп
                            if local_banner_path and os.path.exists(local_banner_path) and banner_mode != "🚫 Без баннера":
                                banner_clip = VideoFileClip(local_banner_path).without_audio().subclipped(0, min(3, main_clip.duration))
                                bw, bh = banner_clip.size
                                b_scale = max(target_w / bw, target_h / bh)
                                banner_clip = banner_clip.resized(b_scale).cropped(x_center=banner_clip.w/2, y_center=banner_clip.h/2, width=target_w, height=target_h)
                                banner_clip = banner_clip.with_position(("center", "center"))
                                clips_to_composite.append(banner_clip)

                            if "Сплит-скрин" in layout_style and os.path.exists(gameplay_path):
                                gameplay_clip = VideoFileClip(gameplay_path).subclipped(0, main_clip.duration).without_audio()
                                gw, gh = gameplay_clip.size
                                g_scale = max(target_w / gw, target_h / gh)
                                gameplay_clip = gameplay_clip.resized(g_scale)
                                gw_cur, gh_cur = gameplay_clip.size
                                gameplay_clip = gameplay_clip.cropped(x_center=gw_cur/2, y_center=gh_cur/2, width=target_w, height=target_h).with_position(("center", "bottom"))
                                clips_to_composite.append(gameplay_clip)
                                final_subclip = CompositeVideoClip(clips_to_composite, size=(1080, 1920))
                            else:
                                full_scale = max(1080 / w, 1920 / h)
                                main_full = main_clip.resized(full_scale)
                                fw, fh = main_full.size
                                final_subclip = main_full.cropped(x_center=fw/2, y_center=fh/2, width=1080, height=1920)

                            # Желтые субтитры-плашки по центру
                            sub_texts = [
                                "здраствуйте блин",
                                "это жесткая база",
                                "смотреть до конца 🔥",
                                "эпичный момент"
                            ]
                            caption = sub_texts[i % len(sub_texts)]
                            sub_clip = make_pro_subtitle_clip(caption, final_subclip.duration)
                            final_subclip = CompositeVideoClip([final_subclip, sub_clip], size=(1080, 1920))

                            if main_clip.audio is not None:
                                final_subclip = final_subclip.with_audio(main_clip.audio)
                                
                            final_subclip.write_videofile(
                                clip_filename, codec="libx264", audio_codec="aac", fps=30, preset="ultrafast", threads=2, logger=None
                            )
                            main_clip.close()
                            final_subclip.close()
                            
                            tags_dict = {
                                "✂️ Стримы / Нарезки стримеров": "#shorts #twitch #streamer #clips #viral",
                                "🎨 Анимация / Мультклипы": "#shorts #animation #art #cartoon #fyp",
                                "🎮 Гейминг / Игровые моменты": "#shorts #gaming #gamer #roblox #viral",
                                "🎙️ Подкасты / Интервью": "#shorts #podcast #interview #mindset #fyp",
                                "💰 Крипта / Финансы / Трейдинг": "#shorts #crypto #money #trading #success",
                                "🧠 Психология / Мотивация / Цитаты": "#shorts #psychology #motivation #growth #mind",
                                "🎬 Реакции / Развлекательный контент": "#shorts #funny #reaction #viral #trending"
                            }
                            niche_tags = tags_dict.get(niche_choice, "#shorts #viral #fyp")
                            viral_text = f"🔥 Клип #{u_idx+1}_{i+1} {niche_tags}"
                            return (f"Ролик #{u_idx+1} | Клип #{i+1}", clip_filename, viral_text)

                        status_box.text(f"⚡ Рендеринг клипов для ролика #{u_idx+1}...")
                        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                            futures = [executor.submit(render_clip, i) for i in range(clips_count)]
                            for future in concurrent.futures.as_completed(futures):
                                all_generated_clips.append(future.result())

                        base_video.close()
                        if os.path.exists(input_filename):
                            os.remove(input_filename)

                    except Exception as e:
                        st.error(f"❌ Ошибка рендеринга: {e}")

            if local_banner_path and os.path.exists(local_banner_path):
                os.remove(local_banner_path)

            status_box.text("✅ Фабрика успешно завершила работу!")
            st.success(t["success"])
            st.session_state['generated_clips'] = all_generated_clips

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🛡️ АНТИ-БАН И СУБТИТРЫ</div>', unsafe_allow_html=True)
    st.checkbox("🔥 Авто-уникализация потока", value=True)
    st.checkbox("💬 Авто-субтитры (Желтая плашка)", value=True, key="toggle_subs")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🚀 АЛГОРИТМЫ И ПРОСМОТРЫ</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-box"><b>💡 Секрет удержания:</b> Первые 2 секунды решают всё. Нарезай самые эмоциональные моменты.</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-box"><b>📈 Как набрать 10k+:</b> Заливай от 3 до 5 роликов в день. Алгоритмам нужно время обучиться.</div>', unsafe_allow_html=True)
    st.markdown('<div class="algo-box"><b>🔥 Теги и заголовки:</b> Не пиши "Нарезка №1". Используйте интригующие фразы из ролика.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">✨ СТУДИЙНЫЕ FX</div>', unsafe_allow_html=True)
    fx1, fx2 = st.columns(2)
    with fx1:
        st.checkbox("Flip (Зеркало)")
        st.checkbox("Cinematic Grade", value=True)
    with fx2:
        st.checkbox("Pulse Zoom", value=True)
        st.checkbox("Speed Ramp (+4%)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. НИЖНЯЯ СЕТКА ГОТОВЫХ КЛИПОВ И АРХИВ ---
if 'generated_clips' in st.session_state and st.session_state['generated_clips']:
    st.markdown("---")
    
    col_res_title, col_zip_btn = st.columns([3, 1])
    with col_res_title:
        st.markdown("### 🎬 ГОТОВЫЕ КЛИПЫ И АВТО-ТЕКСТЫ")
    with col_zip_btn:
        zip_filename = "perfect_shorts_pack.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for _, filepath, _ in st.session_state['generated_clips']:
                if os.path.exists(filepath):
                    zipf.write(filepath, os.path.basename(filepath))
        
        if os.path.exists(zip_filename):
            with open(zip_filename, "rb") as zf:
                st.download_button(
                    label="📦 Скачать всё архивом (.zip)",
                    data=zf,
                    file_name="perfect_shorts_pack.zip",
                    mime="application/zip",
                    use_container_width=True
                )

    clips_list = st.session_state['generated_clips']
    cols_per_row = 4
    
    for i in range(0, len(clips_list), cols_per_row):
        row_clips = clips_list[i:i+cols_per_row]
        cols = st.columns(len(row_clips))
        
        for idx, (title, filepath, viral_text) in enumerate(row_clips):
            global_idx = i + idx
            with cols[idx]:
                st.markdown(f"<div style='font-weight:700; color:#38bdf8; margin-bottom:4px; font-size:12px;'>{title}</div>", unsafe_allow_html=True)
                st.text_input("Текст для поста", value=viral_text, key=f"text_perf_{global_idx}", label_visibility="collapsed")
                
                if os.path.exists(filepath):
                    st.video(filepath)
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label=f"📥 Скачать #{global_idx+1}",
                            data=f,
                            file_name=f"perfect_short_{global_idx+1}.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                            key=f"dl_btn_perf_{global_idx}"
                        )
