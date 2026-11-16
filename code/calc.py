"""계산 · 성능 — MAC 점수, 판정, 라벨 정규화, 연산 시간 측정."""

import time

EPS = 1e-9      # 두 점수 차이가 이보다 작으면 동점
REPEAT = 10     # 성능 측정 반복 횟수

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


# ---------------------------------------------------------------- 성능

def avg_ms(pattern, filt, repeat=REPEAT):
    """[9단계] mac() 을 repeat 번 돌린 평균 시간(ms). 연산 구간만 잰다."""
    # TODO: time.perf_counter() 로 앞뒤 시간 재기
    pass


def print_benchmark(sizes):
    """[9단계] 크기(N×N) / 평균 시간(ms) / 연산 횟수(N²) 표를 출력한다."""
    # TODO: 크기마다 n×n 행렬을 만들어 avg_ms() 호출
    pass
