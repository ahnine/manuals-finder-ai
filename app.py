import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
from googlesearch import search

# Page Configuration
st.set_page_config(page_title="Manuals Finder AI", layout="centered")

# API Key Setup
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # 404 Error ရှင်းရန် gemini-1.5-flash ကို သုံးထားသည်
            model = genai.GenerativeModel('gemini-1.5-flash') 
        except Exception as e:
            st.error(f"API Setup Error: {e}")

# Main App UI
st.title("🛠️ Manuals Finder AI")
st.subheader("အင်ဂျင်နီယာသုံး AI လက်ထောက်")

tab1, tab2, tab3 = st.tabs(["🔍 Search Manuals", "💬 AI Chat", "📄 PDF Analyst"])

# Tab 1: Search Logic (App ထဲမှာတင် PDF Link များ ပြပေးရန်)
with tab1:
    query = st.text_input("Model Number ရိုက်ထည့်ပါ (ဥပမာ- FX3U, Danfoss FC302)")
    if st.button("Search PDF"):
        if query:
            with st.spinner("အင်တာနက်မှ PDF များကို ရှာဖွေနေပါသည်..."):
                try:
                    # Google Search ကို App ထဲမှာတင် Result ထုတ်ပေးရန်
                    search_results = search(f"{query} manual filetype:pdf", num_results=10)
                    
                    st.success(f"{query} အတွက် တွေ့ရှိသော PDF များ -")
                    for idx, url in enumerate(search_results, 1):
                        # Link များကို App ထဲမှာတင် တန်းပြပေးခြင်း
                        st.markdown(f"{idx}. 📄 [Manual Link {idx}]({url})")
                        st.caption(f"Source: {url[:60]}...")
                except Exception as e:
                    st.error(f"Search Error: {e}")
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
                    st.error(f"AI Error: {e}") # 404 models error ရှင်းရန် gemini-1.5-flash သုံးထားပါသည်
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
