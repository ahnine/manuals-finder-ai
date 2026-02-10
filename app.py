import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

# Page Configuration
st.set_page_config(page_title="Manuals Finder AI", layout="wide")

# API Key Setup
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Model နာမည်ကို အလုပ်လုပ်မည့် version အမှန်သို့ ပြောင်းလဲခြင်း
            model = genai.GenerativeModel('gemini-1.5-flash') 
        except Exception as e:
            st.error(f"API Setup Error: {e}")

# Main App UI
st.title("🛠️ Manuals Finder AI")
st.subheader("အင်ဂျင်နီယာသုံး AI လက်ထောက်")

tab1, tab2, tab3 = st.tabs(["🔍 Search Manuals", "💬 AI Chat", "📄 PDF Analyst"])

# Tab 1: Search Logic (App ထဲမှာတင် Google Result မြင်ရအောင် Embed လုပ်နည်း)
with tab1:
    query = st.text_input("Model Number ရိုက်ထည့်ပါ (ဥပမာ- FX3U, FC302)")
    if st.button("Search PDF"):
        if query:
            st.success(f"{query} အတွက် ရှာဖွေမှု ရလဒ်များ -")
            # Google Search ကို App ထဲမှာတင် Frame အနေနဲ့ ပြသခြင်း
            search_url = f"https://www.google.com/search?q={query}+manual+filetype:pdf&igu=1"
            st.markdown(f'<iframe src="{search_url}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)
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
                    # Error 404 ကို ကျော်လွှားရန် generation_config ထည့်သွင်းခြင်း
                    response = model.generate_content(
                        f"Answer in Myanmar language concisely: {prompt}",
                        generation_config=genai.types.GenerationConfig(candidate_count=1)
                    )
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
            text = "".join([page.get_text() for page in doc])
            st.success("PDF ဖတ်လို့ ပြီးပါပြီ!")
            
            question = st.text_input("ဒီ PDF ထဲက ဘာကို သိချင်လဲ?")
            if st.button("Ask PDF"):
                if api_key:
                    # စာသားအရမ်းရှည်လျှင် ဖြတ်တောက်ရန်
                    response = model.generate_content(f"Based on this: {text[:10000]}, answer in Myanmar: {question}")
                    st.write(response.text)
                else:
                    st.error("API Key လိုအပ်ပါသည်")
        except Exception as e:
            st.error(f"Error: {e}")
