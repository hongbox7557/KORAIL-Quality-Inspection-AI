import streamlit as st
import google.generativeai as genai

# 1. 화면 설정
st.set_page_config(page_title="품질검사 지원 AI", page_icon="🔍")
st.title("🔍 품질검사 지원 AI 시스템")
st.markdown("---")

# 2. API 키 설정 (보안을 위해 배포 환경의 Secrets 사용)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("설정에서 GOOGLE_API_KEY를 입력해주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 대화 내용 기억하기 (세션 상태)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 화면에 이전 대화 보여주기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력창 및 답변 생성
if prompt := st.chat_input("품질검사 관련 질문을 입력하세요..."):
    # 내가 보낸 메시지
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI의 답변
    with st.chat_message("assistant"):
        with st.spinner("규정을 확인하는 중..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
