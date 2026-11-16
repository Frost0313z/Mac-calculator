"""Mini NPU 시뮬레이터 — MAC 연산으로 Cross / X 패턴을 판정한다."""

import json
import time

EPS = 1e-9      # 두 점수 차이가 이보다 작으면 동점
REPEAT = 10     # 성능 측정 반복 횟수
DATA_PATH = "data.json"

# [6단계] 원래 라벨 → 표준 라벨(Cross / X) 표
LABELS = {
    "+": "Cross",
    "cross": "Cross",
    "x": "X",
}


# ---------------------------------------------------------------- 계산

def mac(pattern, filt): #맥 연산 실행하는 메서드
    total = 0.0
    n = len(pattern)
    for i in range (n):
      for j in range (n):
        total += pattern[i][j] * filt[i][j]
    return total

def judge(score_a, score_b, name_a="A", name_b="B", tie="판정 불가"): #맥 연산 판정하는 메서드
    """[3단계] 점수가 큰 쪽 이름을 돌려준다. 차이가 EPS 보다 작으면 tie."""
    if abs(score_a - score_b) < EPS:
      return tie
    if score_a > score_b:
      return name_a
    return name_b

def normalize(label):
    """[6단계] '+' · 'cross' → 'Cross', 'x' → 'X'. 모르는 라벨이면 None."""
    key = str(label).strip().lower()
    return LABELS.get(key)


# ---------------------------------------------------------------- 입력

def read_matrix(title, n=3): # 모드1 손으로 입력하는 거 예외처리하는 메서드
    """[4단계] n 줄을 입력받아 n×n 리스트로 돌려준다. 틀리면 그 줄을 다시 묻는다."""
    print(f"{title} ({n}줄 입력, 공백 구분)")
    rows = []
    while len(rows) < n:
      try:
        row = [float(v) for v in input().split() ]
        if len(row) != n:
          raise ValueError
        rows.append(row)
      except ValueError:
        print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
    return rows

    # TODO: input().split() → float 변환, 개수 검사, try/except ValueError


def load_json(path=DATA_PATH):
    """[7단계] data.json 을 읽어 dict 로 돌려준다."""
    # TODO: open(..., encoding="utf-8") + json.load
    pass


# ---------------------------------------------------------------- 성능

def avg_ms(pattern, filt, repeat=REPEAT):
    """[9단계] mac() 을 repeat 번 돌린 평균 시간(ms). 연산 구간만 잰다."""
    # TODO: time.perf_counter() 로 앞뒤 시간 재기
    pass


def print_benchmark(sizes):
    """[9단계] 크기(N×N) / 평균 시간(ms) / 연산 횟수(N²) 표를 출력한다."""
    # TODO: 크기마다 n×n 행렬을 만들어 avg_ms() 호출
    pass


# ---------------------------------------------------------------- 모드

def mode_user():
    """[5단계] 필터 A, B 입력 → 저장 확인 → 패턴 입력 → MAC → 판정 → 성능(3×3)."""
    print("\n# [1] 필터 입력")
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")
    print("✓ 필터 A, B 저장 완료")

    print("\n# [2] 패턴 입력")
    pattern = read_matrix("패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    result = judge(score_a, score_b)

    print("\n# [3] MAC 결과")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"판정: {result}")
    # TODO [9단계] 연산 시간(평균/10회) 출력


def check_case(key, case, filters):
    """[8단계] 패턴 하나를 판정하고 (PASS 여부, 실패 사유) 를 돌려준다.

    키에서 N 꺼내기 → size_N 필터 고르기 → 크기 검증 → 점수 · 판정 · expected 비교.
    문제가 생겨도 예외로 멈추지 말고 (False, "사유") 로 돌려준다.
    """
    # TODO
    pass


def mode_json():
    """[8단계] 필터 로드 → 패턴 판정 · PASS/FAIL → 성능(3·5·13·25) → [10단계] 결과 요약."""
    # TODO
    pass


# ---------------------------------------------------------------- 시작

def main(): #초기 모드 설정화면 세팅
    """[5단계] 제목과 모드 선택 메뉴를 보여주고 1 / 2 에 맞는 모드를 부른다."""
    print("=== Mini NPU Simulator ===")
    print("\n[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    while True:
        choice = input("선택: ").strip()
        if choice == "1":
            mode_user()
            return
        elif choice == "2":
            mode_json()
            return
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()
