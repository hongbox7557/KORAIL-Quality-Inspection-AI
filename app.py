import streamlit as st
import google.generativeai as genai

# 1. 고감도 페이지 설정
st.set_page_config(page_title="품질검사 지원 시스템", layout="wide")

# AI 스튜디오 느낌의 커스텀 디자인
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #4A90E2; color: white; border: none; }
    .stTextArea textarea { border-radius: 10px; }
    .report-box { padding: 20px; border-radius: 15px; background-color: white; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. API 설정 (Secrets에서 불러오기)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 사이드바: 입력 폼 구성 (사용자가 요청한 4가지 항목)
with st.sidebar:
    st.header("📋 분석 상황 입력")
    st.info("정확한 자문을 위해 아래 항목을 상세히 입력해주세요.")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 선로 전환기용 모터")
    reason = st.text_area("2. 불합격 및 지적 사유 (공사 입장)", placeholder="기술규격서 제○조 미흡 등")
    claim = st.text_area("3. 협력사 주장 내용", placeholder="현장 여건에 따른 불가피성 등")
    goal = st.text_area("4. 현재 난항 지점 및 목표", placeholder="공기 준수와 품질 확보 사이의 접점 등")
    
    analyze_btn = st.button("⚖️ 규정 기반 분석 시작")

# 4. 메인 화면: 결과 출력
st.title("⚖️ 품질검사 현안 솔루션")
st.write("한국철도공사 사규, 기술규격 및 국가계약법 기반 객관적 가이드라인")

if analyze_btn:
    if not (item and reason and claim and goal):
        st.warning("모든 항목을 입력해야 정확한 분석이 가능합니다.")
    else:
        # AI에게 전달할 프롬프트 구성
        prompt = f"""
        당신은 한국철도공사(KORAIL)의 품질검사 전문 자문 AI입니다. 
        아래 상황에 대해 사규, 기술규격, 국가계약법을 근거로 객관적인 가이드라인을 제시하세요.
        
        [검사 대상]: {item}
        [지적 사유]: {reason}
        [협력사 주장]: {claim}
        [현안 및 목표]: {goal}
        
        분석은 다음 순서로 진행하세요:
        1. 관련 규정 검토 (사규 및 법령)
        2. 쟁점 사항 분석
        3. 객관적 대응 가이드라인
        4. 향후 조치 권고 사항
        """
        
        with st.spinner("규정 및 법령 사례를 분석 중입니다..."):
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🔍 분석 결과")
                st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
else:
    # 초기 화면 안내
    st.markdown("""
    ---
    ### 사용 가이드
    1. 왼쪽 사이드바에 현안 내용을 입력하세요.
    2. **[규정 기반 분석 시작]** 버튼을 클릭하세요.
    3. AI가 법령과 사규에 근거한 객관적 판단 근거를 제시합니다.
    
    > **주의:** 본 결과는 AI의 분석이며, 최종 결정 시 관련 부서의 법적 검토를 병행하시기 바랍니다.
    """)
