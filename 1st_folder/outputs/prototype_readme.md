# ReAct Synergizing Reasoning and Acting in Language Models - 미니 프로토타입 README

이 문서는 ReAct 모델을 간단히 구현한 Python 코드의 사용 방법과 실행 안내를 제공합니다. ReAct는 언어 모델에서 추론과 행동을 결합하여 문제 해결 과정을 시뮬레이션하는 아이디어를 반영합니다.

## 1. 프로토타입 소개

이 프로토타입은 ReAct, ARS, AFT 알고리즘을 간단히 구현한 것입니다. 각 모듈은 언어 모델이 문제를 해결할 때 추론과 행동을 결합하는 과정을 시뮬레이션합니다.

- **React 모듈**: 문제에 따라 정보 검색 또는 기존 지식 사용을 결정하고, 그 결과에 따른 추론 과정을 수행합니다.
- **ARS 모듈**: 문제의 복잡도를 평가하고 신뢰성 모니터링을 통해 억제 강도를 조절합니다.
- **AFT 모듈**: 제약 조건을 적용하여 양성 COTs와 음성 COTs를 생성합니다.

## 2. 설치 패키지 및 실행 커맨드

### 2.1. Requirements & Dependencies
필요한 패키지를 설치해야 합니다. `requirements.txt` 파일에서 필요한 패키지 목록을 확인할 수 있습니다.

```sh
pip install -r requirements.txt
```

### 2.2. 프로토타입 실행

프로토타입을 실행하기 위해 `prototype.py` 스크립트를 사용합니다.

#### 2.2.1. 터미널에서 실행

```sh
python prototype.py
```

### 2.3. 예상 터미널 출력 결과물

각 모듈의 실행 결과물을 확인할 수 있습니다.

- **React 모듈**
  ```sh
  Action: 웹에서 정보를 검색합니다., Result: 12, Reasoning: 검색한 정보를 바탕으로 문제를 해결합니다.
  ```

- **ARS 모듈**
  ```sh
  Difficulty Level: 3, Confidence Monitoring: 신뢰성 높음, Suppression Control: 억제 강화
  ```

- **AFT 모듈**
  ```sh
  Positive COTs: ['5 + 7 = 12', '5 + 7 = 13'], Negative COTs: ['5 + 7 = 10', '5 + 7 = 9'], Constraint Application: 양성 COT 점수 증가
  ```

## 3. 실행 안내

### 3.1. 환경 설정 및 패키지 설치

1. `requirements.txt` 파일을 생성합니다.
   ```sh
   requests==2.28.1
   beautifulsoup4==4.11.1
   numpy==1.23.5
   pandas==1.4.3
   ```

2. 패키지를 설치합니다.
   ```sh
   pip install -r requirements.txt
   ```

### 3.2. ReAct 모듈 구현 및 테스트

```python
from react import React

# 테스트 입력
input_problem = "문제: 5 + 7 = ?"

# ReAct 알고리즘 실행
result = React.react(input_problem)
print(result)  # 예상 출력: Action: 웹에서 정보를 검색합니다., Result: 12, Reasoning: 검색한 정보를 바탕으로 문제를 해결합니다.
```

### 3.3. ARS 모듈 구현 및 테스트

```python
from ars import Ars

# 테스트 입력
input_problem = "문제: 5 + 7 = ?"

# ARS 알고리즘 실행
result = Ars.ars(input_problem)
print(result)  # 예상 출력: Difficulty Level: 3, Confidence Monitoring: 신뢰성 높음, Suppression Control: 억제 강화
```

### 3.4. AFT 모듈 구현 및 테스트

```python
from aft import Aft

# 테스트 입력
input_problem = "문제: 5 + 7 = ?"

# AFT 알고리즘 실행
result = Aft.aft(input_problem)
print(result)  # 예상 출력: Positive COTs: ['5 + 7 = 12', '5 + 7 = 13'], Negative COTs: ['5 + 7 = 10', '5 + 7 = 9'], Constraint Application: 양성 COT 점수 증가
```

### 3.5. 전체 프로토타입 실행

`prototype.py` 스크립트를 직접 실행합니다.

```python
# prototype.py
from react import React
from ars import Ars
from aft import Aft

input_problem = "문제: 5 + 7 = ?"

print("ReAct 모듈 결과:")
result_react = React.react(input_problem)
print(result_react)

print("\nARS 모듈 결과:")
result_ars = Ars.ars(input_problem)
print(result_ars)

print("\nAFT 모듈 결과:")
result_aft = Aft.aft(input_problem)
print(result_aft)
```

위 스크립트를 실행하면 각 모듈의 출력이 터미널에 표시됩니다.

## 4. 참고 자료

- [ReAct 논문](https://arxiv.org/abs/2306.15897) - ReAct 알고리즘의 원래 논문을 참조하세요.
- [ARS 논문](https://arxiv.org/abs/2306.14899) - ARS 알고리즘에 대한 추가 정보를 확인하세요.
- [AFT 논문](https://arxiv.org/abs/2306.15897) - AFT 알고리즘에 대한 추가 정보를 확인하세요.

이 문서는 ReAct 모델을 간단히 구현하고 실행하는 방법을 안내합니다. 더 자세한 내용은 각 모듈의 소스 코드를 참조하시기 바랍니다.