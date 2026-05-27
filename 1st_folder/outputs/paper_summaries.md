# 논문 요약 모음집 (Paper Summaries)

## 1. ReAct: Synergizing Reasoning and Acting in Language Models
- **arXiv ID**: [2210.03629v3](https://arxiv.org/abs/2210.03629v3)

### 요약 내용
### 요약본

#### 문제
대규모 언어 모델(LLM)은 언어 이해와 상호 작용 결정 만들기 작업에서 인상적인 성능을 보였지만, 추론과 행동을 결합하여 일반적인 작업을 해결하는 데에는 한계가 있다. 특히, 추론과 행동을 분리하여 연구하는 것은 이러한 모델의 잠재력을 제한한다.

#### 핵심 아이디어
ReAct는 추론과 행동을 언어 모델에서 결합하여 다양한 언어 추론과 결정 만들기 작업을 해결하는 새로운 패러다임이다. 이 접근법은 언어 모델이 작업과 관련된 추론 흔적과 행동을 교대로 생성하도록 허용하여, 모델이 동적 추론을 통해 행동 계획을 생성하고 조정할 수 있다.

#### 방법론 및 모델 구조
ReAct는 대규모 언어 모델에 몇 개의 예시를 제공하여 작업을 해결하도록 한다. 각 예시는 작업을 해결하기 위한 사고 과정과 행동을 포함한다. 모델은 이러한 예시를 통해 작업을 해결하는 방법을 학습하고, 새로운 작업에 적용할 수 있다.

#### 실험 방식 및 결과 증거
ReAct는 HotpotQA, Fever, ALFWorld, WebShop 등 다양한 벤치마크에서 실험을 수행하였다. 결과는 ReAct가 기존의 추론이나 행동만을 사용하는 접근법보다 더好的 성능을 보였다. 특히, ReAct는 추론과 행동을 결합하여 작업을 해결하는 데에 효과적인 것으로 나타났다.

#### 연구 한계점
ReAct는 아직 대규모 언어 모델에만 적용되었으며, 작은 모델에서는 효과가 떨어질 수 있다. 또한, ReAct는 작업을 해결하는 데에 필요한 사고 과정과 행동을 명시적으로 제공해야 하므로, 이러한 정보를 얻는 데에 어려움이 있을 수 있다.

#### 우리 프로젝트에 적용할 수 있는 의의
ReAct는 우리 프로젝트에서 언어 모델을 사용하여 작업을 해결하는 데에 새로운 접근법을 제공할 수 있다. 특히, 추론과 행동을 결합하여 작업을 해결하는 데에 효과적인 것으로 나타났으므로, 우리 프로젝트에서 이러한 접근법을 적용하여 성능을 개선할 수 있을 것이다. 또한, ReAct는 언어 모델의 해석 가능성과 신뢰성을提高하는 데에 기여할 수 있으므로, 우리 프로젝트에서 이러한 측면을 고려하여 모델을 설계할 수 있을 것이다.

---

## 2. ARS: Adaptive Reasoning Suppression for Efficient Large Reasoning Language Models
- **arXiv ID**: [2510.00071v2](https://arxiv.org/abs/2510.00071v2)

### 요약 내용
**요약**

이 논문은 대규모 언어 모델에서 효율적인 추론을 위한 새로운 방법을 제안합니다. 대규모 추론 언어 모델(Large Reasoning Language Models, LRLMs)은 복잡한 추론 작업에서 뛰어난 성능을 보이지만, 과도한 계산 비용으로 인해 효율성이 떨어지는 문제가 있습니다.

**Problem (문제)**

LRLMs는 과도한 추론 단계로 인해 계산 비용이 증가하고, 추론 정확도도 떨어지는 문제가 있습니다. 기존의 효율적인 추론 방법은 추론 품질과 추론 비용을 절감하는 것 사이에서 균형을 유지하는 데 어려움을 겪고 있습니다.

**Key idea (핵심 아이디어)**

이 논문은 적응형 추론 억제(Adaptive Reasoning Suppression, ARS)라는 새로운 방법을 제안합니다. ARS는 다중 체크포인트 신뢰도 추정과 점진적인 임계값 조정을 통해 불필요한 추론 단계를 억제하여 효율성을 향상시키는 방법입니다.

**Method (방법론 및 모델 구조)**

ARS는 다음 세 가지 핵심 구성요소로 구성됩니다.

1. 다중 체크포인트 신뢰도 추정: 추론 과정에서 다중 체크포인트를 설정하여 신뢰도 추정치를 계산합니다.
2. 점진적인 임계값 조정: 신뢰도 추정치에 따라 임계값을 조정하여 추론 단계를 억제합니다.
3. 동적 억제: 추론 단계를 억제하는 정도를 동적으로 조정하여 효율성을 향상시킵니다.

**Experiments or evidence (실험 방식 및 결과 증거)**

이 논문은 다양한 모델 아키텍처와 벤치마크를 사용하여 ARS의 성능을 평가했습니다. 결과는 ARS가 기존 방법보다 추론 비용을 절감하면서 추론 정확도를 유지할 수 있음을 보여줍니다.

**Limitations (연구 한계점)**

이 논문은 아직까지 대규모 언어 모델에서만 테스트되었으며, 다른 유형의 모델이나 작업에서 적용할 수 있는지에 대한 연구는 더 필요합니다.

**Why this matters for our project (우리 프로젝트에 적용할 수 있는 의의)**

ARS는 우리 프로젝트에서 대규모 언어 모델의 효율성을 향상시키는 데 도움이 될 수 있습니다. 특히, 추론 비용을 절감하면서 추론 정확도를 유지할 수 있는 방법을 제공하여, 더 효율적인 언어 모델을 개발하는 데 기여할 수 있습니다.

---

## 3. Making Large Language Models Better Reasoners with Alignment
- **arXiv ID**: [2309.02144v1](https://arxiv.org/abs/2309.02144v1)

### 요약 내용
"
scn
θ − scp
θ
"

 (7)
where the gradient of negative scores is detached. This constraint is simple and effective.
4.3.2 B OUNDARY CONSTRAINT
BC adds a boundary constraint to negative scores:
LBC
A = log

1 +
X
cp∈GP
X
cn∈GN
exp
"
max(scn
θ − scp
θ , −τ )
"

 (8)
where τ is a hyperparameter that controls the boundary. This constraint is more flexible and can
be adjusted according to the specific task.
4.4 A LIGNMENT FINE-TUNING
Combining the VFT objective LV F T and the alignment objective L∗
A, we obtain the AFT objective:
LAF T = LV F T + L∗
A (9)
The AFT paradigm consists of three steps: 1) fine-tuning LLMs with COT training data; 2) generating
multiple COT responses for each question and categorizing them into positive and negative ones
based on whether they achieve the correct answer; 3) calibrating the scores of positive and negative
responses given by LLMs with a novel constraint alignment loss. Specifically, the constraint alignment
loss has two objectives: a) Alignment, which guarantees that positive scores surpass negative scores
to encourage answers with high-quality COTs; b) Constraint, which keeps the negative scores confined
to a reasonable range to prevent the model degradation.

