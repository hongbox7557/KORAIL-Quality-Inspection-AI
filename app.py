import streamlit as st
import google.generativeai as genai
import os

# 보안 금고(Secrets)에서 API 키를 가져오는 코드입니다.
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    st.title("💡 나만의 스마트 AI")

    # 입력창 만들기
    user_input = st.text_input("질문을 입력하고 엔터를 치세요!")

    if user_input:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_input)
        st.write("---")
        st.write(response.text)
else:
    st.error("API 키 설정이 필요합니다!")
