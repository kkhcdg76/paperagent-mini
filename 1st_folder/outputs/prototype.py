# react.py
import random

class React:
    def __init__(self):
        pass

    @staticmethod
    def select_action(input_problem):
        if "정보 검색" in input_problem:
            return "웹에서 정보를 검색합니다."
        else:
            return "기존 지식을 사용하여 추론합니다."

    @staticmethod
    def perform_action(action, input_problem):
        if action == "웹에서 정보를 검색합니다.":
            search_result = web_search(input_problem)
            return search_result
        else:
            return existing_knowledge_reasoning(input_problem)

    @staticmethod
    def reason_about_result(result_of_action):
        if "웹에서 정보를 검색합니다." in result_of_action:
            reasoning_process = f"검색한 정보를 바탕으로 문제를 해결합니다."
        else:
            reasoning_process = f"기존 지식을 바탕으로 문제를 해결합니다."
        
        return reasoning_process

    @staticmethod
    def react(input_problem):
        action = React.select_action(input_problem)
        result_of_action = React.perform_action(action, input_problem)
        reasoning_process = React.reason_about_result(result_of_action)
        return f"Action: {action}, Result: {result_of_action}, Reasoning: {reasoning_process}"

def web_search(problem):
    # 가짜 웹 검색 결과 생성
    search_results = ["5 + 7 = 12", "5 + 7 = 13"]
    return random.choice(search_results)

def existing_knowledge_reasoning(problem):
    # 기존 지식을 바탕으로 추론하는 가짜 함수
    if problem == "문제: 5 + 7 = ?":
        return "5 + 7 = 12"
    else:
        raise ValueError("기존 지식에 없는 문제입니다.")

# ars.py
class Ars:
    @staticmethod
    def evaluate_difficulty(input_problem):
        if "정보 검색" in input_problem:
            return 3
        else:
            return 1

    @staticmethod
    def monitor_confidence(difficulty_level, input_problem):
        if difficulty_level > 2 and "정보 검색" in input_problem:
            return "신뢰성 높음"
        else:
            return "신뢰성 낮음"

    @staticmethod
    def adjust_suppression(confidence_monitoring):
        if confidence_monitoring == "신뢰성 높음":
            return "억제 강화"
        else:
            return "억제 완화"

    @staticmethod
    def ars(input_problem):
        difficulty_level = Ars.evaluate_difficulty(input_problem)
        confidence_monitoring = Ars.monitor_confidence(difficulty_level, input_problem)
        dynamic_suppression_control = Ars.adjust_suppression(confidence_monitoring)
        return f"Difficulty Level: {difficulty_level}, Confidence Monitoring: {confidence_monitoring}, Suppression Control: {dynamic_suppression_control}"

# aft.py
import random

class Aft:
    @staticmethod
    def generate_cots(input_problem):
        positive_cots = ["5 + 7 = 12", "5 + 7 = 13"]
        negative_cots = ["5 + 7 = 10", "5 + 7 = 9"]
        
        return positive_cots, negative_cots

    @staticmethod
    def apply_constraints(positive_cots, negative_cots):
        for cot in positive_cots:
            if "5 + 7 = 12" == cot:
                return "양성 COT 점수 증가"
        
        return "제약 조건 적용 완료"

    @staticmethod
    def aft(input_problem):
        positive_cots, negative_cots = Aft.generate_cots(input_problem)
        constraint_application = Aft.apply_constraints(positive_cots, negative_cots)
        return f"Positive COTs: {positive_cots}, Negative COTs: {negative_cots}, Constraint Application: {constraint_application}"

if __name__ == "__main__":
    print("==================================================")
    print("         Paper2Prototype 실행 결과 시연           ")
    print("==================================================\n")
    
    # 정보 검색이 필요한 문제 테스트
    problem_search = "문제: 5 + 7 = ?, 정보 검색 필요"
    print(f"테스트 문제 1: '{problem_search}'")
    print("-" * 50)
    print("[ReAct 에이전트 결과]")
    print(React.react(problem_search))
    print("[ARS 에이전트 결과]")
    print(Ars.ars(problem_search))
    print("[AFT 에이전트 결과]")
    print(Aft.aft(problem_search))
    
    print("\n" + "=" * 50 + "\n")
    
    # 기존 지식을 사용하는 문제 테스트
    problem_knowledge = "문제: 5 + 7 = ?"
    print(f"테스트 문제 2: '{problem_knowledge}'")
    print("-" * 50)
    print("[ReAct 에이전트 결과]")
    print(React.react(problem_knowledge))
    print("[ARS 에이전트 결과]")
    print(Ars.ars(problem_knowledge))
    print("[AFT 에이전트 결과]")
    print(Aft.aft(problem_knowledge))
    print("==================================================")