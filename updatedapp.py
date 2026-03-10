import streamlit as st
import uuid
import sys
import os
import hashlib

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api.recommendation_endpoint import HybridRecommendationSystem

# CONFIGURATION & THEME

st.set_page_config(
    page_title="Wellness Sanctuary",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium Sanctuary Styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');
    
    .stApp {
        background-color: #FFFFFF;
        color: #2F3437;
    }
    
    .main .block-container {
        max-width: 1000px;
        padding-top: 3rem;
        margin: auto;
    }

    h1, h2, h3, .playfair {
        font-family: 'Playfair Display', serif !important;
        color: #1A1C1D !important;
        font-weight: 700 !important;
    }
    
    p, span, div, label, .inter {
        font-family: 'Inter', sans-serif !important;
        color: #4A4E51 !important;
    }

    .yoga-image-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 3rem;
        position: relative;
    }
    .yoga-image {
        width: 280px;
        border-radius: 16px;
        opacity: 0.9;
        transition: transform 0.4s ease, opacity 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }
    .yoga-image:hover {
        opacity: 1;
        transform: translateY(-5px);
    }

    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1px solid #E1E4E6 !important;
        padding: 0.8rem 1.2rem !important;
        background-color: #F9FAFB !important;
        font-size: 1rem !important;
        color: #1A1C1D !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4A675A !important;
        background-color: #FFFFFF !important;
    }
    
    [data-baseweb="input"] {
        border-color: transparent !important;
    }

    .stButton > button {
        background-color: #4A675A !important;
        color: #FFFFFF !important;
        border-radius: 30px !important;
        padding: 0.75rem 2.5rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px 6px rgba(74, 103, 90, 0.2) !important;
    }
    
    .stButton > button:hover {
        background-color: #3D554A !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(74, 103, 90, 0.3) !important;
        color: #FFFFFF !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .video-card {
        background: #FFFFFF;
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.03);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        margin-bottom: 2rem;
        height: 100%;
        position: relative;
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    .video-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(74, 103, 90, 0.1) !important;
        border: 1px solid #7B9E89;
    }
    
    .card-thumb {
        width: 100%;
        aspect-ratio: 16 / 9;
        object-fit: cover;
    }
    
    .card-content {
        padding: 1.5rem;
    }
    
    .match-pill {
        display: inline-block;
        background-color: #E7F2EC;
        color: #4A675A;
        padding: 0.2rem 0.8rem;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }
    
    .video-title {
        font-size: 1.3rem;
        font-family: 'Playfair Display', serif !important;
        line-height: 1.3;
        margin-bottom: 0.5rem;
        color: #1A1C1D !important;
    }

    .breathing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 6rem 0;
    }

    .breathing-circle {
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(255,140,0,0.4) 0%, rgba(0,191,255,0.2) 50%, rgba(255,255,255,0) 70%);
        border: 1px solid rgba(255,140,0,0.1);
        border-radius: 50%;
        animation: breathe 5s ease-in-out infinite;
    }

    @keyframes breathe {
        0%, 100% { transform: scale(0.8); opacity: 0.3; background: radial-gradient(circle, rgba(255,140,0,0.4) 0%, rgba(0,191,255,0.2) 70%); }
        50% { transform: scale(1.6); opacity: 0.8; background: radial-gradient(circle, rgba(0,191,255,0.4) 0%, rgba(255,140,0,0.2) 70%); }
    }

    .breathing-text {
        margin-top: 3rem;
        font-family: 'Playfair Display', serif;
        font-style: italic;
        color: #4A675A;
        font-size: 1.4rem;
        letter-spacing: 0.02em;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    .stDeployButton {display:none;}
    
    .stExpander {
        border: none !important;
        background: #F9FAFB !important;
        border-radius: 12px !important;
        margin-top: 1rem !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
    }

    .feedback-container {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
        padding: 0.5rem 0;
    }
    
    .feedback-btn {
        background: none !important;
        border: 1px solid #E1E4E6 !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-size: 1.2rem !important;
        padding: 0 !important;
    }

    .feedback-btn:hover {
        background-color: #F0F2F0 !important;
        border-color: #4A675A !important;
        transform: scale(1.1);
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# FIX: Added last_query_id so clear_sanctuary() never throws KeyError
# ─────────────────────────────────────────────
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"seeker_{uuid.uuid4().hex[:6]}"
if 'results' not in st.session_state:
    st.session_state.results = None
if 'last_mood' not in st.session_state:
    st.session_state.last_mood = ""
if 'last_query_id' not in st.session_state:       # FIX 1: was missing
    st.session_state.last_query_id = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'current_emotion' not in st.session_state:
    st.session_state.current_emotion = "neutral"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
def check_password():
    """Returns True if the user authenticated successfully."""

    def password_entered():
        # FIX 2: Removed plaintext password comment — hash only, no hint in source
        EXPECTED_HASH = "a4559662e367676980b4e7bea677a03ab55de20bb9cd072a4b52f80baccb7f6c"
        hashed_entered = hashlib.sha256(st.session_state["password"].encode()).hexdigest()
        if hashed_entered == EXPECTED_HASH:
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False
            st.error("😕 Sanctuary access denied. Please check your credentials.")

    if not st.session_state["authenticated"]:
        st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
        col_lock_l, col_lock_c, col_lock_r = st.columns([1, 1, 1])
        with col_lock_c:
            st.image("assets/lock_screen.png", use_container_width=True)
        st.markdown('<h1 style="text-align: center; color: #4A675A;">Sanctuary Lock</h1>', unsafe_allow_html=True)
        col_l, col_c, col_r = st.columns([1, 1, 1])
        with col_c:
            st.text_input(
                "Password", type="password", on_change=password_entered, key="password",
                placeholder="Enter key to unlock..."
            )
        return False
    else:
        with st.sidebar:
            if st.button("Secure Logout"):
                st.session_state["authenticated"] = False
                st.rerun()
        return True

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
@st.cache_resource
def load_sanctuary_controller():
    return HybridRecommendationSystem()

def _get_youtube_embed(url: str) -> str:
    """
    FIX 3: st.video() does NOT support YouTube URLs — it expects direct
    media files (.mp4 etc). Extract the video ID and use an iframe embed instead.
    """
    video_id = ""
    if "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
    if not video_id:
        return ""
    return (
        f'<iframe width="100%" height="215" '
        f'src="https://www.youtube.com/embed/{video_id}" '
        f'frameborder="0" allow="accelerometer; autoplay; clipboard-write; '
        f'encrypted-media; gyroscope; picture-in-picture" allowfullscreen '
        f'style="border-radius: 12px;"></iframe>'
    )

def _infer_category(title: str, channel: str) -> str:
    """
    FIX 4: Derive a real category instead of always passing 'yoga'.
    Used by the LinUCB feedback update so the correct arm gets trained.
    """
    text = (title + " " + channel).lower()
    if any(w in text for w in ["meditat", "mindful", "breathe", "breathing"]):
        return "meditation"
    if any(w in text for w in ["exercise", "workout", "fitness", "hiit", "strength"]):
        return "exercise"
    if any(w in text for w in ["read", "story", "book", "journal"]):
        return "reading"
    return "yoga"  # safe default


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
def main():
    # FIX 5: Auth gate FIRST — model only loads after user is authenticated.
    # Previously load_sanctuary_controller() ran at module level, meaning
    # DistilBERT + KeyBERT loaded before the lock screen even appeared.
    if not check_password():
        return

    # FIX 5 (cont): Load system HERE, after auth passes
    system = load_sanctuary_controller()

    from datetime import datetime
    # FIX 6: Define hour here so it's always available for get_recommendations()
    # regardless of code path (avoids potential NameError on refactor)
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # Name Entry State
    if not st.session_state.user_name:
        st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; font-size: 3rem; margin-bottom: 2rem;">Welcome to the Sanctuary.</h1>', unsafe_allow_html=True)
        col_name_l, col_name_c, col_name_r = st.columns([1, 2, 1])
        with col_name_c:
            name_input = st.text_input("Tell us, what is your name?", placeholder="Your name...", key="temp_name")
            if st.button("Begin Your Journey", use_container_width=True):
                if name_input:
                    st.session_state.user_name = name_input
                    st.rerun()
        return

    # Energy Flow Animation
    st.markdown("""
    <style>
        .energy-flow {
            position: relative;
            overflow: hidden;
        }
        .energy-flow::after {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(180deg, 
                rgba(255, 140, 0, 0) 0%, 
                rgba(255, 140, 0, 0.15) 30%, 
                rgba(0, 191, 255, 0.15) 70%, 
                rgba(0, 191, 255, 0) 100%);
            animation: flowDown 4s ease-in-out infinite;
            pointer-events: none;
            mix-blend-mode: soft-light;
        }
        @keyframes flowDown {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
    </style>
    """, unsafe_allow_html=True)

    import base64
    def get_image_base64(path):
        try:
            with open(path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        except:
            return ""

    posters = [
        os.path.join("assets", "yoga_posture_1.png"),
        os.path.join("assets", "yoga_posture_2.png"),
        os.path.join("assets", "surya_namaskar.png"),
        os.path.join("assets", "warrior_pose.png")
    ]
    poster_html = ""
    for p in posters:
        b64 = get_image_base64(p)
        if b64:
            poster_html += f'<div class="energy-flow" style="border-radius: 16px;"><img src="data:image/png;base64,{b64}" class="yoga-image"></div>'

    st.markdown('<h2 style="text-align: left; font-weight: 700; font-size: 2.5rem; color: #4A675A; font-family: \'Playfair Display\', serif; margin-bottom: 1rem;">Welcome Home</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="yoga-image-container">{poster_html}</div>', unsafe_allow_html=True)

    # Hero Section
    st.markdown(f'<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #4A675A; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.8rem; margin-bottom: 1rem;">{greeting}, {st.session_state.user_name}</p>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 4rem; margin-bottom: 1.5rem;">Peace begins here.</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Playfair Display\', serif; font-size: 1.3rem; color: #6D7275; margin: 0 auto 2rem auto;">Describe how you feel, and we will curate a practice to ground your soul.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Inter\', sans-serif; font-style: italic; color: #4A675A; font-size: 1.1rem; margin-bottom: 3rem; background: #F9FAFB; padding: 2rem; border-radius: 16px;">"You cannot pour from an empty cup. This moment is you refilling yours." ✨</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    def clear_sanctuary():
        st.session_state.results = None
        st.session_state.last_query_id = ""  # now safe — key always exists

    # Bio-Context Inputs
    col_input, col_bio = st.columns([2, 1])
    with col_input:
        user_mood = st.text_input(
            "How is your soul today?",
            placeholder="e.g., I feel stressed and need to breathe",
            label_visibility="collapsed"
        )
    with col_bio:
        just_ate = st.checkbox("I just ate 🍲", on_change=clear_sanctuary)

    col_btn_left, col_btn_center, col_btn_right = st.columns([1, 1, 1])
    with col_btn_center:
        find_btn = st.button("Enter the Sanctuary", use_container_width=True)

    if find_btn and user_mood:
        query_id = f"{user_mood}_{just_ate}"
        if st.session_state.get('last_query_id') != query_id:
            with st.empty():
                st.markdown("""
                    <div class="breathing-container">
                        <div class="breathing-circle"></div>
                        <div class="breathing-text">🌿 Designing your sanctuary...</div>
                    </div>
                """, unsafe_allow_html=True)

                # FIX 7: Wrap the entire recommendation fetch in try/except.
                # Previously, any API failure (quota, network, model error) would
                # crash the app with a raw Python traceback visible to the user.
                with st.status("Gathering peace...", expanded=False) as status:
                    try:
                        response = system.get_recommendations(
                            user_input=user_mood,
                            user_id=st.session_state.user_id,
                            just_ate=just_ate,
                            hour=hour,
                            top_n=4
                        )
                        recs = response.get('recommendations', [])

                        # FIX 8: Convert numpy _context arrays to plain Python lists
                        # before storing in session_state. Numpy arrays survive
                        # in-memory fine but fail on serialization in multi-worker
                        # deployments, causing feedback to silently do nothing.
                        for vid in recs:
                            if vid.get('_context') is not None:
                                try:
                                    vid['_context'] = vid['_context'].tolist()
                                except AttributeError:
                                    pass  # already a list or None
                            if vid.get('features') is not None:
                                try:
                                    vid['features'] = vid['features'].tolist()
                                except AttributeError:
                                    pass

                        st.session_state.results = recs
                        st.session_state.current_emotion = response.get('emotion', 'neutral')
                        st.session_state.last_mood = user_mood
                        st.session_state.last_query_id = query_id
                        status.update(label="Sanctuary Ready", state="complete")

                    except Exception as e:
                        status.update(label="Something went wrong", state="error")
                        st.error("🌿 The sanctuary is momentarily unavailable. Please try again in a moment.")
                        st.session_state.results = None
                        st.session_state.last_query_id = ""

                st.empty()
            st.rerun()

    # Results Grid
    if st.session_state.results:
        st.markdown('<div style="margin-top: 5rem; margin-bottom: 3rem; text-align: center;">', unsafe_allow_html=True)
        st.markdown('<h2 style="font-size: 2.2rem;">Curated for you.</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        results = st.session_state.results
        for i in range(0, len(results), 2):
            cols = st.columns(2, gap="large")
            for j in range(2):
                if i + j < len(results):
                    vid = results[i + j]

                    # FIX 4 (cont): Infer real category per video for LinUCB feedback
                    video_category = _infer_category(
                        vid.get('title', ''),
                        vid.get('channel_name', '')
                    )

                    with cols[j]:
                        st.markdown(f"""
                            <div class="video-card">
                                <img src="{vid['thumbnail']}" class="card-thumb">
                                <div class="card-content">
                                    <span class="match-pill">{vid['match_score']}% PERSONAL MATCH</span>
                                    <h3 class="video-title">{vid['title']}</h3>
                                    <p style="color:#6D7275; font-size: 0.9rem;">{vid['channel_name']}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        # FIX 3 (cont): Use iframe embed instead of st.video().
                        # st.video() only supports direct media file URLs (.mp4 etc),
                        # not YouTube watch URLs — those render as broken/blank players.
                        embed_html = _get_youtube_embed(vid['url'])
                        if embed_html:
                            st.markdown(embed_html, unsafe_allow_html=True)
                        else:
                            st.markdown(f'<a href="{vid["url"]}" target="_blank">▶ Watch on YouTube</a>', unsafe_allow_html=True)

                        # Feedback Loop
                        col_stats, col_fb = st.columns([2, 1])
                        with col_stats:
                            st.markdown(f"""
                                <div style="padding: 1rem 0; text-align: left;">
                                    <p style="color: #6D7275; font-size: 0.8rem;">{vid.get('views', 0):,} views • {vid.get('duration_minutes', 0)} mins</p>
                                </div>
                            """, unsafe_allow_html=True)

                        with col_fb:
                            btn_l, btn_r = st.columns(2)
                            with btn_l:
                                if st.button("👍", key=f"up_{vid['video_id']}_{i+j}"):
                                    system.process_feedback(
                                        user_id=st.session_state.user_id,
                                        emotion=st.session_state.current_emotion,
                                        category=video_category,   # FIX 4: was always 'yoga'
                                        video_id=vid['video_id'],
                                        feedback='thumbs_up',
                                        context=vid.get('_context'),
                                        video_features=vid.get('features')
                                    )
                                    st.toast("Match perfected! 🌿")
                            with btn_r:
                                if st.button("👎", key=f"down_{vid['video_id']}_{i+j}"):
                                    system.process_feedback(
                                        user_id=st.session_state.user_id,
                                        emotion=st.session_state.current_emotion,
                                        category=video_category,   # FIX 4: was always 'yoga'
                                        video_id=vid['video_id'],
                                        feedback='thumbs_down',
                                        context=vid.get('_context'),
                                        video_features=vid.get('features')
                                    )
                                    st.toast("Adjusting your sanctuary... 🕊️")

    elif not user_mood and not st.session_state.results:
        st.markdown('<div style="height: 10rem;"></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()