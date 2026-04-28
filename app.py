import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="KORAIL 품질검사 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정 (gemini-3-flash-preview)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"연결 오류: {e}")
        st.stop()
else:
    st.error("Secrets에 GOOGLE_API_KEY를 등록해 주세요.")
    st.stop()

# 3. 고감도 디자인 및 'keyboard_double_arrow_right' 완전 제거
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif !important; }
    .main { background-color: #fcfaf7; }
    
    /* [핵심] 단축키 안내 텍스트 및 아이콘 태그 강제 제거 */
    [data-testid="stInstructions"], 
    [data-testid="stTooltipHoverTarget"],
    .st-emotion-cache-16ids9d, 
    .st-emotion-cache-1vt4yug,
    small, span:empty {
        display: none !important;
        visibility: hidden !important;
        font-size: 0 !important;
        height: 0 !important;
    }

    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #eceef1;
    }

    /* 입력창 스타일 */
    .stTextInput input, .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #d1d5db !important;
        padding: 18px !important;
        background-color: #ffffff !important;
        line-height: 1.6 !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0054A6 !important;
        box-shadow: 0 0 0 3px rgba(0, 84, 166, 0.1) !important;
    }

    /* 버튼 디자인 */
    .stButton>button {
        height: 55px;
        background-color: #0054A6 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 구성
with st.sidebar:
    st.markdown("<h2 style='color: #0054A6; font-size: 24px; margin-bottom: 20px;'>🚄 현안 상황 입력</h2>", unsafe_allow_html=True)
    item = st.text_input("1. 검사 대상 품목", placeholder="품목 입력")
    reason = st.text_area("2. 지적 사유", placeholder="규격 위반 내용", height=230)
    claim = st.text_area("3. 협력사 주장", placeholder="이의 신청 내용", height=230)
    goal = st.text_area("4. 분석 목표", placeholder="해결하고자 하는 방향", height=150)
    analyze_btn = st.button("⚖️ 정밀 분석 시작", use_container_width=True)

# 5. 메인 화면
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <div style='background-color: #0054A6; width: 6px; height: 35px; border-radius: 3px; margin-right: 15px;'></div>
        <h1 style='font-size: 30px; margin: 0;'>품질검사 현안 솔루션</h1>
    </div>
    <hr style='border: 0.5px solid #eee; margin-bottom: 40px;'>
    """, unsafe_allow_html=True)

if analyze_btn:
    with st.spinner("규정 분석 중..."):
        prompt = f"{item}, {reason}, {claim}, {goal} 분석 보고서 작성해줘."
        response = model.generate_content(prompt)
        st.markdown(response.text)
else:
    st.markdown("""
        <div style='padding: 80px 40px; background-color: white; border-radius: 20px; border: 1px solid #f0f2f6; text-align: center;'>
            <h3 style='color: #0054A6;'>품질검사 현안을 객관적 규정으로 지원합니다.</h3>
            <p>한국철도공사 사규, 기술규격 및 국가계약법을 근거로 가이드라인을 제공합니다.</p>
        </div>
    """, unsafe_allow_html=True)
