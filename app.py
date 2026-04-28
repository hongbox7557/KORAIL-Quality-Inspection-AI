import streamlit as st
import google.generativeai as genai
import os

# 1. 페이지 설정
st.set_page_config(page_title="품질검사 지원 AI", layout="wide")

# 2. API 키 로드
api_key = os.environ.get("GEMINI_API_KEY")

# 상단 상태 표시줄
if not api_key:
    st.error("❌ Secrets에 'GEMINI_API_KEY'가 등록되지 않았습니다.")
    st.stop()

# 3. AI 모델 초기화 (에러 방지 로직 포함)
try:
    genai.configure(api_key=api_key)
    
    # 모델명 앞에 'models/'를 붙이는 것이 404 에러의 가장 확실한 해결책입니다.
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", 
        generation_config={
            "temperature": 0.2,
            "top_p": 0.95,
        },
        system_instruction="당신은 한국철도공사 품질검사 전문가입니다. 사규와 법령에 근거하여 답변하세요."
    )
    st.success("✅ 시스템 연결 성공 (모델: gemini-1.5-flash)")
except Exception as e:
    st.error(f"시스템 초기화 중 오류 발생: {e}")

# 4. UI 구성 (요청하신 4개 항목)
st.title("🔍 품질검사 지원 AI 시스템")
st.write("항목을 입력하고 분석 시작 버튼을 눌러주세요.")

with st.form("audit_form"):
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("1. 검사 대상 품목")
        reason = st.text_area("2. 검사 불합격 사유 (공사 입장)")
    with col2:
        claim = st.text_area("3. 협력사 주장 내용")
        goal = st.text_area("4. 현재 난항 지점 및 목표")
    
    submit = st.form_submit_button("⚖️ 규정 기반 분석 시작")

# 5. 실행 및 결과 도출
if submit:
    if not (item and reason and claim and goal):
        st.warning("모든 항목을 채워주세요.")
    else:
        with st.spinner("규정 분석 중..."):
            try:
                # 프롬프트 조립
                prompt = f"품목: {item}\n지적사유: {reason}\n업체주장: {claim}\n해결목표: {goal}\n\n위 내용에 대해 사규와 국가계약법 근거로 자문해줘."
                
                # 실제 생성 요청
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("---")
                    st.subheader("📋 분석 결과")
                    st.markdown(response.text)
                else:
                    st.error("AI가 빈 답변을 보냈습니다. 프롬프트를 확인해주세요.")
                    
            except Exception as e:
                st.error(f"결과 도출 중 오류 발생: {e}")
                st.info("로그(Logs) 창을 열어 상세 에러 메시지를 확인해주세요.")
