import cv2
import numpy as np
import io
import os
from docling.document_converter import DocumentConverter, ImageFormatOption
from docling.datamodel.base_models import InputFormat, DocumentStream
from docling.datamodel.pipeline_options import PdfPipelineOptions

os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

def convert_table_to_markdown(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("이미지를 불러올 수 없습니다.")
        return

# 1. 과도한 이진화 대신 그레이스케일 및 대비 조정만 수행
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. 이미지 크기 확대 (OCR 인식률 향상을 위해 유지)
    resized = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    # 3. 선을 억지로 그리지 않고, 이미지 그대로 전달
    success, buffer = cv2.imencode(".png", resized)
    image_stream = io.BytesIO(buffer)
    doc_stream = DocumentStream(name="clean_table.png", stream=image_stream)

    # 4. Docling 설정 (Accurate 모드 유지)
    pipeline_options = PdfPipelineOptions()
    pipeline_options.table_structure_options.mode = "accurate"


    converter = DocumentConverter(
        format_options={InputFormat.IMAGE: ImageFormatOption(pipeline_options=pipeline_options)}
    )

    try:
        result = converter.convert(doc_stream)
        md_output = result.document.export_to_markdown()
        
        print("\n🚀 [V3] 선 강화 결과 🚀\n")
        print(md_output)
        
        with open("final_output_v3.md", "w", encoding="utf-8") as f:
            f.write(md_output)
            
    except Exception as e:
        print(f"오류 발생: {e}")

# 실행 (이미지 확장자 주의: .jpg 또는 .png)
convert_table_to_markdown("example_sheets_1.png")