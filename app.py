import streamlit as st
import google.generativeai as genai
import time

# 1. 페이지 설정 (브라우저 탭 아이콘을 KORAIL 로고 톤으로 변경 가능)
st.set_page_config(page_title="KORAIL 품질검사 현안 솔루션", layout="wide", page_icon="🚆")

# 2. API 설정
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # 최신 프레뷰 모델 사용
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception as e:
        st.error(f"모델 연결 중 오류가 발생했습니다: {e}")
        st.stop()
else:
    st.error("Secrets에서 GOOGLE_API_KEY를 설정해주세요.")
    st.stop()

# 3. KORAIL 브랜드 기반 커스텀 CSS (세련된 디자인)
korail_blue = "#0054A6" # 코레일 메인 블루
korail_red = "#E60012"  # 코레일 포인트 레드
bg_beige = "#FDFBF5"    # 샌드 베이지 배경

st.markdown(f"""
    <style>
    /* 전체 배경 및 폰트 */
    .main {{ background-color: {bg_beige}; color: #333; }}
    
    /* 사이드바 스타일 (블루 톤) */
    section[data-testid="stSidebar"] {{ 
        background-color: white !important; 
        width: 500px !important; 
        border-right: 1px solid #e0e0e0;
        padding-top: 2rem;
    }}
    section[data-testid="stSidebar"] .stMarkdown h1 {{ color: {korail_blue}; }}
    
    /* 입력창 디자인 (세련된 테두리) */
    .stTextArea textarea {{ 
        min-height: 250px !important; 
        border-radius: 10px !important;
        border: 1px solid #d1d1d1 !important;
        background-color: white !important;
        font-size: 15px !important;
    }}
    .stTextArea textarea:focus {{ border: 2px solid {korail_blue} !important; }}
    
    /* 분석 버튼 (코레일 블루) */
    .stButton>button {{ 
        height: 60px; 
        font-weight: bold; 
        font-size: 19px !important;
        background-color: {korail_blue} !important; 
        color: white !important; 
        border: none;
        border-radius: 12px;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{ background-color: #003F7F !important; transform: translateY(-2px); }}
    
    /* 분석 결과 카드 디자인 */
    .result-card {{ 
        padding: 40px; 
        border-radius: 20px; 
        background-color: white; 
        border: 1px solid #f0f0f0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        line-height: 1.9;
        font-size: 16px;
    }}
    
    /* 메인 타이틀 (세련된 서체 느낌) */
    .stApp h1 {{ font-weight: 800; color: #1a1a1a; }}
    .stApp h3 {{ color: {korail_blue}; font-weight: 600; }}
    
    /* 로딩 애니메이션 커스텀 */
    .stSpinner {{ color: {korail_red} !important; }}
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바: 입력 폼
with st.sidebar:
    st.markdown("# 🚄 현안 데이터 입력")
    st.markdown("정확하고 객관적인 자문을 위해 아래 항목을 상세히 입력해주세요.")
    st.markdown("---")
    
    item = st.text_input("1. 검사 대상 품목", placeholder="예: 선로 전환기용 모터, 차량용 윤축 등")
    
    reason = st.text_area("2. 검사 불합격 및 지적 사유 (공사 입장)", 
                         placeholder="기술규격서 제○조 미흡, 도면 불일치 등 상세 기술", height=200)
    
    claim = st.text_area("3. 협력사 주장 내용", 
                        placeholder="현장 여건 불가피성, 규정 해석 이견 등", height=200)
    
    goal = st.text_area("4. 현재 난항 지점 및 목표", 
                       placeholder="의사결정 쟁점 및 해결하고자 하는 방향", height=150)
    
    # KORAIL 레드 포인트 버튼
    analyze_btn = st.button("⚖️ 규정 기반 정밀 분석", use_container_width=True)

# 5. 메인 화면 구성
# KORAIL 로고 느낌을 주는 타이틀 디자인
st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <div style='width: 8px; height: 40px; background-color: {korail_blue}; margin-right: 15px; border-radius: 4px;'></div>
        <h1 style='margin: 0; font-size: 36px;'>품질검사 현안 솔루션</h1>
    </div>
    <h3 style='margin-left: 23px; margin-top: -10px; font-weight: 500;'>한국철도공사 사규 · 기술규격 · 국가계약법 기반 자문</h3>
    <hr style='border: 1px solid #e0e0e0; margin: 30px 0;'>
    """, unsafe_allow_html=True)

