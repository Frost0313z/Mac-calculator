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


# ---------------------------------------------------------------- 보너스: 1차원 최적화

def flatten(grid):
    """[보너스] n×n 2차원 리스트를 줄 순서대로 이어 길이 n² 의 1차원 리스트로 편다."""
    return [v for row in grid for v in row]


def mac_flat(a, b):
    """[보너스] 1차원으로 편 두 격자의 MAC. 인덱스 하나(k)로만 접근한다."""
    total = 0.0
    for k in range(len(a)):
        total += a[k] * b[k]
    return total


# ---------------------------------------------------------------- 성능

def avg_ms(pattern, filt, repeat=REPEAT, fn=mac):
    """[9단계] fn(기본 mac) 을 repeat 번 돌린 평균 시간(ms). 연산 구간만 잰다."""
    start = time.perf_counter()
    for _ in range(repeat):
        fn(pattern, filt)
    return (time.perf_counter() - start) / repeat * 1000


def print_benchmark(sizes):
    """[9단계] 크기(N×N) / 평균 시간(ms) / 연산 횟수(N²) 표를 출력한다."""
    print("크기      평균 시간(ms)    연산 횟수")
    print("-" * 37)
    for n in sizes:
        grid = [[1.0] * n for _ in range(n)]
        ms = avg_ms(grid, grid)
        print(f"{n}×{n}".ljust(10) + f"{ms:.4f}".ljust(17) + str(n * n))


def print_flat_compare(sizes):
    """[보너스] 같은 입력 · 같은 반복 횟수로 2차원 mac 과 1차원 mac_flat 의 평균 시간을 비교한다."""
    print("크기      2차원(ms)    1차원(ms)    빨라진 배수")
    print("-" * 46)
    for n in sizes:
        grid = [[1.0] * n for _ in range(n)]
        flat = flatten(grid)              # 펴는 시간은 측정 밖
        ms_2d = avg_ms(grid, grid)
        ms_1d = avg_ms(flat, flat, fn=mac_flat)
        print(f"{n}×{n}".ljust(10) + f"{ms_2d:.4f}".ljust(13) + f"{ms_1d:.4f}".ljust(13) + f"{ms_2d / ms_1d:.2f}배")
