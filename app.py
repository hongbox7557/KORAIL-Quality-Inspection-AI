import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="품질검사 지원 AI", layout="wide")

# 1. API 키 로드
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Secrets에서 'GEMINI_API_KEY'를 찾을 수 없습니다.")
    st.stop()

# 2. 시스템 초기화 및 모델 연결
try:
    genai.configure(api_key=api_key)
    
    # 404 에러 방지를 위한 'models/' 경로 명시
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        generation_config={"temperature": 0.2, "top_p": 0.95},
        system_instruction="당신은 한국철도공사 품질검사 전문가입니다. 사규와 법령에 근거하여 답변하세요."
    )
    st.success("✅ 시스템 연결 성공 (Gemini 1.5 Flash)")
except Exception as e:
    st.error(f"⚠️ 시스템 초기화 오류: {e}")

# 3. 품질검사 입력 UI (4가지 항목)
st.title("🔍 품질검사 지원 AI 시스템")
with st.form("audit_form"):
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("1. 검사 대상 품목")
        reason = st.text_area("2. 검사 불합격 사유 (공사 입장)")
    with col2:
        claim = st.text_area("3. 협력사 주장 내용")
        goal = st.text_area("4. 현재 난항 지점 및 목표")
    
    submit = st.form_submit_button("⚖️ 규정 기반 분석 시작")

# 4. 분석 실행
if submit:
    if not (item and reason and claim and goal):
        st.warning("모든 항목을 입력해주세요.")
    else:
        with st.spinner("규정 분석 중..."):
            try:
                prompt = f"품목: {item}\n지적사유: {reason}\n업체주장: {claim}\n해결목표: {goal}\n\n위 내용에 대해 객관적으로 자문해줘."
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("📋 분석 결과")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"결과 도출 실패: {e}")
                st.info("💡 팁: 모델명에 'models/'가 포함되었는지, requirements.txt에 버전이 명시되었는지 확인하세요.")
