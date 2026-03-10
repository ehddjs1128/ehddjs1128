# 📊 표 이미지-마크다운 변환 엔진 최적화 기록 (Trial & Error)

본 프로젝트에서는 이미지 형태의 표 데이터를 마크다운 형식으로 자동 변환하기 위해 총 5가지의 기술적 접근과 실험을 진행했습니다.

## 🛠️ 전체 기술 스택

* **Deep Learning:** PyTorch, Transformers, Llama-3.2-Vision, TATR
* **OCR Engines:** EasyOCR, PaddleOCR
* **Library:** Docling, OpenCV, Surya (attempted)

---

## 🔄 단계별 시행착오 및 분석

### **1. Llama-3.2-Vision: Zero-shot OCR**

* **접근**: 멀티모달 LLM을 활용한 즉각적인 변환 시도.
* **결과**: 약 8.6초의 준수한 처리 속도.
* **한계**: **Context Length 제한**으로 인해 행(Row)이 많은 긴 표는 중간에 출력이 끊기는 현상 발생.

### **2. Docling & EasyOCR: 전문 문서 변환 도구 도입**

* **접근**: 표 구조 분석에 특화된 `Docling` 엔진 사용.
* **결과**: 구조 인식은 안정적이나, **한글 인식률**이 현저히 떨어짐.
* **한계**: 구분선과 글자가 밀접한 경우 텍스트 노이즈가 발생하고, 이를 보완하기 위해 도입한 `EasyOCR`의 한글 인식 성능도 실무 수준에 미치지 못함.

### **3. TATR + PaddleOCR: 하이브리드 전략 (실패)**

* **접근**: Microsoft의 **TATR**로 구조를 잡고, 한글에 강한 **PaddleOCR**로 텍스트를 추출하는 최상의 조합 기획.
* **문제**: **라이브러리 의존성 충돌**. `PyTorch`(TATR)와 `PaddlePaddle`(PaddleOCR) 간의 CUDA 환경 및 프레임워크 호환성 문제로 인해 가상환경 구축 단계에서 실패.
* **인사이트**: 성능도 중요하지만, 실제 배포 환경에서의 라이브러리 간 결합성(Interoperability)을 고려해야 함을 깨달음.

### **4. TATR + EasyOCR: 최적의 구조 인식 적용**

* **접근**: 프레임워크 충돌을 피하기 위해 `PyTorch` 기반의 TATR과 `EasyOCR`을 결합. (이미지 전처리 로직 포함)
* **결과**: TATR의 성능 덕분에 셀 단위 좌표 추출은 매우 정확했음.
* **한계**: **EasyOCR의 한계점 재확인**. 복잡한 숫자와 한글이 혼재된 표에서 여전히 낮은 정확도를 보임.

### **5. Surya: 최신 OCR 라이브러리 검토 (실패)**

* **접근**: 최근 각광받는 `Surya` 모델을 도입하여 인식률 개선 시도.
* **문제**: 최신 버전 업데이트로 인한 인터페이스 대폭 변경. 공식 문서와 실제 구현부의 괴리, 수많은 `Import Error` 및 런타임 오류로 인해 단기 구현 실패.

---

## 🎯 핵심 인사이트 (Retrospective)

1. **구조와 인식의 분리**: 표 변환은 '구조 분석(Table Structure Recognition)'과 '텍스트 인식(OCR)'이라는 두 가지 과제를 동시에 해결해야 함을 학습.
2. **한글 OCR의 난이도**: 영문과 달리 한글 및 복잡한 숫자 데이터는 전처리(Adaptive Thresholding, 2x Scaling)만으로는 해결되지 않는 고유의 인식 모델 성능이 중요함.
3. **환경 격리의 중요성**: 각기 다른 딥러닝 프레임워크를 혼합할 때 발생하는 의존성 문제를 경험하며, 추후 Microservice Architecture나 Docker 활용의 필요성을 절감함.
