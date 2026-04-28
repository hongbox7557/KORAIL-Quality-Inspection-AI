import streamlit as st
import google.generativeai as genai
import os

# 1. 페이지 설정 (업무용 시스템 느낌)
st.set_page_config(page_title="품질검사 지원 AI 시스템", page_icon="🔍", layout="wide")

# 2. 보안 설정 (API 키)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 3. 사이드바 - 설정 및 가이드
with st.sidebar:
    st.header("⚙️ 시스템 설정")
    st.info("""
    **근거 법령 및 규정:**
    - 한국철도공사 사규
    - 철도차량/시설 기술규격
    - 국가를 당사자로 하는 계약법
    """)

# 4. 메인 화면 UI
st.title("🔍 품질검사 지원 AI 시스템")
st.markdown("---")
st.subheader("📝 분석 상황 입력")
st.write("정확하고 객관적인 자문을 위해 아래 4가지 항목을 상세히 입력해주세요.")

# 입력 폼 (4가지 항목 분리)
with st.form("inspection_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        item_name = st.text_input("1. 검사 대상 품목", placeholder="예: 철도차량용 제동 패드")
        reason_fail = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", placeholder="규정 위반 내용 및 기술적 지적 사항")
    
    with col2:
        vendor_claim = st.text_area("3. 협력사 주장 내용", placeholder="협력사 측의 이의 제기 및 소명 내용")
        goal = st.text_area("4. 현재 난항 지점 및 목표", placeholder="해결이 필요한 쟁점 및 최종 도출 목표")
        
    submit_button = st.form_submit_button("⚖️ 규정 기반 분석 시작")

# 5. AI 분석 로직
if submit_button:
    if not (item_name and reason_fail and vendor_claim and goal):
        st.warning("모든 항목을 입력해야 정확한 분석이 가능합니다.")
    else:
        with st.spinner("사규 및 관련 법령을 분석 중입니다..."):
            # AI에게 전달할 최종 프롬프트 조립
            full_prompt = f"""
            [품질검사 분석 요청]
            1. 품목: {item_name}
            2. 지적 사유: {reason_fail}
            3. 협력사 주장: {vendor_claim}
            4. 쟁점 및 목표: {goal}
            
            위 상황에 대해 한국철도공사 사규, 기술규격, 국가계약법을 근거로 객관적인 가이드라인을 제공해줘.
            """
            
            # AI Studio 설정을 그대로 가져온 모델 호출
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction="당신은 품질검사 전문가입니다. 한국철도공사 사규와 국가계약법에 근거하여 매우 객관적이고 논리적인 답변을 제공하십시오."
            )
            
            response = model.generate_content(full_prompt)
            
            # 결과 출력
            st.markdown("---")
            st.subheader("📋 분석 결과 및 자문 의견")
            st.markdown(response.text)
