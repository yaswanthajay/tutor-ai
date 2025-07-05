import streamlit as st
import requests
import difflib

# ----------------- CONFIG -----------------
client_id = "d4127663132295c8af4c834918ba8457"
client_secret = "fc80b85776bed16836556271e33cd911a497baa3f275b6c6e572eedbdb1f11b2"

languages = {
    "Python": {"language": "python3", "versionIndex": "4"},
    "C": {"language": "c", "versionIndex": "5"},
    "C++": {"language": "cpp", "versionIndex": "5"},
    "Java": {"language": "java", "versionIndex": "4"},
}

# --------------- STREAMLIT UI -----------------
st.set_page_config(page_title="AI Code Tutor + Compiler", layout="centered")

st.title("💡 AI Code Tutor + JDoodle Compiler")
st.markdown("✅ Paste your code → Select Language → Click Compile → Get AI feedback!")

selected_lang = st.selectbox("Select Programming Language", list(languages.keys()))
user_code = st.text_area("📝 Enter Your Code", height=300)

# --------------- AI ERROR CORRECTION -----------------
def simple_correction(code, lang):
    """Basic dummy corrections - you can enhance with ML"""
    if lang == "Python":
        if "pritn" in code:
            return code.replace("pritn", "print")
        if "def main:" in code:
            return code.replace("def main:", "def main():")
    elif lang == "C":
        if "main)" in code and "int main()" not in code:
            return code.replace("main)", "main(void)")
    elif lang == "C++":
        if "include <" not in code:
            return "#include <iostream>\nusing namespace std;\n" + code
    elif lang == "Java":
        if "System.out.println(" not in code:
            return "public class Main {\npublic static void main(String[] args) {\nSystem.out.println(\"Fix Me\");\n}\n}"            
    return code

# --------------- COMPILER CALL -----------------
if st.button("🚀 Compile & Run"):
    if not user_code.strip():
        st.warning("⚠️ Please enter code first.")
    else:
        corrected_code = simple_correction(user_code, selected_lang)
        if corrected_code != user_code:
            st.subheader("🤖 AI Suggestion: Corrected Code")
            st.code(corrected_code, language=selected_lang.lower())
        else:
            st.info("✅ No major errors found. Code looks clean.")

        # Run using JDoodle API
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
            if "output" in result:
                st.subheader("🖥️ Output:")
                st.code(result["output"])
            else:
                st.error("Something went wrong with JDoodle API.")
        except Exception as e:
            st.error(f"JDoodle API Error: {e}")
