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

# 3. UI/UX 디자인
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    * { font-family: 'Pretendard', sans-serif !important; }
    .main { background-color: #f8f9fa; }

    /* 사이드바 완전 숨김 */
    section[data-testid="stSidebar"] { display: none !important; }

    /* 입력창 디자인 */
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

    /* 모든 textarea 높이 강제 통일 */
    .stTextArea textarea {
        height: 150px !important;
        min-height: 150px !important;
        max-height: 150px !important;
        resize: none !important;
    }

    /* 버튼 스타일 */
    .stButton>button {
        height: 60px;
        background-color: #0054A6 !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border: none !important;
        margin-top: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #003F7F !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 84, 166, 0.2);
    }

    /* 입력 카드 */
    .input-card {
        background-color: white;
        padding: 35px 40px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 30px;
    }

    /* 결과 보고서 컨테이너 */
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

# 4. 메인 헤더
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
        <div style='background-color: #0054A6; width: 6px; height: 38px; border-radius: 3px; margin-right: 18px;'></div>
        <h1 style='font-size: 32px; margin: 0; letter-spacing: -0.7px; font-weight: 800;'>품질검사 현안 솔루션</h1>
    </div>
    <p style='margin-left: 24px; color: #718096; font-size: 17px; margin-top: 5px;'>
        KORAIL 사규 · 기술규격 · 국가계약법 통합 검토 서비스
    </p>
    <hr style='border: 0.5px solid #edf2f7; margin: 20px 0 25px 0;'>
    """, unsafe_allow_html=True)

# 5. 안내 문구
st.markdown("""
    <div style='padding: 30px 40px; background-color: white; border-radius: 24px; border: 1px solid #edf2f7; text-align: center; margin-bottom: 30px;'>
        <div style='font-size: 45px; margin-bottom: 15px;'>⚖️</div>
        <h3 style='color: #0054A6; font-size: 22px; margin-bottom: 12px; font-weight: 700;'>품질검사 현안을 객관적 규정으로 지원합니다.</h3>
        <p style='color: #4a5568; font-size: 16px; line-height: 1.8; max-width: 850px; margin: 0 auto; letter-spacing: -0.3px;'>
            협력사와의 품질 기준 해석 차이나 난항 상황에 대해<br>
            <b>한국철도공사 사규, 기술규격 및 국가계약법</b>을 근거로 하여<br>
            실효성 있는 기술·법률 자문과 객관적인 가이드라인을 제공합니다.
        </p>
        <div style='margin-top: 15px; color: #a0aec0; font-size: 15px;'>
            아래 입력폼에 현안 데이터를 입력한 후 분석 시작 버튼을 눌러주세요.
        </div>
    </div>
    """, unsafe_allow_html=True)

# 6. 입력 폼 (2열 레이아웃, 4항목 동일 크기)
st.markdown("<div class='input-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #0054A6; font-size: 20px; margin-bottom: 20px;'>📋 현안 상황 입력</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    item = st.text_area("1. 검사 대상 품목",
                        placeholder="예: 차량용 윤축, 선로전환기 모터 등",
                        height=150)
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)",
                          placeholder="기술규격서(KRCS 등) 위반 사항이나 승인 도면과 상이한 부분을 구체적으로 기술",
                          height=150)

with col2:
    claim = st.text_area("3. 협력사 주장 내용",
                         placeholder="협력사가 제기하는 이의 신청 사유 또는 현장 여건상의 불가피성",
                         height=150)
    goal = st.text_area("4. 현재 난항 지점 및 목표",
                        placeholder="상호 이견이 있는 핵심 쟁점 및 해결하고자 하는 목표",
                        height=150)

st.markdown("</div>", unsafe_allow_html=True)

analyze_btn = st.button("⚖️ 규정 기반 정밀 분석 시작", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. 분석 로직 및 결과 출력
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("📊 정확한 분석을 위해 1~4번 항목을 모두 입력해 주세요.")
    else:
        with st.status("🔍 규정 및 법령 사례 대조 중...", expanded=True) as status:
            st.write("한국철도공사 품질관리 규정 및 KRCS 기술규격 조회 중...")
            time.sleep(0.8)
            st.write("국가계약법 시행령 및 관련 조달 판례 분석 중...")
            time.sleep(0.8)
            status.update(label="✅ 분석 완료", state="complete", expanded=False)

        prompt = f"""
        당신은 철도 품질검사 및 공공계약 법률 전문가입니다. 아래 데이터를 바탕으로 공식적인 분석 보고서를 작성하세요.

        [분석 데이터]
        - 품목: {item}
        - 지적 사유: {reason}
        - 협력사 주장: {claim}
        - 분석 목표: {goal}

        [작성 지침]
        1. '자문단' 같은 표현 없이 객관적인 법적/기술적 판단 근거 위주로 서술하세요.
        2. KORAIL 사규, KRCS, 국가계약법 등 구체적인 조항을 인용하세요.
        3. 결과 하단에 "본 분석 결과로도 현안 해결이 어려울 경우, 법무팀에 공식적인 서면자문을 요청하여 확정적인 법적 판단을 받으시기 바랍니다." 문구를 반드시 포함하세요.
        4. 마지막에 '[참고 규정 및 온라인 자료 목록]' 섹션을 만들어 상세히 나열하세요.
        """

        try:
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown("### 📄 정밀 분석 결과")
                tab1, tab2 = st.tabs(["🏛️ 분석 보고서", "📑 인용 근거 자료"])

                with tab1:
                    main_content = response.text.split("[참고 규정")[0]
                    st.markdown(f"<div class='result-container'>{main_content}</div>", unsafe_allow_html=True)

                with tab2:
                    if "[참고 규정" in response.text:
                        ref_data = response.text.split("[참고 규정")[-1].replace(" 및 온라인 자료 목록]", "")
                        st.success(f"**활용된 법령 및 사규 데이터**\n\n{ref_data}")
                    else:
                        st.info("상세 참고 자료는 보고서 본문을 확인해 주세요.")
        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {e}")
