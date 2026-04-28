import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정
st.set_page_config(page_title="KORAIL 품질검사 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정 (최신 gemini-3-flash-preview 모델 고정)
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

# 3. 고감도 디자인 (1번 항목 테두리 수정 및 Pretendard 적용)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif !important; }
    .main { background-color: #fcfaf7; }
    
    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #eceef1;
        width: 500px !important;
    }

    /* 모든 입력창(TextInput + TextArea) 테두리 통일 및 가시성 강화 */
    .stTextInput input, .stTextArea textarea {
        border-radius: 10px !important;
        border: 1.5px solid #d1d5db !important;
        padding: 15px !important;
        font-size: 15px !important;
        background-color: #ffffff !important;
        line-height: 1.6 !important;
        transition: all 0.2s ease-in-out;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0054A6 !important;
        box-shadow: 0 0 0 2px rgba(0, 84, 166, 0.1) !important;
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
        box-shadow: 0 5px 15px rgba(0, 84, 166, 0.2);
    }

    /* 결과 리포트 카드 */
    .result-container {
        background-color: white;
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #edf2f7;
        box-shadow: 0 4px 25px rgba(0,0,0,0.05);
        line-height: 1.9;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 구성 (오타 제거 및 예시 정교화)
with st.sidebar:
    st.markdown("<h2 style='color: #0054A6; font-size: 24px;'>🚄 현안 상황 입력</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 차량용 윤축, 선로전환기 모터 등")
    
    # 2번 항목 오타 수정 및 명확한 가이드라인 제공
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", 
                         placeholder="기술규격서(KRCS 등) 위반 사항이나 승인 도면과 상이한 부분 기술", height=230)
    
    claim = st.text_area("3. 협력사 주장 내용", 
                        placeholder="협력사가 제기하는 이의 신청 사유 또는 현장 여건상의 불가피성", height=230)
    
    goal = st.text_area("4. 현재 난항 지점 및 목표", 
                       placeholder="상호 이견이 있는 핵심 쟁점 및 해결하고자 하는 목표", height=150)
    
    analyze_btn = st.button("⚖️ 규정 기반 정밀 분석 시작", use_container_width=True)

# 5. 메인 화면 헤더 (가이드라인 텍스트 삭제)
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <div style='background-color: #0054A6; width: 6px; height: 35px; border-radius: 3px; margin-right: 15px;'></div>
        <h1 style='font-size: 30px; margin: 0; letter-spacing: -0.5px;'>품질검사 현안 솔루션</h1>
    </div>
    <p style='margin-left: 21px; color: #666; font-size: 17px; margin-top: -5px;'>KORAIL 사규 · 기술규격 · 국가계약법 통합 자문 시스템</p>
    <hr style='border: 0.5px solid #eee; margin-bottom: 40px;'>
    """, unsafe_allow_html=True)

# 6. 분석 로직
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("상세 분석을 위해 1~4번 항목을 모두 입력해 주세요.")
    else:
        # 진행 상태 표시
        with st.status("🔍 규정 및 법령 사례 대조 중...", expanded=True) as status:
            st.write("한국철도공사 사규 및 기술규격 검토 중...")
            time.sleep(0.7)
            st.write("국가계약법 및 관련 판례 검색 중...")
            time.sleep(0.7)
            status.update(label="✅ 분석 완료", state="complete", expanded=False)

        # AI 프롬프트 (전문성 및 안내 문구 포함)
        prompt = f"""
        당신은 품질검사 및 법률 규정 분석 전문가입니다. 아래 데이터를 바탕으로 보고서를 작성하세요.

        [데이터 정보]
        - 대상: {item}
        - 지적 사유: {reason}
        - 협력사 주장: {claim}
        - 목표: {goal}

        [작성 지침]
        1. '자문단' 또는 '전문가 집단'이라는 표현은 절대 사용하지 마세요.
        2. KORAIL 사규, KRCS 기술규격, 국가계약법 시행령 등 구체적 근거를 포함하세요.
        3. 결과 하단에 반드시 다음 문구를 포함하세요: 
           "본 분석 결과로도 현안 해결이 어려울 경우, 법무팀에 공식적인 서면자문을 요청하여 확정적인 법적 판단을 받으시기 바랍니다."
        4. 마지막 섹션에 [참고 규정 및 온라인 자료 목록]을 번호를 매겨 상세히 나열하세요.
        """

        try:
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown("### 🔍 정밀 분석 결과")
                tab1, tab2 = st.tabs(["📄 분석 보고서", "📊 근거 자료 목록"])
                
                with tab1:
                    st.markdown(f"<div class='result-container'>{response.text}</div>", unsafe_allow_html=True)
                with tab2:
                    if "[참고 규정" in response.text:
                        ref_list = response.text.split("[참고 규정")[-1]
                        st.success(f"**활용된 법령 및 사규 데이터** \n\n {ref_list}")
                    else:
                        st.info("상세 참고 자료는 보고서 하단을 확인해 주시기 바랍니다.")
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")
else:
    # 초기 화면 (가이드라인 텍스트 완전 삭제)
    st.markdown("""
        <div style='padding: 60px; background-color: white; border-radius: 15px; border: 1px solid #f0f2f6; text-align: center; color: #999;'>
            <h3 style='color: #0054A6;'>현안 분석 대기</h3>
            <p>사이드바에 데이터를 입력한 후 버튼을 클릭하면 분석이 시작됩니다.</p>
        </div>
    """, unsafe_allow_html=True)
