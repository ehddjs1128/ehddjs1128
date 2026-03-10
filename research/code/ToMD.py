import base64
import ollama
from openai import OpenAI

# Llama-3.2-Vision을 사용하는 방식 (무료임)
# ollama 설치(1.2G) 후 ollama run llama3.2-vision 을 'cmd'에 입력하여 모델 다운(7.8G) 필요 

client = OpenAI(base_url='http://localhost:11434/v1',
                api_key='ollama',) # 로컬 Ollama 서버 주소로 설정

# 표나 이미지를 받을 때 이미지파일로 받는다
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def transform_table_to_markdown(image_path):
    # 1. 이미지 로드
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except FileNotFoundError:
        return "에러: 이미지 파일을 찾을 수 없습니다."

    # 2. 시스템 프롬프트 (전체 표 처리용으로 소폭 수정)
    # 행 단위가 아닌 "전체 표"를 마크다운으로 변환하도록 지시합니다.
    prompt = (
        "You are a specialized OCR tool for table structure analysis. "
        "Convert the entire table in the image into a single Markdown table. "
        "FOLLOW THESE RULES STRICTLY:\n"
        "1. Output ONLY the markdown table code.\n"
        "2. DO NOT guess or hallucinate text. If a character is illegible, use '[?]'.\n"
        "3. For merged cells: In Markdown, use empty cells '| |' for horizontal merges "
        "or repeat the value/use '[^]' for vertical merges to maintain structure.\n"
        "4. Maintain the exact column and row count as seen in the image.\n"
        "5. Do not include any introductory or concluding remarks."
    )

    # 3. Llama-3.2-Vision 모델 호출
    try:
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_data]
            }],
            options={
                'temperature': 0,
                'num_predict': 2048,  # 응답이 끊기지 않도록 출력 토큰 제한을 늘림
            }
        )
        return response['message']['content']
    except Exception as e:
        return f"모델 호출 중 오류 발생: {str(e)}"
    
table_md = transform_table_to_markdown("example_sheets_1.png")
print(table_md)
