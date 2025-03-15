import streamlit as st
import random
import string
import pyperclip

def generate_password(length, use_special, use_digits, exclude_similar):
    letters = string.ascii_letters
    digits = string.digits if not exclude_similar else "123456789"
    special_chars = "!@#$%^&*"  # Limiting to commonly used special characters

    if exclude_similar:
        letters = letters.replace("O", "").replace("I", "").replace("l", "").replace("B", "").replace("S", "")

    characters = letters
    if use_digits:
        characters += digits
    if use_special:
        characters += special_chars

    password = [random.choice(characters)]
    for _ in range(length - 1):
        next_char = random.choice(characters)
        while next_char == password[-1]:  # Prevent consecutive repetition
            next_char = random.choice(characters)
        password.append(next_char)

    return ''.join(password)

def check_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*" for c in password)

    if length >= 16 and has_upper and has_lower and has_digit and has_special:
        return "🟢 Very Strong", "green", 100
    elif length >= 12 and has_upper and has_lower and (has_digit or has_special):
        return "🟡 Strong", "orange", 80
    elif length >= 8 and (has_upper or has_lower) and (has_digit or has_special):
        return "🟠 Medium", "yellow", 60
    else:
        return "🔴 Weak", "red", 30

# Streamlit UI
st.title("🔐 Password Generator")
st.markdown("### Customize Your Password 🔧")

length = st.slider("🔢 Password Length", min_value=6, max_value=24, value=12)
use_digits = st.checkbox("🔢 Include Digits (1-9)", value=True)
use_special = st.checkbox("🔠 Include Special Characters (!@#$%^&*)", value=True)
exclude_similar = st.checkbox("🚫 Exclude Similar Characters (O, I, l, B, S, 0)", value=True)

if st.button("Generate Password"):
    password = generate_password(length, use_special, use_digits, exclude_similar)
    st.session_state["password"] = password  # Store password in session state

if "password" in st.session_state:
    show_password = st.checkbox("👀 Show Password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        if show_password:
            st.markdown(f"<div style='padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #f9f9f9; text-align: center;'>"
                        f"<span style='font-weight:bold; font-size:24px; color:#333;'>{st.session_state['password']}</span>"
                        "</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #f9f9f9; text-align: center;'>"
                        "<span style='font-weight:bold; font-size:24px; color:#333;'>••••••••••••</span>"
                        "</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📋 Copy to Clipboard"):
        pyperclip.copy(st.session_state["password"])
        st.success("Password copied to clipboard!")

    strength, color, progress = check_strength(st.session_state["password"])
    st.progress(progress)
    st.markdown(f"<p style='color: {color}; font-size: 18px;'>{strength} Password</p>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Built with ❤️ by Khansa</p>", unsafe_allow_html=True)
