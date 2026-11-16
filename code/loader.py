"""입력 — 키보드(모드 1)와 data.json 파일(모드 2)에서 격자를 읽는다."""

import json

DATA_PATH = "data.json"


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
    with open(path, encoding="utf-8") as f:
        return json.load(f)
