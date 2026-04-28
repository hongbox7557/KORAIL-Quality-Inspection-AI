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

# 3. 고감도 디자인 및 아이콘 텍스트 완전 박멸 (최종 강화 버전)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif !important; }
    .main { background-color: #fcfaf7; }
    
    /* [CSS 1차 방어] 툴팁 및 안내 텍스트 영역 완전 비활성화 */
    [data-testid="stInstructions"], 
    [data-testid="stTooltipHoverTarget"],
    .st-ae, .st-af, .st-ag, .st-ah,
    small {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        font-size: 0 !important;
        overflow: hidden !important;
    }

    /* 입력창 및 레이아웃 스타일 */
    .stTextInput input, .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #d1d5db !important;
        padding: 18px !important;
        background-color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #eceef1; }
    .stButton>button {
        height: 55px; background-color: #0054A6 !important; color: white !important;
        border-radius: 10px !important; font-weight: 700; border: none !important;
    }
    </style>

    <script>
    /* [JS 2차 방어] 'keyboard_' 텍스트가 포함된 요소를 실시간으로 찾아내어 텍스트를 지워버림 */
    const observer = new MutationObserver((mutations) => {
        const elements = document.querySelectorAll('span, small, div, p');
        elements.forEach(el => {
            if (el.textContent.includes('keyboard_')) {
                el.textContent = ''; // 텍스트 내용을 직접 삭제
                el.style.display = 'none';
            }
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

# 4. 사이드바 구성
with st.sidebar:
    st.markdown("<h2 style='color: #0054A6; font-size: 24px;'>🚄 현안 상황 입력</h2>", unsafe_allow_html=True)
    item = st.text_input("1. 검사 대상 품목", placeholder="품목 입력")
    reason = st.text_area("2. 지적 사유", placeholder="지적 내용", height=200)
    claim = st.text_area("3. 협력사 주장", placeholder="이의 신청 내용", height=200)
    goal = st.text_area("4. 분석 목표", placeholder="목표 설정", height=120)
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
    if not all([item, reason, claim, goal]):
        st.warning("모든 항목을 입력해 주세요.")
    else:
        with st.status("분석 중...", expanded=True) as status:
            time.sleep(1)
            status.update(label="분석 완료", state="complete")
        
        prompt = f"{item}, {reason}, {claim}, {goal}에 대해 법무팀 자문급 보고서를 작성해줘."
        response = model.generate_content(prompt)
        st.markdown(response.text)
else:
    st.markdown("""
        <div style='padding: 60px 40px; background-color: white; border-radius: 20px; border: 1px solid #f0f2f6; text-align: center;'>
            <h3 style='color: #0054A6;'>품질검사 현안을 객관적 규정으로 지원합니다.</h3>
            <p>사이드바에 정보를 입력하면 규정 및 판례 기반 가이드라인을 제공합니다.</p>
        </div>
    """, unsafe_allow_html=True)
