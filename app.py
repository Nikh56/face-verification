import streamlit as st
from PIL import Image
import numpy as np

# Set page config first
st.set_page_config(page_title="AI Face Verification", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

from utils.ui import apply_theme, render_badge, render_card_open, render_card_close
from utils.face import get_embedding, compare_embeddings
from utils.storage import load_embeddings, save_embedding, clear_embeddings

# Apply dynamic styling
period, icon = apply_theme()

# Sidebar Navigation
st.sidebar.markdown(f"## {icon} Navigation")
menu = ["Verify Face", "Register Face", "Database"]
choice = st.sidebar.radio("Select Mode", menu)
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")
st.sidebar.success("Backend: Online")
st.sidebar.info(f"Loaded Users: {len(load_embeddings())}")

# Header
st.markdown(f"<h1 style='text-align: center; margin-bottom: 0;'>{icon} Good {period}!</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 2rem;'>Production-Ready Face Verification System</h3>", unsafe_allow_html=True)

# Main App Logic
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if choice == "Register Face":
        render_card_open()
        st.markdown("<h2>👤 Register a New Face</h2>", unsafe_allow_html=True)
        st.markdown("Enroll a new user into the secure database.")
        
        name = st.text_input("Enter User Name:", placeholder="e.g., John Doe")
        capture_method = st.radio("Capture Method", ["Webcam", "File Upload"], horizontal=True)
        
        image_file = None
        if capture_method == "Webcam":
            image_file = st.camera_input("Take a clear picture")
        else:
            image_file = st.file_uploader("Upload a high-quality face image", type=["jpg", "jpeg", "png"])
            
        if st.button("🚀 Register User", use_container_width=True):
            if not name.strip():
                render_badge("⚠️ Please enter a valid name.", "error")
            elif not image_file:
                render_badge("⚠️ Please provide an image.", "error")
            else:
                with st.spinner("Processing facial features..."):
                    img = Image.open(image_file).convert("RGB")
                    img_array = np.array(img)
                    
                    embedding = get_embedding(img_array)
                    if embedding is not None:
                        save_embedding(name.strip(), embedding)
                        render_badge(f"✅ Successfully registered <b>{name}</b>!", "success")
                        st.balloons()
                    else:
                        render_badge("❌ No face detected. Ensure your face is clearly visible and well-lit.", "error")
        render_card_close()

    elif choice == "Verify Face":
        render_card_open()
        st.markdown("<h2>🔐 Verify Identity</h2>", unsafe_allow_html=True)
        st.markdown("Scan your face to access the system.")
        
        capture_method = st.radio("Capture Method", ["Webcam", "File Upload"], horizontal=True)
        
        image_file = None
        if capture_method == "Webcam":
            image_file = st.camera_input("Look at the camera")
        else:
            image_file = st.file_uploader("Upload your photo for verification", type=["jpg", "jpeg", "png"])
            
        if st.button("🔍 Verify Now", use_container_width=True) and image_file:
            with st.spinner("Analyzing biometric data..."):
                img = Image.open(image_file).convert("RGB")
                img_array = np.array(img)
                
                target_embedding = get_embedding(img_array)
                
                if target_embedding is not None:
                    stored_embeddings = load_embeddings()
                    match_name, confidence = compare_embeddings(target_embedding, stored_embeddings)
                    
                    if match_name:
                        render_badge(f"🔓 Access Granted! Welcome back, {match_name}.", "success")
                        st.markdown(f"<h4 style='text-align: center;'>Match Confidence: <span class='accent-text'>{confidence:.2f}%</span></h4>", unsafe_allow_html=True)
                    else:
                        render_badge("🔒 Access Denied. Face not recognized.", "error")
                else:
                    render_badge("❌ No face detected. Please ensure your face is clearly visible.", "error")
        render_card_close()

    elif choice == "Database":
        render_card_open()
        st.markdown("<h2>🗃️ Registered Users</h2>", unsafe_allow_html=True)
        
        stored_embeddings = load_embeddings()
        if stored_embeddings:
            st.markdown(f"<p>Total active users in system: <span class='accent-text'>{len(stored_embeddings)}</span></p>", unsafe_allow_html=True)
            
            # Display users in a nice layout
            for idx, user in enumerate(stored_embeddings.keys()):
                st.markdown(f"<div style='padding: 10px; margin: 5px 0; border-radius: 8px; background: rgba(0,0,0,0.1);'><b>{idx+1}.</b> {user}</div>", unsafe_allow_html=True)
                
            st.markdown("---")
            if st.button("🗑️ Clear Database", use_container_width=True):
                clear_embeddings()
                # Use st.rerun() if available, otherwise rely on the page reloading by user interacting again
                if hasattr(st, 'rerun'):
                    st.rerun()
                elif hasattr(st, 'experimental_rerun'):
                    st.experimental_rerun()
        else:
            st.info("No users registered yet. Go to 'Register Face' to add users.")
        render_card_close()
