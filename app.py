import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 사용 가능한 모델 출력
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
