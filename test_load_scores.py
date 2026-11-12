import pytest

from load_scores import load_scores


def _write_csv(tmp_path, contents):
    csv_path = tmp_path / "scores.csv"
    csv_path.write_text(contents, encoding="utf-8")
    return csv_path


def test_정상적인_점수들을_읽는다(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "name,score\nAlice,88\nBob,100\nAlice,88\n",
    )

    kept, skipped = load_scores(csv_path)

    assert kept == [("Alice", 88), ("Bob", 100), ("Alice", 88)]
    assert skipped == []


def test_헤더만_있는_파일은_빈_결과를_돌려준다(tmp_path):
    csv_path = _write_csv(tmp_path, "name,score\n")

    assert load_scores(csv_path) == ([], [])


def test_빈_줄은_건너뛰고_건너뛴_기록에_포함하지_않는다(tmp_path):
    csv_path = _write_csv(tmp_path, "name,score\nAlice,90\n\nBob,80\n")

    kept, skipped = load_scores(csv_path)

    assert kept == [("Alice", 90), ("Bob", 80)]
    assert skipped == []


def test_파일이_없으면_FileNotFoundError가_발생한다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    "score, expected_valid",
    [
        (-1, False),
        (0, True),
        (1, True),
        (99, True),
        (100, True),
        (101, False),
    ],
)
def test_점수_경계값(tmp_path, score, expected_valid):
    csv_path = _write_csv(tmp_path, f"name,score\nTest,{score}\n")

    kept, _ = load_scores(csv_path)

    assert (len(kept) == 1) is expected_valid


@pytest.mark.parametrize(
    "row, expected_reason",
    [
        ("OnlyOneColumn", "열 개수가 2가 아님"),
        (",90", "이름이 비어 있음"),
        ("Alice,", "점수가 비어 있음"),
        ("Alice,absent", "점수가 정수가 아님"),
        ("Alice,101", "점수가 0~100 밖"),
    ],
)
def test_잘못된_행은_이유와_함께_건너뛴다(tmp_path, row, expected_reason):
    csv_path = _write_csv(tmp_path, f"name,score\n{row}\n")

    kept, skipped = load_scores(csv_path)

    assert kept == []
    assert skipped == [(2, row, expected_reason)]
