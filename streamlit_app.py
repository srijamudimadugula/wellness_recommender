

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
    /* Typography Imports */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Overrides */
    .stApp {
        background-color: #FFFFFF;
        color: #2F3437;
    }
    
    /* Center Layout (1000px Max) */
    .main .block-container {
        max-width: 1000px;
        padding-top: 3rem;
        margin: auto;
    }

    /* Headings & Body */
    h1, h2, h3, .playfair {
        font-family: 'Playfair Display', serif !important;
        color: #1A1C1D !important;
        font-weight: 700 !important;
    }
    
    p, span, div, label, .inter {
        font-family: 'Inter', sans-serif !important;
        color: #4A4E51 !important;
    }

    /* Posture Images Gallery */
    .yoga-image-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 3rem;
        position: relative; /* Added for absolute positioning of title */
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

    /* Input Styling - Minimalist & Rounded */
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
    
    /* Hide Default Red Borders on Error/Focus */
    [data-baseweb="input"] {
        border-color: transparent !important;
    }

    /* Button Styling */
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

    /* Video Cards with Refined Hover Lift (User Request: -5px) */
    /* Card Entrance Animation */
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

    /* Breathing Bubble Animation (Enhanced) */
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

    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    .stDeployButton {display:none;}
    
    /* Expander Styling - Floating Effect */
    .stExpander {
        border: none !important;
        background: #F9FAFB !important;
        border-radius: 12px !important;
        margin-top: 1rem !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
    }

    /* Feedback Buttons */
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

# SESSION STATE & SYSTEM

if 'user_id' not in st.session_state:
    st.session_state.user_id = f"seeker_{uuid.uuid4().hex[:6]}"
if 'results' not in st.session_state:
    st.session_state.results = None
if 'last_mood' not in st.session_state:
    st.session_state.last_mood = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'current_emotion' not in st.session_state:
    st.session_state.current_emotion = "neutral"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # The password for development is 'wellness2026'
        # Hashed value of 'wellness2026' using SHA-256
        EXPECTED_HASH = "a4559662e367676980b4e7bea677a03ab55de20bb9cd072a4b52f80baccb7f6c"
        
        entered_password = st.session_state["password"]
        hashed_entered = hashlib.sha256(entered_password.encode()).hexdigest()
        
        if hashed_entered == EXPECTED_HASH:
            st.session_state["authenticated"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["authenticated"] = False
            st.error("😕 Sanctuary access denied. Please check your credentials.")

    if not st.session_state["authenticated"]:
        # First-time user: Enter password
        st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
        
        # Lock Screen Image
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
            st.markdown('<p style="font-size: 0.7rem; text-align: center; color: #6D7275;">Default Key: <code>wellness2026</code></p>', unsafe_allow_html=True)
        return False
    else:
        # Password correct: show the "Log Out" button in the sidebar
        with st.sidebar:
            if st.button("Secure Logout"):
                st.session_state["authenticated"] = False
                st.rerun()
        return True

@st.cache_resource
def load_sanctuary_controller():
    return HybridRecommendationSystem()

system = load_sanctuary_controller()


# MAIN UI

def main():
    # 0. Security Gate
    if not check_password():
        return

    # Dynamic Sanctuary Greeting
    from datetime import datetime
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

    # Energy Flow Animation Styling
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

    # Yoga Postures integration
    import base64
    def get_image_base64(path):
        try:
            with open(path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        except: return ""

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

       # Welcome Home title above the container
    st.markdown('<h2 style="text-align: left; font-weight: 700; font-size: 2.5rem; color: #4A675A; font-family: \'Playfair Display\', serif; margin-bottom: 1rem;">Welcome Home</h2>', unsafe_allow_html=True)

    st.markdown(f'''
        <div class="yoga-image-container">
            {poster_html}
        </div>
    ''', unsafe_allow_html=True)

    # Hero Section
    st.markdown(f'<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #4A675A; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.8rem; margin-bottom: 1rem;">{greeting}, {st.session_state.user_name}</p>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 4rem; margin-bottom: 1.5rem;">Peace begins here.</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Playfair Display\', serif; font-size: 1.3rem; color: #6D7275; margin: 0 auto 2rem auto;">Describe how you feel, and we will curate a practice to ground your soul.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: \'Inter\', sans-serif; font-style: italic; color: #4A675A; font-size: 1.1rem; margin-bottom: 3rem; background: #F9FAFB; padding: 2rem; border-radius: 16px;">"You cannot pour from an empty cup. This moment is you refilling yours." ✨</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Reset Logic: Clear results if biometric context changes
    def clear_sanctuary():
        st.session_state.results = None
        st.session_state.last_query_id = ""

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

    # Logic: Stateful Search "Lock"
    if find_btn and user_mood:
        # Only search if context changed or results are empty
        query_id = f"{user_mood}_{just_ate}"
        if "results" not in st.session_state or st.session_state.get('last_query_id') != query_id:
            # Show Breathing Bubble Loader
            with st.empty():
                st.markdown("""
                    <div class="breathing-container">
                        <div class="breathing-circle"></div>
                        <div class="breathing-text">🌿 Designing your sanctuary...</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Fetch data using the Hybrid Controller
                with st.status("Gathering peace...", expanded=False) as status:
                    response = system.get_recommendations(
                        user_input=user_mood,
                        user_id=st.session_state.user_id,
                        just_ate=just_ate,
                        hour=hour,
                        top_n=4
                    )
                    st.session_state.results = response.get('recommendations', [])
                    st.session_state.current_emotion = response.get('emotion', 'neutral')
                    st.session_state.last_mood = user_mood
                    st.session_state.last_query_id = query_id
                    status.update(label="Sanctuary Ready", state="complete")
                
                st.empty() # Clear the breathing bubble
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
                    vid = results[i+j]
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
                        
                        st.video(vid['url'])
                        
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
                                        category='yoga',
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
                                        category='yoga',
                                        video_id=vid['video_id'],
                                        feedback='thumbs_down',
                                        context=vid.get('_context'),
                                        video_features=vid.get('features')
                                    )
                                    st.toast("Adjusting your sanctuary... 🕊️")

    # Empty State
    elif not user_mood and not st.session_state.results:
        st.markdown('<div style="height: 10rem;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
