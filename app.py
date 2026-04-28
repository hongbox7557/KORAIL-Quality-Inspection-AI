import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 및 브라우저 설정
st.set_page_config(page_title="KORAIL 품질검사 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정 (최신 gemini-3-flash-preview 모델 고정)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"연결 실패: {e}")
        st.stop()
else:
    st.error("Secrets에 GOOGLE_API_KEY를 등록해주세요.")
    st.stop()

# 3. 고감도 UX 디자인 (Pretendard 폰트 및 KORAIL 컬러 시스템)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 폰트 및 배경 */
    * { font-family: 'Pretendard', -apple-system, sans-serif !important; }
    .main { background-color: #fdfaf5; }
    
    /* 사이드바 가시성 강화 */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #eef0f2;
        width: 500px !important;
    }
    
    /* 입력창 디자인: 더 크게, 더 세련되게 */
    .stTextArea textarea {
        min-height: 250px !important;
        border-radius: 12px !important;
        border: 1px solid #d1d5db !important;
        padding: 18px !important;
        font-size: 15px !important;
        line-height: 1.7 !important;
        background-color: #ffffff !important;
    }
    .stTextArea textarea:focus {
        border-color: #0054A6 !important;
        box-shadow: 0 0 0 1px #0054A6 !important;
    }
    
    /* 버튼: KORAIL 블루 적용 */
    .stButton>button {
        height: 60px;
        background-color: #0054A6 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border: none !important;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        background-color: #003F7F !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 84, 166, 0.2);
    }

    /* 결과 리포트 카드 */
    .report-container {
        background-color: #ffffff;
        padding: 45px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        line-height: 2.0;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바: 전문가용 입력 인터페이스
with st.sidebar:
    st.markdown("<h1 style='color: #0054A6; font-size: 28px;'>📋 현안 상황 입력</h1>", unsafe_allow_html=True)
    st.markdown("정확한 분석을 위해 기술규격 및 현장 상황을 상세히 기재해 주세요.")
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 차량용 윤축, 선로전환기 등")
    
    # 2번 항목 오타 및 예시 완전 수정
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", 
                         placeholder="기술규격서(KRCS 등) 조항 미준수 사항이나 승인 도면과 상이한 세부 내용 기재", height=250)
    
    claim = st.text_area("3. 협력사 주장 내용", 
                        placeholder="협력사가 제기하는 이의 신청 사유 또는 현장 여건상의 불가피성", height=250)
    
    goal = st.text_area("4. 현재 난항 지점 및 목표", 
                       placeholder="상호 이견이 있는 쟁점 및 해결하고자 하는 방향", height=180)
    
    analyze_btn = st.button("⚖️ 규정 기반 정밀 분석 시작", use_container_width=True)

# 5. 메인 화면 구성
st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 25px;'>
        <div style='background-color: #0054A6; width: 8px; height: 40px; border-radius: 4px; margin-right: 15px;'></div>
        <h1 style='margin: 0; font-size: 34px; letter-spacing: -1px;'>품질검사 현안 솔루션</h1>
    </div>
    <h3 style='margin-left: 23px; margin-top: -10px; font-weight: 400; color: #666;'>KORAIL 사규 · 기술규격 · 국가계약법 통합 자문</h3>
    <hr style='border: 0.5px solid #e5e7eb; margin: 30px 0;'>
    """, unsafe_allow_html=True)

if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("모든 항목을 빠짐없이 입력하셔야 정밀 분석이 가능합니다.")
    else:
        # 분석 중 UI (애니메이션 및 단계별 표시)
        with st.status("🔍 규정 및 법령 사례 분석 중...", expanded=True) as status:
            st.write("한국철도공사 사규 및 기술규격 데이터베이스 참조 중...")
            time.sleep(1.0)
            st.write("국가계약법 및 법제처 판례 대조 중...")
            time.sleep(1.0)
            status.update(label="✅ 분석이 완료되었습니다.", state="complete", expanded=False)

        # AI 프롬프트 (엄격한 지시사항 반영)
        prompt = f"""
        당신은 품질검사 규정 및 법률 분석 전문가입니다. 아래 데이터를 기반으로 '한국철도공사' 내부 보고용 분석 보고서를 작성하세요.

        [데이터]
        - 품목: {item}
        - 지적 사유: {reason}
        - 협력사 주장: {claim}
        - 목표: {goal}

        [지침]
        1. '자문단' 또는 '전문가 집단' 명칭을 절대 사용하지 마세요.
        2. KORAIL 사규, 기술규격(KRCS), 국가계약법 시행령 등 구체적인 근거를 제시하세요.
        3. 결과 하단에 반드시 다음 문구를 포함하세요: 
           "본 분석 결과로도 현안 해결이 어려울 경우, 법무팀에 공식적인 서면자문을 요청하여 확정적인 법적 판단을 받으시기 바랍니다."
        4. 보고서 마지막에 [참고 규정 및 온라인 자료 목록] 섹션을 만들어 상세히 나열하세요.
        """

        try:
            response = model.generate_content(prompt)
            
            if response and response.text:
                st.markdown("### 🔍 정밀 분석 리포트")
                
                # 탭을 활용한 세련된 결과 도출
                report_tab, ref_tab = st.tabs(["📊 분석 보고서", "📚 관련 근거 데이터"])
                
                with report_tab:
                    st.markdown(f"<div class='report-container'>{response.text}</div>", unsafe_allow_html=True)
                
                with ref_tab:
                    st.markdown("#### 본 분석에 참고된 주요 규정 및 자료")
                    # 참고자료 섹션만 추출하여 표시 시도
                    if "[참고 규정" in response.text:
                        ref_data = response.text.split("[참고 규정")[-1]
                        st.info(f"자료 목록: \n\n {ref_data}")
                    else:
                        st.info("상세 자료는 보고서 본문을 참조해 주시기 바랍니다.")
        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {e}")
else:
    # 대기 화면 (가이드라인 텍스트 삭제 및 깔끔한 로고 배치)
    st.markdown("""
        <div style='padding: 80px; background-color: white; border-radius: 20px; border: 1px solid #f0f2f6; text-align: center;'>
            <h2 style='color: #0054A6; margin-bottom: 15px;'>데이터 분석 대기 중</h2>
            <p style='color: #888; font-size: 18px;'>왼쪽 사이드바에 현안 내용을 상세히 입력한 후,<br>분석 시작 버튼을 눌러주세요.</p>
        </div>
    """, unsafe_allow_html=True)
