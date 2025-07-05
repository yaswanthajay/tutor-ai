import streamlit as st
import requests
from gtts import gTTS
import uuid
import base64
import os

# === JDoodle API credentials ===
client_id = "d4127663132295c8af4c834918ba8457"
client_secret = "fc80b85776bed16836556271e33cd911a497baa3f275b6c6e572eedbdb1f11b2"

languages = {
    "Python": {"language": "python3", "versionIndex": "4"},
    "C": {"language": "c", "versionIndex": "5"},
    "C++": {"language": "cpp", "versionIndex": "5"},
    "Java": {"language": "java", "versionIndex": "4"},
}

# === Helper: Simple Correction Logic ===
def simple_correction(code, lang):
    if lang == "Python":
        if "pritn" in code:
            return code.replace("pritn", "print"), "Replaced 'pritn' with 'print'"
    elif lang == "C":
        if "main)" in code and "int main()" not in code:
            return code.replace("main)", "main(void)"), "Fixed function declaration"
    elif lang == "C++":
        if "#include" not in code:
            return "#include <iostream>\nusing namespace std;\n" + code, "Added C++ header"
    elif lang == "Java":
        if "System.out.println(" not in code:
            boiler = """public class Main {
    public static void main(String[] args) {
        System.out.println("Fix Me");
    }
}"""
            return boiler, "Added missing Java main class"
    return code, ""

# === Helper: Text-to-Speech ===
def text_to_speech(text):
    filename = f"voice_{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def render_audio(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# === Streamlit UI ===
st.set_page_config(page_title="AI Code Tutor + Voice", layout="centered")
st.title(" AI Code Tutor + JDoodle Compiler")

selected_lang = st.selectbox("Choose Language", list(languages.keys()))
user_code = st.text_area("Write Your Code", height=300)

if st.button(" Compile & Run"):
    if not user_code.strip():
        st.warning("⚠️ Please enter some code.")
    else:
        corrected_code, ai_tip = simple_correction(user_code, selected_lang)

        if corrected_code != user_code:
            st.subheader("AI Correction Applied:")
            st.code(corrected_code, language=selected_lang.lower())
            if ai_tip:
                st.info(f"💬 {ai_tip}")
                file_path = text_to_speech(ai_tip)
                render_audio(file_path)
        else:
            st.success("No basic syntax issues detected.")

        payload = {
            "clientId": client_id,
            "clientSecret": client_secret,
            "script": corrected_code,
            "language": languages[selected_lang]["language"],
            "versionIndex": languages[selected_lang]["versionIndex"]
        }

        try:
            res = requests.post("https://api.jdoodle.com/v1/execute", json=payload)
            result = res.json()
            st.subheader("Output:")
            st.code(result.get("output", "No output."))
        except Exception as e:
            st.error(f"JDoodle API Error: {e}")
