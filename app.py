import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="KORAIL 품질검사 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"모델 연결 오류: {e}")
        st.stop()
else:
    st.error("Streamlit Secrets에 GOOGLE_API_KEY를 등록해 주세요.")
    st.stop()

# 3. 스타일 (🔥 문제 해결 CSS 포함)
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

* { font-family: 'Pretendard', sans-serif !important; }
.main { background-color: #f8f9fa; }

/* ✅ 사이드바 전체 */
section[data-testid="stSidebar"] {
    background-color: white !important;
    border-right: 1px solid #edf2f7;
}

/* ✅ 문제 원인 제거 (hover 시 뜨는 상단 텍스트 제거) */
section[data-testid="stSidebarNav"] {
    display: none !important;
}

/* 추가로 불필요한 상단 영역 제거 */
section[data-testid="stSidebar"] > div:first-child {
    display: none !important;
}

/* 입력창 */
.stTextInput input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid #d1d5db !important;
    padding: 18px !important;
    font-size: 15px !important;
    background-color: #ffffff !important;
    transition: all 0.2s ease-in-out;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #0054A6 !important;
    box-shadow: 0 0 0 3px rgba(0, 84, 166, 0.1) !important;
    outline: none !important;
}

/* 버튼 */
.stButton>button {
    height: 60px;
    background-color: #0054A6 !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    border: none !important;
    margin-top: 15px;
    transition: all 0.3s;
}
.stButton>button:hover {
    background-color: #003F7F !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 84, 166, 0.2);
}

/* 결과 */
.result-container {
    background-color: white;
    padding: 45px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    line-height: 2.0;
    color: #2d3748;
}
</style>
""", unsafe_allow_html=True)

# 4. 사이드바
with st.sidebar:
    st.markdown("<h2 style='color: #0054A6;'>📋 현안 상황 입력</h2>", unsafe_allow_html=True)
    
    item = st.text_input("1. 검사 대상 품목")
    reason = st.text_area("2. 검사 불합격 사유", height=180)
    claim = st.text_area("3. 협력사 주장", height=180)
    goal = st.text_area("4. 목표", height=120)
    
    st.markdown("---")
    analyze_btn = st.button("⚖️ 분석 시작", use_container_width=True)

# 5. 메인
st.title("🚆 품질검사 현안 솔루션")

# 6. 분석
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("모든 항목 입력 필요")
    else:
        with st.status("분석 중...", expanded=True):
            time.sleep(1)

        prompt = f"""
        품목: {item}
        사유: {reason}
        협력사 주장: {claim}
        목표: {goal}
        """

        try:
            response = model.generate_content(prompt)
            st.markdown("### 결과")
            st.markdown(f"<div class='result-container'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"오류: {e}")

else:
    st.info("좌측 입력 후 실행하세요.")
