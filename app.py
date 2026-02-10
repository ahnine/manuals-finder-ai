import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# Page Configuration
st.set_page_config(page_title="Manuals Finder AI", layout="centered")

# CSS for Burmese Font & Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pyidaungsu&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Pyidaungsu', sans-serif;
    }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# API Key Setup
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Gemini-Pro ကို သုံးထားပေးတယ် (ပိုငြိမ်အောင်လို့)
            model = genai.GenerativeModel('gemini-pro') 
        except Exception as e:
            st.error(f"API Setup Error: {e}")

# Main App UI
st.title("🛠️ Manuals Finder AI")
st.subheader("အင်ဂျင်နီယာသုံး AI လက်ထောက်")

tab1, tab2, tab3 = st.tabs(["🔍 Search Manuals", "💬 AI Chat", "📄 PDF Analyst"])

# Tab 1: Search Logic (Direct Google Link နည်းလမ်း)
with tab1:
    query = st.text_input("Model Number ရိုက်ထည့်ပါ (ဥပမာ- FX3U, S7-1200)")
    if st.button("Search PDF"):
        if query:
            search_url = f"https://www.google.com/search?q={query}+manual+filetype:pdf"
            st.success(f"ရှာဖွေမှု အဆင်သင့်ဖြစ်ပါပြီ!")
            st.markdown(f"### 👉 [ဒီနေရာကိုနှိပ်ပြီး {query} Manual ကို ကြည့်ပါ]({search_url})")
        else:
            st.warning("Model Number အရင်ရိုက်ပါ")

# Tab 2: AI Chat
with tab2:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("မေးခွန်းမေးမြန်းနိုင်ပါသည်..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if api_key:
                try:
                    response = model.generate_content(f"Answer in Myanmar language: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"AI Error: {e}")
            else:
                st.error("Sidebar မှာ API Key အရင်ထည့်ပေးပါ")

# Tab 3: PDF Analyst
with tab3:
    uploaded_file = st.file_uploader("Manual PDF ကို ဒီမှာ တင်ပါ", type="pdf")
    if uploaded_file is not None:
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            
            st.success("PDF ဖတ်လို့ ပြီးပါပြီ!")
            question = st.text_input("ဒီ PDF ထဲက ဘာကို သိချင်လဲ?")
            if st.button("Ask PDF"):
                full_prompt = f"Using this text: {text[:8000]}, answer this in Myanmar: {question}"
                response = model.generate_content(full_prompt)
                st.write(response.text)
        except Exception as e:
            st.error(f"PDF Error: {e}")
