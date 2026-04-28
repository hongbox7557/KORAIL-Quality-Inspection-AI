import streamlit as st
import google.generativeai as genai

# 1. 고감도 페이지 및 테마 설정
st.set_page_config(page_title="품질검사 현안 솔루션", layout="wide")

# 디자인 개선: 입력창 확대 및 전문적인 색감 적용
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    
    /* 입력창(TextArea) 높이 대폭 확대 */
    .stTextArea textarea { 
        min-height: 250px !important; 
        border-radius: 12px !important;
        border: 1px solid #d1d1d1 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    /* 사이드바 너비 확장 */
    section[data-testid="stSidebar"] { width: 500px !important; }
    
    /* 결과 카드 디자인 */
    .result-card { 
        padding: 30px; 
        border-radius: 20px; 
        background-color: white; 
        border: 1px solid #eef0f2;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        line-height: 1.8;
    }
    
    /* 버튼 스타일 */
    .stButton>button { 
        height: 55px; 
        font-weight: bold; 
        font-size: 18px !important;
        border-radius: 10px; 
        background-color: #2c3e50; 
        color: white; 
        border: none;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API 설정
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Streamlit Cloud 설정(Secrets)에서 GOOGLE_API_KEY를 등록해주세요.")
    st.stop()

# 3. 사이드바: 입력 폼 (오타 수정 및 문구 정제)
with st.sidebar:
    st.title("📋 현안 분석 데이터")
    st.markdown("정확하고 객관적인 자문을 위해 아래 4가지 항목을 상세히 입력해주세요.")
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 차량용 부품명 또는 기술 규격명")
    
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", 
                         placeholder="품질규격서 조항 미준수 사항 등 구체적 지적 내용", height=200)
    
    claim = st.text_area("3. 협력사 주장 내용", 
                        placeholder="협력사가 제기하는 이의 신청 사유 또는 현장 여건", height=200)
    
    goal = st.text_area("4. 현재 난항 지점 및 목표", 
                       placeholder="의사결정이 필요한 쟁점 및 해결하고자 하는 목표", height=150)
    
    analyze_btn = st.button("⚖️ 규정 기반 분석 시작")

# 4. 메인 화면 구성
st.title("⚖️ 품질검사 현안 솔루션")
st.subheader("한국철도공사 사규 · 기술규격 · 국가계약법 기반 자문 시스템")
st.markdown("---")

if analyze_btn:
    if not (item and reason and claim and goal):
        st.warning("상세한 분석을 위해 모든 항목을 빠짐없이 입력해주세요.")
    else:
        # AI 프롬프트 구성
        prompt = f"""
        당신은 한국철도공사(KORAIL)의 품질검사 전문가 및 법률 자문가입니다.
        제공된 정보를 바탕으로 관련 사규와 국가계약법에 근거한 객관적 분석 보고서를 작성하세요.
        
        [입력 데이터]
        1. 대상 품목: {item}
        2. 공사 입장(
