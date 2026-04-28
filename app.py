import streamlit as st
import google.generativeai as genai

# 1. 고감도 페이지 및 테마 설정
st.set_page_config(page_title="품질검사 현안 솔루션", layout="wide")

# 디자인 개선: 입력창 확대 및 전문적인 색감 적용
st.markdown("""
    <style>
    /* 배경 및 폰트 */
    .main { background-color: #fdfaf5; }
    
    /* 입력창(TextArea) 크기 및 디자인 최적화 */
    .stTextArea textarea { 
        min-height: 150px !important; 
        border-radius: 12px !important;
        border: 1px solid #d1d1d1 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    /* 사이드바 너비 및 가독성 */
    section[data-testid="stSidebar"] { width: 450px !important; }
    
    /* 결과 박스 디자인 */
    .result-card { 
        padding: 30px; 
        border-radius: 20px; 
        background-color: white; 
        border: 1px solid #eef0f2;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        line-height: 1.8;
    }
    
    /* 분석 버튼 스타일 */
    .stButton>button { 
        height: 50px; 
        font-weight: bold; 
        border-radius: 10px; 
        background-color: #2c3e50; 
        color: white; 
        border: none;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Secrets에 API 키를 설정해주세요.")
    st.stop()

# 3. 사이드바: 고감도 분석 상황 입력 (문구 교정 및 입력칸 확대)
with st.sidebar:
    st.title("📋 현안 분석 데이터")
    st.markdown("정확하고 객관적인 자문을 위해 아래 항목을 상세히 입력해주세요.")
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 차량용 부품명 또는 규격명")
    
    # height 파라미터를 사용하여 입력칸을 더 크게 만듦
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", 
                         placeholder="품질 규격서 제○조 위반 내용 등 상세 기술", height=150)
    
    claim = st.text_area("3. 협력사 주장 내용", 
                        placeholder="협력사가 제기하는 이의 신청 또는 현장 상황", height=150)
    
    goal = st.text_area("4. 현재 난항 지점 및 목표", 
                       placeholder="의사결정이 필요한 부분 및 해결 지향점", height=120)
    
    analyze_btn = st.button("⚖️ 규정 기반 분석 시작")

# 4. 메인 화면 구성
st.title("⚖️ 품질검사 현안 솔루션")
st.subheader("한국철도공사 사규 · 기술규격 · 국가계약법 기반 자문")

if analyze_btn:
    if not (item and reason and claim and goal):
        st.warning("상세한 분석을 위해 모든 항목을 입력해주세요.")
    else:
        prompt = f"""
        당신은 한국철도공사(KORAIL) 품질검사 전문가 및 법률 자문가입니다.
        제공된 4가지 정보를 바탕으로 규정 중심의 분석 보고서를 작성하세요.
        
        1. 대상: {item}
        2. 공사 입장: {reason}
        3. 협력사 주장: {claim}
        4. 난항 및 목표: {goal}
        
        [지시 사항]
        - 관련 사규 및 국가계약법 조항을 유추하여 인용할 것.
        - 논리적이고 객관적인 톤을 유지할 것.
        - 결론에는 실무적인 가이드라인을 포함할 것.
        """
        
        with st.spinner("규정을 정밀 분석 중입니다..."):
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("### 🔍 분석
