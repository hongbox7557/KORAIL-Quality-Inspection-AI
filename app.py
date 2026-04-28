import streamlit as st
import google.generativeai as genai
import threading

st.set_page_config(page_title="API 테스트", layout="wide")
st.title("🔧 Gemini API 연결 테스트")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ API 키 없음")
    st.stop()
st.success("✅ STEP 1: API 키 확인됨")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.success("✅ STEP 2: 모델 연결 성공")
except Exception as e:
    st.error(f"❌ STEP 2 실패: {e}")
    st.stop()

# 타임아웃 10초 적용
st.info("🔄 STEP 3: API 호출 중... (최대 10초)")
result = {"text": None, "error": None}

def call_api():
    try:
        response = model.generate_content("안녕이라고만 답해줘")
        result["text"] = response.text
    except Exception as e:
        result["error"] = str(e)

thread = threading.Thread(target=call_api)
thread.start()
thread.join(timeout=10)

if thread.is_alive():
    st.error("❌ STEP 3 실패: 10초 타임아웃 — 네트워크에서 API 호출이 차단된 것 같습니다.")
elif result["error"]:
    st.error(f"❌ STEP 3 실패: {result['error']}")
elif result["text"]:
    st.success(f"✅ STEP 3 통과! 응답: {result['text']}")
else:
    st.error("❌ STEP 3 실패: 응답이 비어있습니다.")
