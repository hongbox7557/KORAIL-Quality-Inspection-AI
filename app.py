import streamlit as st
import google.generativeai as genai
import os

# 1. 페이지 설정 (전문가용 시스템 UI)
st.set_page_config(page_title="품질검사 지원 AI", page_icon="🔍", layout="wide")

# 사이드바: 시스템 정보 및 상태 표시
with st.sidebar:
    st.header("⚙️ 시스템 정보")
    st.markdown("""
    **분석 근거:**
    - 한국철도공사 사규 및 지침
    - 철도차량/시설 기술규격(KRS)
    - 국가를 당사자로 하는 계약법
    """)
    st.divider()
    
    # API 키 연결 상태 확인
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        st.success("✅ 시스템 연결 완료")
    else:
        st.error("❌ API 키 미연결 (Secrets 확인 필요)")

# 2. 모델 설정 및 보안
if api_key:
    genai.configure(api_key=api_key)
    
    # 404 에러 방지를 위해 'models/' 접두사를 명시합니다.
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        generation_config={
            "temperature": 0.2,  # 객관적 자문을 위해 창의성을 낮춤
            "top_p": 0.95,
            "max_output_tokens": 4096,
        },
        system_instruction="""당신은 한국철도공사의 품질검사 자문 전문가입니다. 
        사규, 기술규격, 국가계약법을 근거로 협력사와의 품질 기준 해석 차이에 대해 
        객관적인 기술·법률 자문 가이드라인을 제공하는 것이 임무입니다."""
    )

# 3. 메인 화면 구성
st.title("🔍 품질검사 지원 AI 시스템")
st.subheader("품질검사 현안을 객관적 규정으로 지원합니다.")
st.write("정확하고 객관적인 자문을 위해 아래 4가지 항목에 상세 내용을 입력해주세요.")

# 4. 입력 폼 (요청하신 4가지 항목)
with st.form("inspection_analysis_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        item = st.text_input("1. 검사 대상 품목", placeholder="예: 차량용 견인전동기")
        reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", height=200, placeholder="규격 미달 사항이나 불합격 근거를 상세히 입력")
        
    with col2:
        claim = st.text_area("3. 협력사 주장 내용", height=150, placeholder="협력사가 주장하는 예외 조항이나 소명 내용")
        goal = st.text_area("4. 현재 난항 지점 및 목표", height=150, placeholder="해결이 필요한 쟁점과 기대하는 결과")
        
    submit_button = st.form_submit_button("⚖️ 규정 기반 분석 시작")

# 5. 결과 도출 로직
if submit_button:
    if not api_key:
        st.error("API 키가 설정되지 않아 분석을 시작할 수 없습니다.")
    elif not (item and reason and claim and goal):
        st.warning("모든 항목을 입력해야 정확한 분석 결과가 도출됩니다.")
    else:
        with st.spinner("관련 규정 및 사규를 분석 중입니다. 잠시만 기다려주세요..."):
            # 프롬프트 구성
            user_prompt = f"""
            [품질검사 분석 요청 건]
            - 대상 품목: {item}
            - 공사측 지적 사유: {reason}
            - 협력사측 주장: {claim}
            - 쟁점 및 목표: {goal}
            
            위 상황에 대해 다음 순서로 답변해줘:
            1. 관련 사규 및 법령 근거 제시
            2. 쟁점사항에 대한 객관적 판단
            3. 향후 대응을 위한 기술/법률적 가이드라인
            """
            
            try:
                response = model.generate_content(user_prompt)
                st.markdown("---")
                st.subheader("📋 분석 결과 및 자문 의견")
                st.markdown(response.text)
                st.download_button("결과 복사하기", response.text, file_name=f"{item}_분석결과.txt")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
                st.info("로그(Logs)를 확인하여 'API_KEY_INVALID' 여부를 다시 체크해주세요.")
