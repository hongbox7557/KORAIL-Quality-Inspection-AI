import streamlit as st
import google.generativeai as genai
import os

# 페이지 설정
st.set_page_config(page_title="품질검사 AI", layout="centered")
st.title("🔍 품질검사 지원 시스템")

# 1. API 키 로드 (Secrets 이름 확인 필수: GEMINI_API_KEY)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# 2. AI 설정
try:
    genai.configure(api_key=api_key)
    # 모델명 앞에 'models/'를 붙여 경로를 명확히 지정합니다.
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction="당신은 한국철도공사 품질검사 전문가입니다."
    )
    st.success("✅ 시스템 준비 완료")
except Exception as e:
    st.error(f"연결 오류: {e}")

# 3. 입력창 (4개 항목)
with st.form("my_form"):
    c1, c2 = st.columns(2)
    with c1:
        item = st.text_input("1. 검사 품목")
        reason = st.text_area("2. 불합격 사유")
    with c2:
        claim = st.text_area("3. 협력사 주장")
        goal = st.text_area("4. 난항 및 목표")
    
    submit = st.form_submit_button("분석 시작")

# 4. 결과 출력
if submit:
    if item and reason and claim and goal:
        with st.spinner("분석 중..."):
            prompt = f"품목:{item}\n사유:{reason}\n주장:{claim}\n목표:{goal}\n\n위 상황을 사규 근거로 자문해줘."
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"도출 실패: {e}")
    else:
        st.warning("모든 칸을 채워주세요.")
