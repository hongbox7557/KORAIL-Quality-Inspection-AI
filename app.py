import streamlit as st
import google.generativeai as genai
import os

# 1. 페이지 설정 (전문가용 시스템 느낌 내기)
st.set_page_config(page_title="품질검사 지원 AI", layout="centered")
st.title("🔍 품질검사 지원 AI 시스템")
st.info("KORAIL 품질검사 규정 및 법령에 근거하여 답변을 생성합니다.")

# 2. 보안 설정 (API 키)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 3. [복사한 지침 넣기] AI Studio와 똑같은 성능을 내는 핵심 부분
SYSTEM_PROMPT = """
(여기에 AI 스튜디오에서 복사한 지침 내용을 그대로 붙여넣으세요)
예: 당신은 품질검사 전문가로서...
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config={
        "temperature": 0.2,  # 품질검사는 정확도가 중요하므로 낮게 설정(0.1~0.3 권장)
        "top_p": 0.95,
    }
)

# 4. 채팅 기록 유지 (이걸 안 하면 질문할 때마다 리셋됩니다)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 5. 채팅 화면 구성 (AI Studio와 가장 흡사한 디자인)
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("검사 항목이나 규정에 대해 물어보세요."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
