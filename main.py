import streamlit as st
import re
import random
import string

# Function to set background image for both main content and sidebar
def set_bg():
    st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1547623641-d2c56c03e2a7?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDd8fGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Apply background to sidebar */
    [data-testid="stSidebar"] {
        background-image: url("https://images.unsplash.com/photo-1547623641-d2c56c03e2a7?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDd8fGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D");
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Apply the background image
set_bg()

# Password Strength Checker Function
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make your password at least 8 characters long.")

    if any(char.islower() for char in password) and any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add at least one digit (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    if score <= 2:
        strength = "🔴 Weak"
    elif score <= 4:
        strength = "🟠 Moderate"
    else:
        strength = "🟢 Strong"

    return strength, score, feedback

# Password Generator Function
def generate_password(length, use_special, use_digits, exclude_similar):
    letters = string.ascii_letters
    digits = string.digits if not exclude_similar else "123456789"
    special_chars = "!@#$%^&*"

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

# Sidebar Navigation
st.sidebar.title("🔒 Password Manager")
option = st.sidebar.radio("Select an option:", ["Check Password Strength", "Generate Strong Password"])

if option == "Check Password Strength":
    st.title("🔑 Password Strength Checker")

    password = st.text_input("Enter your password:", type="password")

    if st.button("Check Strength"):
        if password:
            strength, score, feedback = check_password_strength(password)

            st.subheader(f"Password Strength: {strength}")
            st.progress(score / 5)

            if strength == "🔴 Weak":
                st.warning("Your password is weak. Improve it by following these suggestions:")
            elif strength == "🟠 Moderate":
                st.info("Your password is moderate. Improve it by following these suggestions:")

            for tip in feedback:
                st.write(f"- {tip}")

            if strength == "🟢 Strong":
                st.success("Your password is strong! Well done. ✅")
        else:
            st.error("Please enter a password.")

elif option == "Generate Strong Password":
    st.title("🔐 Password Generator")
    st.markdown("### Customize Your Password 🔧")

    length = st.slider("🔢 Password Length", min_value=8, max_value=24, value=12)
    use_digits = st.checkbox("🔢 Include Digits (1-9)", value=True)
    use_special = st.checkbox("🔠 Include Special Characters (!@#$%^&*)", value=True)
    exclude_similar = st.checkbox("🚫 Exclude Similar Characters (O, I, l, B, S, 0)", value=True)

    if st.button("Generate Password"):
        password = generate_password(length, use_special, use_digits, exclude_similar)
        st.session_state["password"] = password

    if "password" in st.session_state:
        show_password = st.checkbox("👀 Show Password")

        with st.container():
            if show_password:
                st.markdown(f"<div style='padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #f9f9f9; text-align: center;'>"
                            f"<span style='font-weight:bold; font-size:24px; color:#333;'>{st.session_state['password']}</span>"
                            "</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #f9f9f9; text-align: center;'>"
                            "<span style='font-weight:bold; font-size:24px; color:#333;'>••••••••••••</span>"
                            "</div>", unsafe_allow_html=True)

        strength, score, feedback = check_password_strength(st.session_state["password"])
        st.progress(score / 5)
        st.markdown(f"<p style='font-size: 18px;'>{strength} Password</p>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Built with ❤️ by Khansa</p>", unsafe_allow_html=True)
