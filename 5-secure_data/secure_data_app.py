import streamlit as st
import hashlib
from cryptography.fernet import Fernet, InvalidToken

# Set page configuration
st.set_page_config(page_title="🔐 Secure Data System", layout="centered")

# Generate a symmetric encryption key (only once per session)
if "fernet_key" not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.fernet_key)

# Initialize session state for failed attempts and stored data
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}  # {encrypted_text: {"encrypted_text": ..., "passkey": hashed_passkey}}

# Hashing function
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt text
def encrypt_data(text):
    return st.session_state.cipher.encrypt(text.encode()).decode()

# Decrypt text with validation and error handling
def decrypt_data(encrypted_text, passkey):
    try:
        hashed = hash_passkey(passkey)

        if encrypted_text in st.session_state.stored_data:
            stored_entry = st.session_state.stored_data[encrypted_text]
            if stored_entry["passkey"] == hashed:
                st.session_state.failed_attempts = 0
                decrypted = st.session_state.cipher.decrypt(encrypted_text.encode()).decode()
                return decrypted
            else:
                raise ValueError("Incorrect passkey")
        else:
            raise KeyError("Data not found")

    except (InvalidToken, ValueError, KeyError):
        st.session_state.failed_attempts += 1
        return None

# Reset attempts
def reset_attempts():
    st.session_state.failed_attempts = 0

# UI Layout
st.title("🛡️ Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    st.subheader("🏠 Welcome!")
    st.markdown("Use this app to **securely store and retrieve data** using a unique passkey.")
    st.markdown("Encryption is handled using **Fernet** (symmetric encryption).")

elif choice == "Store Data":
    st.subheader("📥 Store Your Data")
    user_input = st.text_area("Enter the text to encrypt:")
    passkey = st.text_input("Enter a passkey:", type="password")

    if st.button("Encrypt & Store"):
        if user_input.strip() and passkey.strip():
            encrypted = encrypt_data(user_input.strip())
            hashed = hash_passkey(passkey.strip())
            st.session_state.stored_data[encrypted] = {
                "encrypted_text": encrypted,
                "passkey": hashed
            }
            st.success("✅ Data encrypted and stored securely!")
            st.code(encrypted, language="text")
        else:
            st.error("❗ Please provide both the text and the passkey.")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_input = st.text_area("Paste your encrypted data:")
    passkey = st.text_input("Enter your passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input.strip() and passkey.strip():
            result = decrypt_data(encrypted_input.strip(), passkey.strip())
            if result:
                st.success("✅ Decrypted successfully!")
                st.code(result, language="text")
            else:
                attempts_left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey or data! Attempts left: {attempts_left}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts! Redirecting to login...")
                    st.experimental_rerun()
        else:
            st.error("❗ Both encrypted data and passkey are required.")

elif choice == "Login":
    st.subheader("🔐 Reauthorization Required")
    password = st.text_input("Enter master password:", type="password")

    if st.button("Login"):
        if password == "Haseeb":  # Change this in production
            reset_attempts()
            st.success("✅ Reauthorized successfully!")
            st.info("You can now go back to 'Retrieve Data' tab.")
        else:
            st.error("❌ Incorrect master password.")
