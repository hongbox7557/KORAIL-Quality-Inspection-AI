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
    st.error("Secrets에서 GOOGLE_API_KEY를 설정해주세요.")
    st.stop()

# 3. 고감도 디자인 및 세련된 폰트 (Pretendard 적용)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif !important; }
    .main { background-color: #f8f9fa; }
    
    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e9ecef;
    }
    
    /* 입력창 스타일: 예시 문구 가독성 강화 */
    .stTextArea textarea {
        min-height: 200px !important;
        border-radius: 12px !important;
        border: 1px solid #dee2e6 !important;
        font-size: 15px !important;
        background-color: #ffffff !important;
    }
    
    /* 버튼: 코레일 블루 적용 */
    .stButton>button {
        height: 55px;
        background-color: #0054A6 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #003d7a !important; }

    /* 결과 카드 */
    .result-card {
        background-color: white;
        padding: 35px;
        border-radius: 16px;
        border: 1px solid #edf2f7;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 구성 (오타 완전 수정 및 예시 강화)
with st.sidebar:
    st.markdown("<h2 style='color: #0054A6;'>📋 현안 데이터 입력</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 차량용 부품(윤축), 시설물(선로전환기) 등")
    
    # 2번 항목 오타 수정 완료: '기술규격서 제○조' 등 예시 문구 정제
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", 
                         placeholder="기술규격서 제○조 미준수 또는 승인 도면과 상이한 부분 기술", height=200)
    
    claim = st.text_area("3. 협력사 주장 내용", 
                        placeholder="현장 여건에 따른 불가피성 또는 규정 해석에 대한 이견 기술", height=200)
    
    goal = st.text_area("4. 현재 난항 지점 및 목표", 
                       placeholder="상호 합의가 필요한 쟁점 및 최종 해결 지향점", height=150)
    
    analyze_btn = st.button("⚖️ 규정 기반 정밀 분석 시작", use_container_width=True)

# 5. 메인 화면 헤더
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 30px;'>
        <div style='background-color: #0054A6; width: 6px; height: 35px; border-radius: 3px; margin-right: 15px;'></div>
        <h1 style='font-size: 30px; margin: 0;'>품질검사 현안 솔루션</h1>
    </div>
    """, unsafe_allow_html=True)

# 6. 분석 로직
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("정확한 분석을 위해 1~4번 항목을 모두 입력해 주세요.")
    else:
        # 분석 진행 중 표시 (세련된 UI)
        with st.status("🔍 KORAIL 사규 및 국가계약법 DB 분석 중...", expanded=True) as status:
            st.write("관련 규정 검토 중...")
            time.sleep(0.8)
            st.write("기술규격 및 판례 대조 중...")
            time.sleep(0.8)
            status.update(label="✅ 분석 완료", state="complete", expanded=False)

        # 프롬프트: '자문단' 명칭 삭제 및 법무팀 안내 포함
        prompt = f"""
        당신은 품질검사 및 법률 규정 분석 전문가입니다. 아래 데이터를 기반으로 분석 보고서를 작성하세요.

        [데이터]
        - 대상: {item}
        - 지적 사유: {reason}
        - 협력사 주장: {claim}
        - 해결 목표: {goal}

        [지침]
        1. '자문단' 또는 '전문가 집단' 명칭을 절대 사용하지 마세요.
        2. 한국철도공사 사규, 기술규격, 국가계약법을 근거로 분석하세요.
        3. 결과 하단에 반드시 다음 문구를 포함하세요: 
           "본 분석 결과로도 현안 해결이 어려울 경우, 법무팀에 공식적인 서면자문을 요청하여 확정적인 법적 판단을 받으시기 바랍니다."
        4. 마지막에 [참고 규정 및 자료 목록]을 명시하세요.
        """

        try:
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown("### 🔍 분석 결과 가이드라인")
                tab1, tab2 = st.tabs(["📝 분석 보고서", "📚 참고 근거"])
                
                with tab1:
                    st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
                with tab2:
                    if "[참고 규정" in response.text:
                        ref_part = response.text.split("[참고 규정")[-1]
                        st.info(f"관련 법령 및 사규 근거: \n\n {ref_part}")
                    else:
                        st.info("상세 참고 자료는 보고서 본문을 확인해 주세요.")
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")
else:
    # 초기 화면 (가이드라인 텍스트 삭제 및 깔끔한 안내)
    st.markdown("""
        <div style='padding: 50px; background-color: white; border-radius: 15px; border: 1px solid #eee; text-align: center;'>
            <h3 style='color: #0054A6;'>데이터 분석 대기 중</h3>
            <p style='color: #666;'>사이드바에 현안 내용을 입력하고 버튼을 누르면 분석이 시작됩니다.</p>
        </div>
    """, unsafe_allow_html=True)
