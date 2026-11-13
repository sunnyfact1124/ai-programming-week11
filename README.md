# ai-programming-week11
2026100678 김태양
코드 작성에 Ai를 활용하여 제작되었습니다.

## 파일
성적CSV를 읽어 유효한 점수를 골라냅니다.
`load_scores.py`가 CSV 성적을 읽어 유효한 행과 건너뛴 행을 구분합니다.

## 실행 방법

CSV 파일은 첫 번째 행을 헤더로 사용하고, 각 데이터 행은 `이름,점수` 형식이어야 합니다.

```csv
name,score
Alice,88
Bob,100
```

프로젝트 폴더에서 CSV 파일 경로를 지정해 실행합니다.

```bash
python load_scores.py scores.csv
```

CSV 파일 경로를 생략하면 현재 폴더의 `scores.csv`를 읽습니다.

## 테스트 방법

pytest가 설치되어 있지 않다면 먼저 설치합니다.

```bash
python -m pip install pytest
```

프로젝트 폴더에서 테스트를 실행합니다.

```bash
python -m pytest -q
```
