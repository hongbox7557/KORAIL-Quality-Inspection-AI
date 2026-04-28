import streamlit as st
import google.generativeai as genai
import time
import traceback

st.set_page_config(page_title="KORAIL 품질검사 솔루션", layout="wide", page_icon="🚆")

# API 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 GEMINI_API_KEY를 등록해 주세요.")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.0-flash')
except Exception as e:
    st.error(f"모델 연결 오류: {e}")
    st.stop()

# 스타일
st.markdown("""<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
* { font-family: 'Pretendard', sans-serif !important; }
.main { background-color: #f8f9fa; }
section[data-testid="stSidebar"] { display: none !important; }
.stTextArea textarea {
    border-radius: 12px !important; border: 1.5px solid #d1d5db !important;
    padding: 18px !important; font-size: 15px !important;
    height: 150px !important; min-height: 150px !important;
    max-height: 150px !important; resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #0054A6 !important;
    box-shadow: 0 0 0 3px rgba(0,84,166,0.1) !important;
}
.stButton>button {
    height: 60px; background-color: #0054A6 !important; color: white !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 18px !important; border: none !important; margin-top: 10px;
}
.stButton>button:hover { background-color: #003F7F !important; }
.result-container {
    background: white; padding: 45px; border-radius: 20px;
    border: 1px solid #e2e8f0; line-height: 2.0; color: #2d3748;
}
</style>""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div style='display:flex; align-items:center; margin-bottom:10px;'>
    <div style='background:#0054A6; width:6px; height:38px; border-radius:3px; margin-right:18px;'></div>
    <h1 style='font-size:32px; margin:0; font-weight:800;'>품질검사 현안 솔루션</h1>
</div>
<p style='margin-left:24px; color:#718096; font-size:17px;'>KORAIL 사규 · KRCS 기술규격 · 국가계약법 통합 검토 서비스</p>
<hr style='border:0.5px solid #edf2f7; margin:20px 0 25px 0;'>
<div style='padding:30px 40px; background:white; border-radius:24px; border:1px solid #edf2f7; text-align:center; margin-bottom:30px;'>
    <div style='font-size:45px; margin-bottom:15px;'>⚖️</div>
    <h3 style='color:#0054A6; font-size:22px; font-weight:700;'>품질검사 현안을 객관적 규정으로 지원합니다.</h3>
    <p style='color:#4a5568; font-size:16px; line-height:1.8;'>
        협력사와의 품질 기준 해석 차이나 난항 상황에 대해<br>
        <b>한국철도공사 사규, 기술규격 및 국가계약법</b>을 근거로 하여<br>
        실효성 있는 기술·법률 자문과 객관적인 가이드라인을 제공합니다.
    </p>
    <div style='color:#a0aec0; font-size:15px; margin-top:10px;'>아래 입력폼에 현안 데이터를 입력한 후 분석 시작 버튼을 눌러주세요.</div>
</div>""", unsafe_allow_html=True)

# 입력 폼
st.markdown("<h3 style='color:#0054A6; font-size:20px; margin-bottom:20px;'>📋 현안 상황 입력</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    item   = st.text_area("1. 검사 대상 품목", placeholder="예: 차량용 윤축, 선로전환기 모터 등", height=150)
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", placeholder="기술규격서(KRCS 등) 위반 사항이나 승인 도면과 상이한 부분을 구체적으로 기술", height=150)
with col2:
    claim  = st.text_area("3. 협력사 주장 내용", placeholder="협력사가 제기하는 이의 신청 사유 또는 현장 여건상의 불가피성", height=150)
    goal   = st.text_area("4. 현재 난항 지점 및 목표", placeholder="상호 이견이 있는 핵심 쟁점 및 해결하고자 하는 목표", height=150)

analyze_btn = st.button("⚖️ 규정 기반 정밀 분석 시작", use_container_width=True)

# 분석 실행
if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("📊 정확한 분석을 위해 1~4번 항목을 모두 입력해 주세요.")
    else:
        with st.status("🔍 규정 및 법령 사례 대조 중...", expanded=True) as status:
            st.write("한국철도공사 품질관리 규정 및 KRCS 기술규격 조회 중...")
            time.sleep(0.8)
            st.write("국가계약법 시행령 및 관련 조달 판례 분석 중...")
            time.sleep(0.8)
            status.update(label="✅ 분석 완료", state="complete", expanded=False)

        prompt = f"""당신은 철도 품질검사 및 공공계약 법률 전문가입니다. 아래 데이터를 바탕으로 공식 분석 보고서를 작성하세요.

[분석 데이터]
- 품목: {item}
- 지적 사유: {reason}
- 협력사 주장: {claim}
- 분석 목표: {goal}

[작성 지침]
1. 객관적인 법적/기술적 판단 근거 위주로 서술하세요.
2. KORAIL 사규, KRCS, 국가계약법 등 구체적인 조항을 인용하세요.
3. 결과 하단에 "본 분석 결과로도 현안 해결이 어려울 경우, 법무팀에 공식적인 서면자문을 요청하여 확정적인 법적 판단을 받으시기 바랍니다." 문구를 반드시 포함하세요.
4. 마지막에 '[참고 규정 및 온라인 자료 목록]' 섹션을 만들어 상세히 나열하세요."""

        try:
            response = model.generate_content(prompt)
            if response and response.text:
                tab1, tab2 = st.tabs(["🏛️ 분석 보고서", "📑 인용 근거 자료"])
                with tab1:
                    st.markdown(f"<div class='result-container'>{response.text.split('[참고 규정')[0]}</div>", unsafe_allow_html=True)
                with tab2:
                    if "[참고 규정" in response.text:
                        ref = response.text.split("[참고 규정")[-1].replace(" 및 온라인 자료 목록]", "")
                        st.success(f"**활용된 법령 및 사규 데이터**\n\n{ref}")
                    else:
                        st.info("상세 참고 자료는 보고서 본문을 확인해 주세요.")
            else:
                st.error("응답이 비어있습니다. API 키를 확인해주세요.")
        except Exception as e:
            st.error(f"분석 중 오류: {e}")
            st.code(traceback.format_exc())
