import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
from googlesearch import search

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
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # Flash သုံးရင် ပိုမြန်တယ်

# Main App UI
st.title("🛠️ Manuals Finder AI")
st.subheader("အင်ဂျင်နီယာသုံး AI လက်ထောက်")

tab1, tab2, tab3 = st.tabs(["🔍 Search Manuals", "💬 AI Chat", "📄 PDF Analyst"])

# Tab 1: Search Logic
with tab1:
    query = st.text_input("Model Number ရိုက်ထည့်ပါ (ဥပမာ- FX3U, S7-1200)")
    if st.button("Search PDF"):
        if query:
            with st.spinner("အင်တာနက်မှ ရှာဖွေနေပါသည်..."):
                results = list(search(f"{query} manual filetype:pdf", num_results=5))
                for url in results:
                    st.write(f"📄 [Download Manual]({url})")
        else:
            st.warning("Model Number အရင်ရိုက်ပါ")

# Tab 2: AI Chat (NotebookLM Style အနီးစပ်ဆုံး)
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
                response = model.generate_content(f"Answer in Myanmar language: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Sidebar မှာ API Key အရင်ထည့်ပေးပါ")

# Tab 3: PDF Analyst (NotebookLM လိုမျိုး PDF ဖတ်ခိုင်းခြင်း)
with tab3:
    uploaded_file = st.file_uploader("Manual PDF ကို ဒီမှာ တင်ပါ", type="pdf")
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        st.success("PDF ဖတ်လို့ ပြီးပါပြီ!")
        question = st.text_input("ဒီ PDF ထဲက ဘာကို အနှစ်ချုပ်ပေးရမလဲ?")
        if st.button("Ask PDF"):
            full_prompt = f"Based on this PDF text: {text[:10000]}... Answer this in Myanmar: {question}"
            response = model.generate_content(full_prompt)
            st.write(response.text)
