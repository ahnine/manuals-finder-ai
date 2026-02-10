import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Engineer AI", page_icon="⚡")

with st.sidebar:
    st.title("⚙️ Setup")
    api_key = st.text_input("Enter API Key", type="password")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # ဒီနေရာမှာ gemini-pro ကိုပဲ သုံးပါမယ် (404 Error ကင်းစေရန်)
            model = genai.GenerativeModel('gemini-pro')
            st.success("Ready!")
        except Exception as e:
            st.error(f"Error: {e}")

st.title("⚡ Specialist Electrical Engineer")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("မေးခွန်းမေးပါ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if api_key:
            try:
                # အင်ဂျင်နီယာအဖြစ် သတ်မှတ်ရန် instruction ကို ဒီမှာ ထည့်လိုက်ပါသည်
                response = model.generate_content(f"Answer as an Electrical Engineer in Myanmar: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
        else:
            st.error("Please enter API Key in sidebar")
