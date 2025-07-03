import streamlit as st
from difflib import unified_diff
import re

st.set_page_config(page_title="Multi-Language Code Tutor", layout="wide")
st.title("👨‍💻 AI Code Correction Tutor (C, C++, Java, Python)")

language = st.selectbox("Select Programming Language", ["Python", "C", "C++", "Java"])
user_code = st.text_area("🔤 Paste your code here", height=200)

# Placeholder rule-based correction function
def correct_code(code, lang):
    if lang == "Python":
        corrected = re.sub(r"print (.+)", r"print(\1)", code)
        corrected = re.sub(r"def (\w+)\((.*)\):", r"def \1(\2):", corrected)
    elif lang == "C":
        corrected = "#include <stdio.h>\n\n" + code
        corrected = corrected.replace("main()", "int main()")
        if "return" not in corrected:
            corrected += "\nreturn 0;"
    elif lang == "C++":
        corrected = "#include <iostream>\nusing namespace std;\n\n" + code
        corrected = corrected.replace("main()", "int main()")
        if "return" not in corrected:
            corrected += "\nreturn 0;"
    elif lang == "Java":
        corrected = (
            "public class Main {\npublic static void main(String[] args) {\n" +
            code + "\n}\n}"
        )
    else:
        corrected = code
    return corrected

if st.button("✅ Show Corrected Code"):
    if not user_code.strip():
        st.warning("Please enter some code.")
    else:
        corrected_code = correct_code(user_code, language)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📥 Your Code")
            st.code(user_code, language.lower())

        with col2:
            st.subheader("✅ Corrected Code")
            st.code(corrected_code, language.lower())

        # Show diff
        diff = unified_diff(
            user_code.strip().splitlines(),
            corrected_code.strip().splitlines(),
            fromfile="Your Code",
            tofile="Corrected Code",
            lineterm=""
        )
        st.subheader("🔍 Difference")
        st.code("\n".join(diff))
