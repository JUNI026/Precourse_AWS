# -*- coding: utf-8 -*-
# =====================================================
# 차트 만들기 실습 - generate_dashboard.py
#  - 같은 폴더에 results.json, dashboard_template.html 필요
# ★ 꾸미기는 index.html이 아니라 dashboard_template.html을 수정!
#   (index.html은 생성물이라 다음 실행 때 덮어써집니다)
# =====================================================
import json
from datetime import datetime


# 1. 집계 결과 읽기
with open("results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

# 2. 템플릿 읽기
with open("dashboard_template.html", "r", encoding="utf-8") as f:
    html = f.read()


# 3. 상태코드 데이터 삽입 (완성된 예시)
status_counts = results["status_counts"]
status_labels = list(status_counts.keys())          # 예: ["200", "301", ...]
status_data = list(status_counts.values())          # 예: [1523, 42, ...]
status_labels.sort()
status_data = [status_counts[label] for label in status_labels]

html = html.replace("__STATUS_LABELS__", json.dumps(status_labels))
html = html.replace("__STATUS_DATA__", json.dumps(status_data))

# 4. TODO: 시간대별 데이터 삽입
#    results["hourly_counts"] 를 시(hour) 순서로 정렬해
#    __HOURLY_LABELS__ 와 __HOURLY_DATA__ 를 치환하세요.

# 4. 시간대별 데이터 삽입
hourly_counts = results["hourly_counts"]

# 키(시간 문자열) 기준으로 정렬 -> [("00", 10), ("01", 9), ...]
sorted_hourly = sorted(hourly_counts.items(), key=lambda x: x[0])

hourly_labels = [hour for hour, count in sorted_hourly]   # ["00", "01", ..., "23"]
hourly_data = [count for hour, count in sorted_hourly]    # [10, 9, ..., 31]

html = html.replace("__HOURLY_LABELS__", json.dumps(hourly_labels))
html = html.replace("__HOURLY_DATA__", json.dumps(hourly_data))


# 5. TODO: 에러 URL TOP 5 데이터 삽입
#    results["top_error_urls"] 는 [URL, 횟수] 쌍의 리스트입니다.
#    URL 리스트와 횟수 리스트로 나눠
#    __ERROR_LABELS__ 와 __ERROR_DATA__ 를 치환하세요.

error_urls = results["top_error_urls"]
error_labels = [url for url, count in error_urls]   # URL 리스트
error_data = [count for url, count in error_urls]   # 횟수 리스트

html = html.replace("__ERROR_LABELS__", json.dumps(error_labels))
html = html.replace("__ERROR_DATA__", json.dumps(error_data))


# 5.5 TODO: 의심 IP TOP 5 데이터 삽입
suspicious_ips = results["top_ips"]
suspicious_ip_labels = [ip for ip, count in suspicious_ips]   # IP
suspicious_ip_data = [count for ip, count in suspicious_ips]   # 횟수

html = html.replace("__SUSPICIOUS_IP_LABELS__", json.dumps(suspicious_ip_labels))
html = html.replace("__SUSPICIOUS_IP_DATA__", json.dumps(suspicious_ip_data))


# 5-5-2 전체 이용 횟수 및 에러 건수

total = sum(status_counts.values())
error_total = sum(cnt for code, cnt in status_counts.items() if int(code)>=400)
error_percent = results["error_rate_percent"]
html = html.replace("__ERROR_RATE__", f"{error_percent:.2f}%")  # 소수점 2자리
html = html.replace("__TOTAL_COUNT__", f"{total:,}")  # 천 단위 구분 쉼표
html = html.replace("__ERROR_COUNT__", f"{error_total:,}")
html = html.replace("__GENERATED_AT__", datetime.now().strftime("%Y-%m-%d %H:%M"))


# 6. 작성자 이름 삽입 
html = html.replace("__AUTHOR__", "JUN")

# 7. 완성본 저장
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html 생성 완료. 브라우저로 열어 확인하세요.")