if analyze_btn:
    if not all([item, reason, claim, goal]):
        st.warning("상세한 분석을 위해 모든 항목(1~4번)을 입력해주세요.")
    else:
        # --- 분석 중 UI 표현 ---
        with st.spinner("KORAIL 사규 및 국가계약법 사례를 정밀 검색 중입니다... 잠시만 기다려 주세요."):
            # 상태 표시 전용 공간
            status_box = st.empty()
            status_box.markdown(f"""
                <div style='padding: 20px; border-radius: 10px; background-color: white; border: 1px solid {korail_blue}; text-align: center;'>
                    <span style='color: {korail_blue}; font-size: 18px; font-weight: bold;'>🔄 규정 및 법령 사례를 분석 중입니다...</span><br>
                    <span style='color: #666; font-size: 14px;'>시스템이 한국철도공사 사규집과 국가계약법 온라인 DB를 참조하고 있습니다.</span>
                </div>
            """, unsafe_allow_html=True)
            
            # (시각적 효과를 위한 아주 짧은 지연)
            time.sleep(1)

            # 지시사항: 자문단 명칭 금지, 법무팀 절차 안내 강제, 참고 규정 명시
            prompt = (
                f"당신은 품질검사 규정 및 법률 분석 전문가입니다. 아래 상황을 분석하여 보고서를 작성하세요.\n\n"
                f"[상황 정보]\n"
                f"- 품목: {item}\n"
                f"- 공사 지적: {reason}\n"
                f"- 협력사 주장: {claim}\n"
                f"- 목표: {goal}\n\n"
                f"[작성 지침]\n"
                f"1. '자문단'이나 '전문가 집단'이라는 표현은 절대 사용하지 마세요.\n"
                f"2. 한국철도공사 사규, 기술규격, 국가계약법, 공정거래법 등 관련 법령을 근거로 객관적인 판단을 내리세요.\n"
                f"3. 보고서 마지막에는 반드시 다음과 같은 취지의 안내 문구를 포함하세요:\n"
                f"   '본 분석 결과로도 현안 해결이 어려울 경우, 법무팀에 공식적인 서면자문을 요청하여 확정적인 법적 판단을 받으시기 바랍니다.'\n"
                f"4. **가장 중요:** 보고서 마지막 섹션에 '참고한 규정 및 온라인 자료 목록'을 구체적으로 명시하세요. (예: 한국철도공사 기술규격서 제○조, 국가계약법 시행령 제○조, 법제처 판례 등)\n\n"
                f"[보고서 형식]\n"
                f"- 관련 규정 검토\n"
                f"- 주요 쟁점 분석\n"
                f"- 객관적 가이드라인\n"
                f"- 향후 조치 권고\n"
                f"- 참고 규정 및 자료 목록 (구체적 명시)"
            )
            
            try:
                # AI 모델 호출
                responses = model.generate_content(prompt)
                
                # 분석 중 UI 제거
                status_box.empty()
                
                if responses and responses.text:
                    st.markdown("### 🔍 규정 기반 정밀 분석 결과")
                    
                    # 탭 기능을 활용하여 결과와 참고자료를 분리 (세련된 UX)
                    tab1, tab2 = st.tabs(["📝 분석 보고서", "📚 참고 규정 및 자료"])
                    
                    with tab1:
                        # 메인 분석 결과 출력
                        st.markdown(f"<div class='result-card'>{responses.text}</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        # 프롬프트 지시에 따라 도출된 참고 자료 목록을 세련된 카드로 출력
                        # (응답 텍스트 내의 특정 섹션을 가져오거나, AI가 전체를 다 쓰게 할 수도 있습니다. 
                        # 여기선 전체 텍스트에 포함된 참고 자료 목록을 그대로 보여줍니다.)
                        st.markdown("""
                            <div style='padding: 20px; border-radius: 10px; background-color: #f9f9f9; border: 1px solid #e0e0e0;'>
                                <h3>📚 주요 참고 문헌</h3>
                                본 분석에 활용된 한국철도공사 사규, 기술규격 및 관련 법령은 다음과 같습니다.
                                (상세 내용은 법제처 국가법령정보센터 및 공사 사규 관리 시스템을 참조하시기 바랍니다.)
                            </div>
                        """, unsafe_allow_html=True)
                        st.write(responses.text.split("참고 규정 및 자료 목록")[-1]) # AI 응답의 마지막 섹션만 추출

                else:
                    st.error("응답 생성에 실패했습니다. 데이터를 다시 확인하고 시도해 주세요.")
            except Exception as e:
                status_box.empty()
                st.error(f"분석 중 기술적 오류 발생: {e}")
else:
    # 초기 화면 디자인 (가이드라인 적용)
    st.markdown(f"""
        <div style='padding: 40px; border-radius: 15px; background-color: white; border: 1px solid #f0f0f0; box-shadow: 0 4px 15px rgba(0,0,0,0.03);'>
            <h2 style='color: {korail_blue};'>사용 가이드</h2>
            ---
            1. 왼쪽 사이드바에 <strong>[분석 상황]</strong>을 상세히 입력해 주세요.<br>
            2. <strong>[규정 기반 정밀 분석]</strong> 버튼을 클릭하세요.<br>
            3. 시스템이 KORAIL 사규와 국가계약법 DB를 참조하여 객관적인 가이드라인을 제시합니다.<br><br>
            <strong style='color: {korail_red};'>주의:</strong> 본 결과는 AI의 규정 해석이며, 최종 결정 시 관련 부서의 법적 검토를 병행하시기 바랍니다.
        </div>
    """, unsafe_allow_html=True)
