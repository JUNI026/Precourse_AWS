# -*- coding: utf-8 -*-
# =====================================================
# [체크포인트] 3일차 단계 3까지의 완성 코드
# 막혔을 때: 이 파일 내용을 log_analyzer.py에 통째로 붙여넣고
#            다음 단계부터 이어서 진행하세요.
# =====================================================

# ---------- 단계 1. 파싱 ----------
def parse_line(line):
    """로그 한 줄에서 IP, 시각, 메서드, URL, 상태코드를 추출한다.
    형식에 맞지 않는 줄은 None을 반환한다."""
    line = line.strip()                 # 앞뒤 공백 / 줄바꿈 제거
    if line == "":                      # 빈 줄이므로 None 반환
        return None
    parts = line.split()                # 공백 기준으로 나눠서 parts라는 리스트에 저장
    if len(parts) < 9:                  # parts의 길이가 모자라면 깨진 줄 
        return None                     # 잘못된 결과이므로 None 반환
    try:
        status = int(parts[8])          # 상태코드를 정수로 변환
    except ValueError:                  # 숫자가 아니면 깨진 줄
        return None                     # 잘못된 결과이므로 None 반환
    return {
        "ip": parts[0],
        "time": parts[3].lstrip("[") + " " + parts[4].rstrip("]"),
        "method": parts[5].lstrip('"'),
        "url": parts[6],
        "status": status,
    }

entries = []          # 파싱에 성공한 딕셔너리들을 담는 리스트
skipped = 0           # 건너뛴(깨진) 줄 수
total_lines = 0       # 파일의 전체 줄 수

with open("access.log", "r", encoding="utf-8") as f:
    for raw in f:
        total_lines += 1
        entry = parse_line(raw)
        if entry is None:
            skipped += 1
        else:
            entries.append(entry)

print("=== 처음 5줄 파싱 결과 ===")
for e in entries[:5]:
    print(e)
print(f"\n전체 줄 수: {total_lines} / 건너뛴 줄 수: {skipped} / 파싱 성공: {len(entries)}")

# ---------- 단계 2. 상태코드별 집계 ----------
status_counts = {}
for entry in entries:
    code = str(entry["status"])                    # json 키로 쓰기 위해 문자열로
    status_counts[code] = status_counts.get(code, 0) + 1

print("\n=== 상태코드별 요청 수 ===")
for code in sorted(status_counts.keys()):
    print(f"{code}: {status_counts[code]}")
# 검산: 개수의 총합 == 전체 줄 수 - 건너뛴 줄 수
print(f"(검산) 집계 총합: {sum(status_counts.values())} == {total_lines - skipped}")

# ---------- 단계 3. 시간대별 집계 ----------
hourly_counts = {}
for entry in entries:
    hour = entry["time"].split(":")[1]             # "07/Jul/2026:14:23:45 ..." → "14"
    hourly_counts[hour] = hourly_counts.get(hour, 0) + 1

print("\n=== 시간대별 요청 수 ===")
for hour in sorted(hourly_counts.keys()):
    print(f"{hour}시: {hourly_counts[hour]}")
