"""Mini NPU 시뮬레이터 — MAC 연산으로 Cross / X 패턴을 판정한다. (실행 파일)"""

from calc import mac, judge, normalize, avg_ms, print_benchmark, print_flat_compare
from loader import read_matrix, load_json


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
    print(f"연산 시간(평균/10회): {avg_ms(pattern, filter_a):.4f} ms")


def check_case(key, case, filters):
    """[8단계] 패턴 하나를 판정하고 (PASS 여부, 실패 사유) 를 돌려준다.

    키에서 N 꺼내기 → size_N 필터 고르기 → 크기 검증 → 점수 · 판정 · expected 비교.
    문제가 생겨도 예외로 멈추지 말고 (False, "사유") 로 돌려준다.
    """
    try:
        n = int(key.split("_")[1])
        pair = filters.get(f"size_{n}")
        if pair is None:
            return False, f"size_{n} 필터 없음"

        pattern = case["input"]
        if len(pattern) != n or len(pair["Cross"]) != n or len(pair["X"]) != n:
            return False, f"크기 불일치: N={n}, 패턴 {len(pattern)}, Cross {len(pair['Cross'])}, X {len(pair['X'])}"

        score_c = mac(pattern, pair["Cross"])
        score_x = mac(pattern, pair["X"])
        result = judge(score_c, score_x, "Cross", "X", "UNDECIDED")
        expected = normalize(case["expected"])
        ok = result == expected

        print(f"--- {key} ---")
        print(f"Cross 점수: {score_c}")
        print(f"X 점수: {score_x}")
        print(f"판정: {result} | expected: {expected} | {'PASS' if ok else 'FAIL'}")

        if ok:
            return True, ""
        if result == "UNDECIDED":
            return False, "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
        return False, f"판정 {result} ≠ expected {expected}"
    except Exception as e:
        return False, f"데이터 오류: {e}"


def mode_json():
    """[8단계] 필터 로드 → 패턴 판정 · PASS/FAIL → 성능(3·5·13·25) → [10단계] 결과 요약."""
    try:
        data = load_json()
    except (OSError, ValueError) as e:
        print(f"data.json 을 읽지 못했습니다: {e}")
        return

    print("\n# [1] 필터 로드")
    filters = {}
    for size, pair in data.get("filters", {}).items():
        filters[size] = {normalize(k): v for k, v in pair.items()}
        print(f"✓ {size} 필터 로드 완료 (Cross, X)")

    print("\n# [2] 패턴 분석 (라벨 정규화 적용)")
    fails = []
    patterns = data.get("patterns", {})
    for key, case in patterns.items():
        ok, reason = check_case(key, case, filters)
        if not ok:
            fails.append((key, reason))

    print("\n# [3] 성능 분석 (평균/10회)")
    print_benchmark([3, 5, 13, 25])

    print("\n# [3-1] 보너스: 2차원 vs 1차원 (같은 입력 · 평균/10회)")
    print_flat_compare([3, 5, 13, 25])

    print("\n# [4] 결과 요약")
    print(f"총 테스트: {len(patterns)}개")
    print(f"통과: {len(patterns) - len(fails)}개")
    print(f"실패: {len(fails)}개")
    if fails:
        print("\n실패 케이스:")
        for key, reason in fails:
            print(f"- {key}: {reason}")


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
