import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (브라우저 탭 제목 및 아이콘)
st.set_page_config(page_title="품질검사 법률/기술 자문 시스템", page_icon="⚖️")

# 2. API 설정 (Streamlit Secrets 사용)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 3. 메인 화면 헤더 및 설명
st.title("⚖️ 품질검사 현안 자문 시스템")
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
    item_name = st.text_input("1. 검사 대상 품목", placeholder="예: 객차용 제동패드")
    issue_reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", placeholder="규격서 제7조 미흡 등...")
    partner_claim = st.text_area("3. 협력사 주장 내용", placeholder="제조 공정상 불가피함 등...")
    goal = st.text_area("4. 현재 난항 지점 및 목표", placeholder="공정성 확보 및 납기 준수 방안 등...")
    
    submit_button = st.form_submit_button("규정 기반 분석 시작")

# 5. 분석 실행 및 결과 출력
if submit_button:
    if not (item_name and issue_reason and partner_claim and goal):
        st.warning("모든 항목을 입력해야 정확한 분석이 가능합니다.")
    else:
        # 프롬프트 구성 (AI에게 역할 부여)
        prompt = f"""
        당신은 한국철도공사(KORAIL)의 품질검사 및 법률 자문 전문가입니다. 
        다음 정보를 바탕으로 사규, 기술규격, 국가계약법에 근거하여 객관적인 가이드라인을 작성하세요.
        
        1. 대상 품목: {item_name}
        2. 공사 입장: {issue_reason}
        3. 협력사 주장: {partner_claim}
        4. 난항 지점 및 목표: {goal}
        
        [분석 요청 사항]
        - 관련 사규 및 법적 근거 제시
        - 양측 주장의 쟁점 분석
        - 향후 조치 방향에 대한 객관적 권고안
        """
        
        with st.spinner("규정을 분석 중입니다..."):
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("### 🔍 분석 결과")
                st.write(response.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
