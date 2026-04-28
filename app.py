import streamlit as st
import google.generativeai as genai
import os

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="품질검사 지원 AI", page_icon="🔍", layout="wide")
st.title("🔍 품질검사 지원 AI 시스템")
st.markdown("---")

# 2. 보안 설정: Secrets에서 GEMINI_API_KEY 불러오기
# Streamlit Cloud의 Settings > Secrets에 GEMINI_API_KEY가 등록되어 있어야 합니다.
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API 키를 찾을 수 없습니다. Streamlit Secrets 설정을 확인해주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 3. 모델 설정 (AI Studio의 지침과 설정을 이식)
# 품질검사의 객관성을 위해 도출 온도를 낮게(0.2) 설정하는 것이 핵심입니다.
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",  # 'models/'를 앞에 붙여주세요
    generation_config={
        "temperature": 0.2,
        "top_p": 0.95,
    },
    system_instruction=SYSTEM_PROMPT
)
    system_instruction="""당신은 한국철도공사의 품질검사 자문 전문가입니다. 
    사용자가 제공하는 4가지 정보를 바탕으로 사규, 기술규격, 국가계약법에 근거하여 
    협력사와의 갈등 상황에 대한 객관적인 가이드라인과 법률·기술적 자문을 제공하십시오."""
)

# 4. 분석 상황 입력 폼
st.subheader("📝 분석 상황 입력")
st.info("정확한 자문을 위해 아래 4가지 항목을 상세히 입력해주세요.")

with st.form("inspection_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        item = st.text_input("1. 검사 대상 품목", placeholder="예: 철도차량용 제동 장치")
        reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", height=150)
        
    with col2:
        claim = st.text_area("3. 협력사 주장 내용", height=150)
        goal = st.text_area("4. 현재 난항 지점 및 목표", height=150)
        
    submit = st.form_submit_button("⚖️ 규정 기반 분석 시작")

# 5. 결과 도출 로직
if submit:
    if not (item and reason and claim and goal):
        st.warning("⚠️ 모든 항목을 입력해야 분석이 가능합니다.")
    else:
        with st.spinner("규정을 분석하여 자문 의견을 생성 중입니다..."):
            # 프롬프트 구성
            prompt = f"""
            아래 품질검사 현안에 대해 객관적인 분석을 수행해줘.
            
            - 품목: {item}
            - 공사 지적사유: {reason}
            - 협력사 주장: {claim}
            - 해결 목표: {goal}
            
            위 내용을 바탕으로 한국철도공사 사규 및 국가계약법에 따른 법적·기술적 판단 근거와 대응 가이드라인을 제시해줘.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.subheader("📋 분석 결과 및 자문 의견")
                st.success("분석이 완료되었습니다.")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
