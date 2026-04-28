import streamlit as st
import google.generativeai as genai

# 1. 고감도 페이지 및 테마 설정
st.set_page_config(page_title="품질검사 현안 솔루션", layout="wide")

# 디자인 개선: 입력창 확대 및 전문적인 색감 적용
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    
    /* 입력창(TextArea) 높이 대폭 확대 및 텍스트 정렬 */
    .stTextArea textarea { 
        min-height: 250px !important; 
        border-radius: 12px !important;
        border: 1px solid #d1d1d1 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        padding: 15px !important;
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
        font-size: 16px;
    }
    
    /* 분석 버튼 스타일 */
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

# 2. API 설정 (Secrets 확인)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Streamlit Cloud의 'Advanced Settings > Secrets'에 GOOGLE_API_KEY를 등록해야 합니다.")
    st.stop()

# 3. 사이드바: 입력 폼 (문구 정제 및 오타 수정)
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
    
    # 버튼 클릭 여부를 변수에 담음
    analyze_submitted = st.button("⚖️ 규정 기반 분석 시작")

# 4. 메인 화면 구성
st.title("⚖️ 품질검사 현안 솔루션")
st.subheader("한국철도공사 사규 · 기술규격 · 국가계약법 기반 자문 시스템")
st.markdown("---")

if analyze_submitted:
    if not (item and reason and claim and goal):
        st.warning("모든 항목을 빠짐없이 입력해야 정확한 분석이 가능합니다.")
    else:
        # 프롬프트 생성 시 줄바꿈과 따옴표 오류 방지를 위해 f-string 구조 정밀 교정
        analysis_prompt = (
            f"당신은 한국철도공사(KORAIL)의 품질검사 전문가 및 법률 자문가입니다.\n"
            f"제공된 정보를 바탕으로 관련 사규와 국가계약법에 근거한 객관적 분석 보고서를 작성하세요.\n\n"
            f"[입력 데이터]\n"
            f"1. 대상 품목: {item}\n"
            f"2. 공사 입장(지적 사유): {reason}\n"
            f"3. 협력사 주장: {claim}\n"
            f"4. 난항 및 목표: {goal}\n\n"
            f"[보고서 구성 요소]\n"
            f"- 관련 사규 및 국가계약법 조항 인용 및 분석\n"
            f"- 양측 주장의 기술적/법적 쟁점 비교\n"
            f"- 객관적인 판단 가이드라인 및 대응 논리\n"
            f"- 향후 조치 권고 사항"
        )
        
        with st.spinner("규정 및 법령 사례를 정밀 분석 중입니다..."):
            try:
                response = model.generate_content(analysis_prompt)
                st.markdown("### 🔍 규정 기반 분석 결과")
                # 최종 결과 출력
                st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"분석 도중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에 현안 내용을 입력하신 후 [분석 시작] 버튼을 눌러주세요.")
