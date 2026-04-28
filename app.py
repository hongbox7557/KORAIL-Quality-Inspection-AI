import streamlit as st
import google.generativeai as genai

# 1. 고감도 페이지 및 테마 설정
st.set_page_config(page_title="품질검사 현안 솔루션", layout="wide")

# 디자인: 입력창 최적화 및 결과창 가독성 강화
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    .stTextArea textarea { 
        min-height: 250px !important; 
        border-radius: 12px !important;
        font-size: 16px !important;
    }
    section[data-testid="stSidebar"] { width: 500px !important; }
    .result-card { 
        padding: 30px; 
        border-radius: 20px; 
        background-color: white; 
        border: 1px solid #eef0f2;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. API 설정 (모델명: gemini-3-flash-preview)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 최신 모델명으로 업데이트
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"모델 연결 중 오류가 발생했습니다: {e}")
        st.stop()
else:
    st.error("Streamlit Cloud 설정(Secrets)에서 GOOGLE_API_KEY를 등록해주세요.")
    st.stop()

# 3. 사이드바: 입력 폼
with st.sidebar:
    st.title("📋 현안 분석 데이터")
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="부품명 또는 규격명")
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", height=200)
    claim = st.text_area("3. 협력사 주장 내용", height=200)
    goal = st.text_area("4. 현재 난항 지점 및 목표", height=150)
    
    analyze_btn = st.button("⚖️ 규정 기반 분석 시작", use_container_width=True)

# 4. 메인 화면 구성 및 로직
st.title("⚖️ 품질검사 현안 솔루션")
st.subheader("한국철도공사 사규 · 기술규격 · 국가계약법 기반 자문")

if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("분석을 위해 모든 항목을 입력해주세요.")
    else:
        # 진행 상태 표시
        status_text = st.empty()
        status_text.info("🔄 데이터를 분석하고 규정 사례를 검토 중입니다...")
        
        # 프롬프트 구성
        prompt = f"""
        당신은 한국철도공사(KORAIL)의 품질검사 전문가 및 법률 자문가입니다.
        아래 정보를 바탕으로 사규와 국가계약법에 근거한 분석 보고서를 작성하세요.
        
        1. 품목: {item}
        2. 공사 지적: {reason}
        3. 협력사 주장: {claim}
        4. 목표: {goal}
        
        [요구사항]
        - 관련 법령(국가계약법 등) 및 사규를 인용하여 논리적으로 분석할 것.
        - 향후 대응을 위한 실무적 가이드라인을 제시할 것.
        """
        
        try:
            # AI 모델 호출
            response = model.generate_content(prompt)
            
            if response and response.text:
                status_text.empty() # 로딩 메시지 제거
                st.markdown("### 🔍 규정 기반 분석 결과")
                st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
            else:
                st.error("AI 응답을 생성하지 못했습니다. 다시 시도해 주세요.")
        except Exception as e:
            st.error(f"분석 도중 오류가 발생했습니다. 원인: {e}")
else:
    st.info("왼쪽 사이드바에 내용을 입력하신 후 분석 버튼을 눌러주세요.")
