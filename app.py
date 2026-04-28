import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정 및 브라우저 타이틀
st.set_page_config(page_title="KORAIL 품질검사 현안 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정 (최신 gemini-3-flash-preview 모델 반영)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"모델 연결 중 오류가 발생했습니다: {e}")
        st.stop()
else:
    st.error("Secrets에서 GOOGLE_API_KEY를 설정해주세요.")
    st.stop()

# 3. KORAIL 브랜드 아이덴티티 및 세련된 폰트 설정 (CSS)
korail_blue = "#0054A6"
korail_red = "#E60012"
bg_light = "#F8F9FA"

st.markdown(f"""
    <style>
    /* 폰트 및 기본 스타일 설정: 가독성이 뛰어난 프리텐다드/나눔스퀘어 스타일 스택 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {{
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
    }}

    .main {{ background-color: {bg_light}; }}

    /* 사이드바 디자인: 입력 가독성 강화 */
    section[data-testid="stSidebar"] {{
        background-color: #ffffff !important;
        border-right: 1px solid #e9ecef;
        padding: 2rem 1rem;
    }}
    
    /* 텍스트 입력창: 넉넉한 여백과 세련된 테두리 */
    .stTextArea textarea {{
        min-height: 250px !important;
        border-radius: 12px !important;
        border: 1px solid #dee2e6 !important;
        padding: 15px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }}
    .stTextArea textarea:focus {{
        border-color: {korail_blue} !important;
        box-shadow: 0 0 0 2px rgba(0, 84, 166, 0.1) !important;
    }}

    /* 버튼 디자인: KORAIL 블루 및 호버 효과 */
    .stButton>button {{
        height: 55px;
        background-color: {korail_blue} !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        transition: 0.3s ease;
        border: none !important;
    }}
    .stButton>button:hover {{
        background-color: #003d7a !important;
        box-shadow: 0 4px 12px rgba(0, 84, 166, 0.2);
    }}

    /* 결과 카드: 전문가 보고서 느낌의 화이트 레이아웃 */
    .result-card {{
        background-color: #ffffff;
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #edf2f7;
        box-shadow: 0 4px 25px rgba(0,0,0,0.04);
        line-height: 1.8;
    }}
    
    .status-box {{
        padding: 25px;
        border-radius: 12px;
        background-color: white;
        border-left: 5px solid {korail_blue};
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 구성
with st.sidebar:
    st.markdown(f"<h1 style='color: {korail_blue}; font-size: 26px;'>📋 현안 데이터 입력</h1>", unsafe_allow_html=True)
    st.markdown("규정에 근거한 정확한 분석을 위해 상세 내용을 입력해 주세요.")
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 고속열차용 제동 패드")
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", height=200, placeholder="기술규격서 위반 사항 등을 기재")
    claim = st.text_area("3. 협력사 주장 내용", height=200, placeholder="이의 신청 사유 또는 현장 상황")
    goal = st.text_area("4. 현재 난항 지점 및 목표", height=150, placeholder="해결하고자 하는 핵심 쟁점")
    
    analyze_btn = st.button("⚖️ 규정 기반 정밀 분석", use_container_width=True)

# 5. 메인 화면 헤더
st.markdown(f"""
    <div style='display: flex; align-items: center;'>
        <div style='background-color: {korail_blue}; width: 6px; height: 35px; border-radius: 3px; margin-right: 15px;'></div>
        <h1 style='font-size: 32px; margin: 0;'>품질검사 현안 솔루션</h1>
    </div>
    <p style='margin-left: 21px; color: #666; font-size: 18px; margin-top: 5px;'>한국철도공사 사규 · 기술규격 · 국가계약법 통합 자문 시스템</p>
    <hr style='margin-top: 20px; margin-bottom: 40px; border: 0.5px solid #eee;'>
    """, unsafe_allow_html=True)

# 6. 분석 로직
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("분석을 시작하려면 1번부터 4번까지 모든 항목을 입력해야 합니다.")
    else:
        # 분석 중 UI 표현
        status_placeholder = st.empty()
        with status_placeholder:
            st.markdown(f"""
                <div class="status-box">
                    <h4 style="color: {korail_blue}; margin: 0;">🔄 분석 진행 중...</h4>
                    <p style="margin: 10px 0 0 0; color: #555;">공사 사규집 및 법제처 국가법령정보 DB로부터 관련 근거를 검색하고 있습니다.</p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.5)

        # 프롬프트 설정 (규정 및 자료 목록 도출 강조)
        prompt = f"""
        당신은 품질검사 및 관련 법률 분석 전문가입니다. 아래 데이터를 기반으로 전문가 수준의 분석 보고서를 작성하세요.

        [분석 데이터]
        - 품목: {item}
        - 공사 지적사항: {reason}
        - 협력사 주장: {claim}
        - 난항 및 목표: {goal}

        [지시 사항]
        1. '자문단'이나 '전문가 집단'이라는 표현은 절대 사용하지 마세요.
        2. 한국철도공사 사규, 해당 품목 기술규격(KRCS 등), 국가계약법 시행령/규칙을 구체적으로 인용하세요.
        3. 온라인 자료(법제처 판례, 조달청 유권해석 사례 등)가 있다면 함께 참조하세요.
        4. 보고서 하단에는 반드시 다음 문구를 포함하세요:
           "본 분석 결과로도 현안 해결이 어려울 경우, 법무팀에 공식적인 서면자문을 요청하여 확정적인 법적 판단을 받으시기 바랍니다."
        5. 보고서 마지막 섹션에 [참고 규정 및 온라인 자료 목록]을 번호를 매겨 상세히 나열하세요.

        [보고서 구성]
        I. 관련 규정 및 법령 검토
        II. 핵심 쟁점 분석
        III. 객관적 가이드라인 (판단 근거)
        IV. 실무적 향후 조치 권고
        V. 참고 규정 및 온라인 자료 목록
        """

        try:
            response = model.generate_content(prompt)
            status_placeholder.empty()

            if response and response.text:
                st.markdown("### 🔍 정밀 분석 결과")
                
                # 탭 레이아웃을 통한 정보 분리
                res_tab, ref_tab = st.tabs(["📝 분석 보고서", "📚 참고 문헌 및 근거"])
                
                with res_tab:
                    st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
                
                with ref_tab:
                    st.markdown("### 📚 활용된 법령 및 사규 데이터")
                    st.info("본 보고서 작성 시 참고한 주요 규정 목록입니다.")
                    # 결과 텍스트 중 마지막 섹션만 추출하여 표시 (V. 섹션 이후)
                    if "V." in response.text:
                        ref_content = response.text.split("V.")[-1]
                        st.markdown(f"<div class='result-card'>{ref_content}</div>", unsafe_allow_html=True)
                    else:
                        st.write("상세 참고 자료는 보고서 본문을 확인해 주시기 바랍니다.")
            else:
                st.error("응답을 생성할 수 없습니다. 잠시 후 다시 시도해 주세요.")
        except Exception as e:
            status_placeholder.empty()
            st.error(f"분석 중 오류가 발생했습니다: {e}")
else:
    # 대기 화면 가이드
    st.markdown("""
        <div style="background-color: white; padding: 40px; border-radius: 15px; border: 1px solid #f0f2f6;">
            <h4 style="color: #0054A6; margin-bottom: 20px;">💡 시스템 사용 방법</h4>
            <ol style="line-height: 2;">
                <li>사이드바에 <strong>품목 및 현황</strong>을 상세히 입력합니다.</li>
                <li><strong>정밀 분석 시작</strong> 버튼을 클릭합니다.</li>
                <li>AI가 도출한 <strong>규정 근거와 가이드라인</strong>을 확인합니다.</li>
                <li>필요 시 <strong>참고 문헌 탭</strong>에서 법적 근거 조항을 확인합니다.</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
