import streamlit as st
import datetime

def get_time_context():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Morning", "🌅", "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)", "#2c3e50", "#3498db"
    elif 12 <= current_hour < 17:
        return "Afternoon", "☀️", "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)", "#1a1a1a", "#667eea"
    elif 17 <= current_hour < 21:
        return "Evening", "🌇", "linear-gradient(135deg, #f6d365 0%, #fda085 100%)", "#333333", "#d35400"
    else:
        return "Night", "🌙", "linear-gradient(135deg, #141e30 0%, #243b55 100%)", "#ffffff", "#4facfe"

def apply_theme():
    period, icon, bg_grad, text_color, accent_color = get_time_context()
    
    # Check if text_color is dark or light to adjust container backgrounds
    is_dark_text = text_color in ["#2c3e50", "#1a1a1a", "#333333"]
    container_bg = "rgba(255, 255, 255, 0.6)" if is_dark_text else "rgba(0, 0, 0, 0.4)"
    
    css = f"""
    <style>
    .stApp {{
        background: {bg_grad} !important;
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp, .stApp p, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label {{
        color: {text_color} !important;
    }}

    .stTextInput > div > div > input {{
        background-color: {container_bg} !important;
        color: {text_color} !important;
        border-radius: 10px;
        border: 1px solid {accent_color};
    }}
    
    .badge-success {{
        background-color: rgba(40, 167, 69, 0.9);
        color: white !important;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
        animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }}
    
    .badge-error {{
        background-color: rgba(220, 53, 69, 0.9);
        color: white !important;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
        animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }}
    
    .accent-text {{
        color: {accent_color} !important;
        font-weight: 800;
        font-size: 1.2em;
    }}
    
    .card {{
        background-color: {container_bg};
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.3);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }}
    
    .card:hover {{
        transform: translateY(-5px);
    }}

    @keyframes popIn {{
        0% {{ transform: scale(0.5); opacity: 0; }}
        70% {{ transform: scale(1.05); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    return period, icon

def render_badge(text, status="success"):
    css_class = "badge-success" if status == "success" else "badge-error"
    st.markdown(f'<div style="text-align: center; margin: 1rem 0;"><div class="{css_class}">{text}</div></div>', unsafe_allow_html=True)

def render_card_open():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
def render_card_close():
    st.markdown('</div>', unsafe_allow_html=True)
