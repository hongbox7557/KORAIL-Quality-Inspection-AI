import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="KORAIL 품질검사 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정 (Gemini 1.5 Flash 사용)
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

# 3. [최종 솔루션] CSS + JS 결합형 텍스트 박멸 디자인
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif !important; }
    .main { background-color: #fcfaf7; }
    
    /* [1단계: CSS] 안내 문구 영역의 존재 자체를 부정함 */
    [data-testid="stInstructions"], 
    [data-testid="stTooltipHoverTarget"],
    .st-ae, .st-af, .st-ag, .st-ah,
    small, span:empty {
        display: none !important;
        visibility: hidden !important;
        font-size: 0 !important;
        line-height: 0 !important;
        color: transparent !important;
        height: 0 !important;
        width: 0 !important;
        pointer-events: none !important;
    }

    /* 입력창 디자인 커스텀 */
    .stTextInput input, .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #d1d5db !important;
        padding: 18px !important;
        background-color: #ffffff !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0054A6 !important;
        box-shadow: 0 0 0 3px rgba(0, 84, 166, 0.1) !important;
        outline: none !important;
    }

    /* 버튼 및 사이드바 스타일 */
    section[data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #eceef1; }
    .stButton>button {
        height: 55px; background-color: #0054A6 !important; color: white !important;
        border-radius: 10px !important; font-weight: 700 !important; border: none !important;
    }
    </style>

    <script>
    /* [2단계: JS] 화면에 'keyboard_' 텍스트가 나타나면 즉시 삭제 */
    const observer = new MutationObserver((mutations) => {
        const elements = document.querySelectorAll('span, small, div, p');
        elements.forEach(el => {
            if (el.textContent.includes('keyboard_')) {
                el.innerHTML = ''; // 텍스트 강제 삭제
                el.style.display = 'none';
            }
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

# 4. 사이드바 (입력 필드)
with st.sidebar:
    st.markdown("<h2 style='color: #0054A6; font-size: 24px; margin-bottom: 20px;'>🚄 현안 상황 입력</h2>", unsafe_allow_html=True)
    
    item = st.text_input("1. 검사 대상 품목", placeholder="품목을 입력하세요")
    reason = st.text_area("2. 지적 사유 (공사 입장)", placeholder="기술규격 위반 내용 등", height=200)
    claim = st.text_area("3. 협력사 주장", placeholder="이의 신청 사유", height=200)
    goal = st.text_area("4. 현재 난항 및 목표", placeholder="해결하고자 하는 쟁점", height=150)
    
    st.markdown("---")
    analyze_btn = st.button("⚖️ 규정 기반 정밀 분석 시작", use_container_width=True)

# 5. 메인 화면 구성
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 25px;'>
        <div style='background-color: #0054A6; width: 6px; height: 35px; border-radius: 3px; margin-right: 15px;'></div>
        <h1 style='font-size: 30px; margin: 0; letter-spacing: -0.5px;'>품질검사 현안 솔루션</h1>
    </div>
    <hr style='border: 0.5px solid #eee; margin-bottom: 40px;'>
    """, unsafe_allow_html=True)

# 6. 분석 로직
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("모든 항목을 입력해 주셔야 정밀 분석이 가능합니다.")
    else:
        with st.status("🔍 규정 검토 중...", expanded=True) as status:
            time.sleep(1)
            status.update(label="✅ 검토 완료", state="complete")

        prompt = f"""
        철도 품질검사 전문가로서 아래 상황을 분석하세요.
        - 대상: {item}
        - 지적내용: {reason}
        - 업체주장: {claim}
        - 목표: {goal}
        
        KORAIL 사규 및 국가계약법을 근거로 대응 방안을 제안하고, 
        마지막에 '본 분석은 참고용이며 법적 판단은 법무팀 자문을 거치시기 바랍니다'라는 취지의 문구를 포함하세요.
        """
        
        try:
            response = model.generate_content(prompt)
            st.markdown("### 📄 분석 리포트")
            st.info(response.text)
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")
else:
    # 대기 화면 디자인
    st.markdown("""
        <div style='padding: 80px 40px; background-color: white; border-radius: 20px; border: 1px solid #f0f2f6; text-align: center;'>
            <h3 style='color: #0054A6; font-size: 24px; font-weight: 700;'>품질검사 현안을 객관적 규정으로 지원합니다.</h3>
            <p style='color: #4a5568; font-size: 17px; margin-top: 15px;'>사이드바에 데이터를 입력하면 AI가 사규와 법령을 바탕으로 분석을 시작합니다.</p>
        </div>
    """, unsafe_allow_html=True)
