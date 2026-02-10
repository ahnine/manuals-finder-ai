import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Electrical Expert AI", page_icon="⚡")

# Sidebar for API Key
with st.sidebar:
    st.title("⚡ Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Engineer တစ်ယောက်လို ပြုမူရန် Instruction ပေးခြင်း
            model = genai.GenerativeModel(
                model_name="models/gemini-1.5-flash",
                system_instruction="မင်းက အတွေ့အကြုံရင့်ကျက်တဲ့ Electrical Engineer တစ်ယောက်ဖြစ်တယ်။ မင်းကို မေးသမျှ မေးခွန်းတွေကို နည်းပညာပိုင်းဆိုင်ရာ သေချာကျနစွာနဲ့ မြန်မာဘာသာစကားဖြင့်သာ ရှင်းပြရမယ်။ အထူးသဖြင့် Wiring, PLC, Industrial Control နဲ့ Electrical Safety ပိုင်းတွေကို ကျွမ်းကျင်စွာ ဖြေပေးရမယ်။"
            )
            st.success("Engineer AI is Ready!")
        except Exception as e:
            st.error(f"Setup Error: {e}")

# Main UI
st.title("⚡ Pro Electrical Engineer AI")
st.write("ကျွန်တော်ကတော့ ကိုနှိုင်းရဲ့ Electrical ပိုင်းဆိုင်ရာ လက်ထောက်အင်ဂျင်နီယာ ဖြစ်ပါတယ်။")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("အင်ဂျင်နီယာကို မေးခွန်းမေးပါ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if api_key:
            try:
                # Chat response
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # 404 error ဖြစ်ရင် model နာမည်ကို models/gemini-1.5-flash လို့ အစားထိုးစမ်းကြည့်ပါ
                st.error(f"Error: {e}. (Hint: အကယ်၍ 404 ဖြစ်ပါက API Key အသစ် သို့မဟုတ် Model Name စစ်ဆေးပါ)")
        else:
            st.error("Sidebar မှာ API Key အရင်ထည့်ပေးပါဗျာ။")