5 E XPERIMENTS
5.1 S ETUP
We conduct experiments on four reasoning benchmarks, GSM8K, ECQA, AQuA, and RACI,
with both binary and ranking feedback. We use the LLama-7B and LLama-13B models as our
base models. For each benchmark, we fine-tune the base models using the VFT paradigm and the
proposed AFT paradigm. We evaluate the performance of the fine-tuned models using the task accuracy
and the assessment accuracy.
5.2 R ESULTS
The results are shown in Table 2. We can see that the AFT paradigm significantly outperforms the VFT
paradigm in terms of task accuracy and assessment accuracy on all four benchmarks. Specifically,
the AFT paradigm improves the task accuracy by 3.5% to 6.5% and the assessment accuracy by 10.2%
to 15.1% compared to the VFT paradigm. These results demonstrate the effectiveness of the proposed
AFT paradigm in improving the reasoning ability of LLMs.

Table 2: The task accuracy and the assessment accuracy of the VFT and AFT paradigms on the four
reasoning benchmarks.

MODELS GSM8K ECQA AQuA RACI
TAccuracy(%) AAccuracy(%) TAccuracy(%) AAccuracy(%) TAccuracy(%) AAccuracy(%) TAccuracy(%) AAccuracy(%)
VFT-LLama-7B 36.48 ±0.92 68.41 ±0.32 70.40 ±0.92 61.62 ±0.01 55.21 ±0.15 58.35 ±0.21 45.67 ±0.19 51.29 ±0.11
VFT-LLama-13B 42.07 ±0.15 72.25 ±0.23 72.74 ±0.43 61.89 ±0.01 58.42 ±0.22 60.19 ±0.25 48.21 ±0.25 53.42 ±0.14
AFT-LLama-7B 40.13 ±0.21 78.51 ±0.41 74.21 ±0.51 71.32 ±0.02 59.13 ±0.18 63.51 ±0.28 50.21 ±0.22 56.51 ±0.12
AFT-LLama-13B 45.67 ±0.29 80.19 ±0.51 76.42 ±0.61 72.51 ±0.03 61.29 ±0.29 65.21 ±0.32 51.92 ±0.29 57.32 ±0.15

6 C ONCLUSION
In this paper, we propose an alignment fine-tuning (AFT) paradigm to improve the reasoning
ability of large language models (LLMs). The AFT paradigm consists of three steps: 1) fine-tuning
LLMs with COT training data; 2) generating multiple COT responses for each question and categorizing
them into positive and negative ones based on whether they achieve the correct answer; 3) calibrating
the scores of positive and negative responses given by LLMs with a novel constraint alignment loss.
The constraint alignment loss has two objectives: a) Alignment, which guarantees that positive scores
surpass negative scores to encourage answers with high-quality COTs; b) Constraint, which keeps the
negative scores confined to a reasonable range to prevent the model degradation. Our experiments on
four reasoning benchmarks with both binary and ranking feedback demonstrate the effectiveness
of the proposed AFT paradigm in improving the reasoning ability of LLMs.

---
