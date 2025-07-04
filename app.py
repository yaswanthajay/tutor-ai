import streamlit as st
import requests

# Title
st.title("🧠 AI Code Tutor + JDoodle Online Compiler")
st.markdown("Write code, select language, and click Compile to see output instantly!")

# JDoodle credentials (replace with your real credentials)
client_id = "d4127663132295c8af4c834918ba8457"
client_secret = "fc80b85776bed16836556271e33cd911a497baa3f275b6c6e572eedbdb1f11b2"

# Supported languages and JDoodle language codes
languages = {
    "Python": {"language": "python3", "versionIndex": "4"},
    "C": {"language": "c", "versionIndex": "5"},
    "C++": {"language": "cpp", "versionIndex": "5"},
    "Java": {"language": "java", "versionIndex": "4"},
}

# Select language
selected_lang = st.selectbox("Select Language", list(languages.keys()))

# Text area for code
user_code = st.text_area("✍️ Enter your code below:", height=300)

# Compile button
if st.button("🚀 Compile & Run"):
    if not user_code.strip():
        st.warning("Please enter some code to compile.")
    else:
        # Build request
        payload = {
            "clientId": client_id,
            "clientSecret": client_secret,
            "script": user_code,
            "language": languages[selected_lang]["language"],
            "versionIndex": languages[selected_lang]["versionIndex"]
        }

        try:
            # Send request to JDoodle
            res = requests.post("https://api.jdoodle.com/v1/execute", json=payload)
            result = res.json()

            # Show result
            if "output" in result:
                st.subheader("🖥️ Output:")
                st.code(result["output"])
            else:
                st.error("Something went wrong. Check API credentials or JDoodle limits.")
        except Exception as e:
            st.error(f"Error calling JDoodle: {e}")
