# Ollama 로컬 LLM 가이드

논문 분석 및 요약 작업을 로컬(무료)로 진행하기 위한 Ollama 모델 추천 및 설정 가이드입니다.

---

## 1. 모델 추천

| 모델명 | 파라미터 크기 | 권장 사양 | 특징 |
| :--- | :--- | :--- | :--- |
| **qwen2.5:7b** | 7B | RAM/VRAM 8GB 이상 | 한국어 요약 품질이 좋고 코딩 성능이 뛰어나 기본 모델로 추천합니다. |
| **llama3.1:8b** | 8B | RAM/VRAM 8GB 이상 | 메타의 범용 모델로 요약 능력이 준수합니다. |
| **deepseek-r1:8b** | 8B | RAM/VRAM 8GB 이상 | 추론(Thinking) 과정을 거치므로 논문 속 논리나 수식을 단계별로 뜯어볼 때 유용합니다. |

---

## 2. 컨텍스트 윈도우(Context Window) 설정

논문은 텍스트 길이가 매우 길기 때문에 Ollama의 기본 컨텍스트 설정(2,048 토큰)으로는 내용이 잘려 제대로 된 분석이 어렵습니다. 
원활한 분석을 위해 컨텍스트 크기를 최소 **32,768 (32k)** 이상으로 늘려주어야 합니다.

### 설정 방법 (Modelfile 빌드)
1. 프로젝트 폴더에 `Modelfile`을 만들고 아래 내용을 작성합니다.
   ```dockerfile
   FROM qwen2.5:7b
   PARAMETER num_ctx 32768
   ```
2. 터미널에서 아래 명령어로 커스텀 모델을 빌드합니다.
   ```bash
   ollama create qwen-paper -f Modelfile
   ```
3. 생성된 `qwen-paper`를 `.env` 파일의 `LLM_MODEL` 값에 기입하여 사용합니다.
