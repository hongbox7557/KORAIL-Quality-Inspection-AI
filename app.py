import streamlit as st
import google.generativeai as genai
import os

# 1. 사이드바에서 상태 확인
with st.sidebar:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        st.success("✅ API 키 연결됨")
    else:
        st.error("❌ API 키 미연결 (Secrets 확인 필요)")

# 2. 간단한 테스트 버튼
st.title("연결 테스트")
if st.button("AI 응답 테스트"):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("안녕? 연결 확인용이야.")
        st.write("AI 응답:", response.text)
    except Exception as e:
        st.error(f"에러 발생: {e}")
