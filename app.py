import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="API 테스트", layout="wide")
st.title("🔧 Gemini API 연결 테스트")

# STEP 1: API 키 확인
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ STEP 1 실패: API 키 없음")
    st.stop()
st.success("✅ STEP 1 통과: API 키 확인됨")

# STEP 2: 모델 연결
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.success("✅ STEP 2 통과: 모델 연결 성공")
except Exception as e:
    st.error(f"❌ STEP 2 실패: {e}")
    st.stop()

# STEP 3: 버튼 없이 자동 실행
st.info("🔄 STEP 3: API 호출 중...")
try:
    response = model.generate_content("안녕이라고만 답해줘")
    st.success(f"✅ STEP 3 통과! 응답: {response.text}")
except Exception as e:
    st.error(f"❌ STEP 3 실패: {e}")
    import traceback
    st.code(traceback.format_exc())
