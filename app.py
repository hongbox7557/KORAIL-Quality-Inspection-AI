import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="API 테스트", layout="wide")

st.title("🔧 Gemini API 연결 테스트")

# STEP 1: API 키 확인
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ STEP 1 실패: GOOGLE_API_KEY가 Secrets에 없습니다.")
    st.stop()
else:
    st.success("✅ STEP 1 통과: API 키 확인됨")

# STEP 2: 모델 연결 확인
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
    st.success("✅ STEP 2 통과: 모델 연결 성공")
except Exception as e:
    st.error(f"❌ STEP 2 실패: {e}")
    st.stop()

# STEP 3: 실제 응답 확인
if st.button("테스트 요청 보내기"):
    try:
        response = model.generate_content("안녕하세요, 한 문장으로 답해주세요.")
        st.success("✅ STEP 3 통과: 응답 수신 성공")
        st.write("응답 내용:", response.text)
    except Exception as e:
        st.error(f"❌ STEP 3 실패: {e}")
        import traceback
        st.code(traceback.format_exc())
