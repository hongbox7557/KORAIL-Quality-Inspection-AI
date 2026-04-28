import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="KORAIL 품질검사 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정 (Gemini 1.5 Flash)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"연결 오류: {e}")
        st.stop()
else:
    st.error("Secrets에 GOOGLE_API_KEY를 등록해 주세요.")
    st.stop()

# 3. 고감도 디자인 (특정 안내 문구만 정밀 제거)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 폰트 설정 */
    * { font-family: 'Pretendard', sans-serif !important; }
    .main { background-color: #fcfaf7; }
    
    /* [핵심] keyboard_double_arrow_right 등 단축키 안내 문구만 보이지 않게 제거 */
    [data-testid="stInstructions"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        font-size: 0 !important;
    }

    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #eceef1;
    }

    /* 입력창 디자인 (고감도 레이아웃 유지) */
    .stTextInput input, .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #d1d5db !important;
        padding: 18px !important;
        background-color: #ffffff !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        transition: all 0.2s ease-in-out;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0054A6 !important;
        box-shadow: 0 0 0 3px rgba(0, 84, 166, 0.1) !important;
        outline: none !important;
    }

    /* 버튼 디자인 */
    .stButton>button {
        height: 55px;
        background-color: #0054A6 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        border: none !important;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #003F7F !important;
    }

    /* 결과 리포트 영역 */
    .result-box {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 구성
with st.sidebar:
    st.markdown("<h2 style='color: #0054A6; font-size: 22px; margin-bottom: 20px;'>🚄 현안 상황 입력</h2>", unsafe_allow_html=True)
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 차량용 윤축")
    reason = st.text_area("2. 지적 사유 (공사 입장)", placeholder="규격 위반 사항 기술", height=180)
    claim = st.text_area("3. 협력사 주장 내용", placeholder="업체 이의 신청 내용", height=180)
    goal = st.text_area("4. 현재 난항 및 목표", placeholder="해결하고자 하는 쟁점", height=120)
    
    st.markdown("---")
    analyze_btn = st.button("⚖️ 정밀 분석 시작", use_container_width=True)

# 5. 메인 화면
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <div style='background-color: #0054A6; width: 6px; height: 35px; border-radius: 3px; margin-right: 15px;'></div>
        <h1 style='font-size: 28px; margin: 0; letter-spacing: -0.5px;'>품질검사 현안 솔루션</h1>
    </div>
    <hr style='border: 0.5px solid #eee; margin-bottom: 30px;'>
    """, unsafe_allow_html=True)

# 6. 분석 로직
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("상세 분석을 위해 모든 항목을 입력해 주세요.")
    else:
        with st.status("🔍 규정 대조 및 분석 중...", expanded=True) as status:
            time.sleep(1.2)
            status.update(label="✅ 분석 완료", state="complete")

        prompt = f"품목: {item}, 지적사유: {reason}, 업체주장: {claim}, 목표: {goal}. 위 상황을 KORAIL 사규 및 국가계약법 근거로 분석하여 공식 보고서 형태로 작성해줘."
        
        try:
            response = model.generate_content(prompt)
            st.markdown("### 📄 분석 결과 리포트")
            st.markdown(f"<div class='result-box'>{response.text}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"오류 발생: {e}")
else:
    st.markdown("""
        <div style='padding: 60px 40px; background-color: white; border-radius: 20px; border: 1px solid #f0f2f6; text-align: center;'>
            <h3 style='color: #0054A6; font-size: 22px;'>품질검사 현안을 객관적 규정으로 지원합니다.</h3>
            <p style='color: #666; margin-top: 15px;'>사이드바에 정보를 입력하면 분석이 시작됩니다.</p>
        </div>
    """, unsafe_allow_html=True)
