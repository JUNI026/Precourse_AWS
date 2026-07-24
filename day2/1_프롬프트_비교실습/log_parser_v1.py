# =====================================================
# 프롬프트 비교 실습 - 미션 1. 대충 요청해 보기 (1차 시도) 
# =====================================================
# 1) "로그 파싱하는 파이썬 코드 줘" 를 AI에게 그대로 보내세요.
# 2) AI가 준 코드를 아래에 붙여넣고 실행해 보세요.
#
# 실행 후 기록해 보기:
# - AI가 어떤 로그 형식을 가정했나?
# - 외부 라이브러리를 쓰라고 하지는 않았나?
# - 내가 원하는 값(IP, 시각, URL, 상태코드)이 나오나?

# TODO: AI가 준 코드를 여기에 붙여넣으세요.

"""
범용 로그 파싱 스크립트

일반적인 로그 포맷 예시:
2026-07-21 10:23:15 INFO Server started on port 8080
2026-07-21 10:23:16 ERROR Connection refused: 192.168.0.10

필요에 따라 LOG_PATTERN 정규식만 바꾸면 다른 포맷에도 재사용 가능합니다.
"""

import re
import csv
from pathlib import Path
from collections import Counter

# 로그 한 줄의 형식을 정의하는 정규식
# 그룹: 날짜(date), 시간(time), 로그레벨(level), 메시지(message)
LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<message>.*)$"
)


def parse_log_line(line: str) -> dict | None:
    """한 줄을 파싱해서 dict로 반환. 패턴이 안 맞으면 None."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    return match.groupdict()


def parse_log_file(file_path: str) -> list[dict]:
    """로그 파일 전체를 파싱해서 리스트로 반환."""
    parsed_entries = []
    unmatched_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            if not line.strip():
                continue
            entry = parse_log_line(line)
            if entry:
                entry["line_num"] = line_num
                parsed_entries.append(entry)
            else:
                unmatched_lines.append((line_num, line.strip()))

    if unmatched_lines:
        print(f"[경고] 패턴에 매칭되지 않은 줄 {len(unmatched_lines)}개:")
        for num, content in unmatched_lines[:5]:  # 최대 5개만 출력
            print(f"  줄 {num}: {content}")

    return parsed_entries


def summarize_by_level(entries: list[dict]) -> Counter:
    """로그 레벨별 개수 집계."""
    return Counter(entry["level"] for entry in entries)


def filter_by_level(entries: list[dict], level: str) -> list[dict]:
    """특정 레벨(예: ERROR)만 필터링."""
    return [e for e in entries if e["level"] == level.upper()]


def save_to_csv(entries: list[dict], output_path: str) -> None:
    """파싱 결과를 CSV로 저장."""
    if not entries:
        print("저장할 데이터가 없습니다.")
        return

    fieldnames = ["line_num", "date", "time", "level", "message"]
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)
    print(f"CSV 저장 완료: {output_path}")


if __name__ == "__main__":
    # 사용 예시
    sample_log_path = "sample.log"

    # 테스트용 샘플 로그 파일이 없으면 생성
    if not Path(sample_log_path).exists():
        sample_data = """2026-07-21 10:23:15 INFO Server started on port 8080
2026-07-21 10:23:16 ERROR Connection refused: 192.168.0.10
2026-07-21 10:23:17 WARNING High memory usage: 85%
2026-07-21 10:23:18 INFO Request processed in 120ms
2026-07-21 10:23:19 ERROR Timeout while connecting to DB
this is a malformed line without proper format
"""
        Path(sample_log_path).write_text(sample_data, encoding="utf-8")
        print(f"샘플 로그 파일 생성됨: {sample_log_path}")

    entries = parse_log_file(sample_log_path)
    print(f"\n총 {len(entries)}개의 로그 항목 파싱 완료\n")

    print("=== 레벨별 집계 ===")
    for level, count in summarize_by_level(entries).items():
        print(f"{level}: {count}건")

    print("\n=== ERROR 로그만 필터링 ===")
    for entry in filter_by_level(entries, "ERROR"):
        print(f"[{entry['date']} {entry['time']}] {entry['message']}")

    save_to_csv(entries, "parsed_log.csv")