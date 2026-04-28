import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="품질검사 지원 AI", layout="wide")

# 1. API 키 로드 및 안전 검사
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API 키를 찾을 수 없습니다. Secrets 설정을 확인하세요.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    
    # 2. 모델 설정 (경로 명시 및 정확도 우선 설정)
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        generation_config={"temperature": 0.1, "top_p": 0.95},
        system_instruction="당신은 한국철도공사 품질검사 전문가입니다."
    )
    
    st.success("✅ 시스템이 정상적으로 연결되었습니다.")

except Exception as e:
    st.error(f"초기 설정 오류: {e}")

# (이하 4가지 입력 항목 UI 코드는 기존과 동일하게 유지)
