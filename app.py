import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="KORAIL 품질검사 자문 시스템", page_icon="⚖️")

# 2. API 및 시스템 프롬프트 설정
SYSTEM_INSTRUCTION = """
한국철도공사(KORAIL)의 품질검사 및 법률 자문 전문 AI입니다.
사용자의 현안에 대해 한국철도공사 사규, 기술규격(KRCS 등), 국가계약법 및 시행령을 근거로 답변해야 합니다.

[필수 준수 사항]
- 모든 분석 근거에는 반드시 구체적인 '법령 조항 번호'나 '사무분장/사규 명칭'을 명시할 것.
- 답변은 전문적이고 객관적인 문어체로 작성할 것.
- 5번 항목에는 분석에 활용된 실제 법령이나 사규의 명칭을 정확히 나열할 것.
"""

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    system_instruction=SYSTEM_INSTRUCTION
)

# 3. UI 구성
st.title("⚖️ KORAIL 품질검사 자문 시스템")
st.subheader("품질검사 현안을 객관적 규정으로 지원합니다.")

st.info("""
협력사와의 품질 기준 해석 차이나 난항 상황에 대해 **한국철도공사 사규, 기술규격 및 국가계약법**을 근거로 
기술·법률 자문과 객관적 가이드라인을 제공합니다.
""")

st.divider()

# 4. 분석 상황 입력 섹션
st.markdown("### 📝 분석 상황 입력")
st.caption("정확하고 객관적인 자문을 위해, 아래 4가지 항목에 상세한 내용을 입력해주세요.")

with st.form("inspection_form"):
    item_name = st.text_input("1. 검사 대상 품목", placeholder="예: 객차용 제동패드 등")
    issue_reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", placeholder="규격서 제7조 미흡 등")
    partner_claim = st.text_area("3. 협력사 주장 내용", placeholder="제조 공정상 불가피함 등")
    goal = st.text_area("4. 현재 난항 지점 및 목표", placeholder="공정성 확보 및 납기 준수 방안 등")
    
    submit_button = st.form_submit_button("규정 기반 분석 시작")

# 5. 분석 실행 및 결과 출력
if submit_button:
    if not (item_name and issue_reason and partner_claim and goal):
        st.warning("모든 항목을 입력해야 정확한 분석이 가능합니다.")
    else:
        # 4번 항목에 법무팀 서면 자문 요청 내용을 포함하도록 프롬프트 수정
        user_prompt = f"""
        다음 정보를 바탕으로 KORAIL 품질검사 자문 보고서를 작성하세요.
        
        1. 대상 품목: {item_name}
        2. 공사 입장: {issue_reason}
        3. 협력사 주장: {partner_claim}
        4. 현재 난항 및 목표: {goal}
        
        [작성 목차]
        1. 상황 요약 및 핵심 쟁점 분석
        2. 적용 규정 및 근거 제시 (반드시 관련 법령/사규의 구체적인 '조항 번호' 포함)
        3. 객관적 협의 방향 제시
        4. 해결을 위한 구체적인 조치
           - 현안 해결을 위한 실무적 단계별 조치 사항을 제시할 것.
           - 특히, **위의 조치로도 협의가 이루어지지 않거나 규정 해석의 쟁점이 해소되지 않을 경우, 사내 법무팀에 공식적인 서면 자문을 요청하여 법적 근거를 명확히 할 것**을 반드시 포함할 것.
        5. 참고한 규정 및 온라인 자료
        """
        
        with st.spinner("전문적인 규정 분석을 진행 중입니다..."):
            try:
                response = model.generate_content(user_prompt)
                st.markdown("---")
                st.markdown("### 🔍 품질검사 규정 자문 결과")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
                st.info("Tip: 만약 404 오류가 지속된다면 모델명을 'gemini-1.5-flash'로 변경해 보세요.")
