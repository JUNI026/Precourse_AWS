# -*- coding: utf-8 -*-
# =====================================================
# [체크포인트 · 단계 2] 차트 3종 완성 버전
# 사용법: 이 파일 내용을 generate_dashboard.py에 그대로 덮어쓰기
#  - 같은 폴더에 results.json, dashboard_template.html 필요
# 실행: python generate_dashboard.py   (mac은 python3)
# ★ 꾸미기는 index.html이 아니라 dashboard_template.html을 수정!
#   (index.html은 생성물이라 다음 실행 때 덮어써집니다)
# =====================================================
import json

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

html = html.replace("__STATUS_LABELS__", json.dumps(status_labels))
html = html.replace("__STATUS_DATA__", json.dumps(status_data))

# 4. 시간대별 데이터 삽입 (키를 시간 순서로 정렬)
hourly = results["hourly_counts"]
hourly_labels = sorted(hourly.keys())               # ["00", "01", ..., "23"]
hourly_data = [hourly[h] for h in hourly_labels]

html = html.replace("__HOURLY_LABELS__", json.dumps(hourly_labels))
html = html.replace("__HOURLY_DATA__", json.dumps(hourly_data))

# 5. 에러 URL TOP 5 데이터 삽입 ([URL, 횟수] 쌍을 두 리스트로 분리)
top_errors = results["top_error_urls"]
error_labels = [item[0] for item in top_errors]
error_data = [item[1] for item in top_errors]

html = html.replace("__ERROR_LABELS__", json.dumps(error_labels))
html = html.replace("__ERROR_DATA__", json.dumps(error_data))

# 6. 작성자 이름 삽입  ★ "본인 이름"을 실제 이름으로 바꾸세요
html = html.replace("__AUTHOR__", "본인 이름")

# 7. 완성본 저장
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html 생성 완료. 브라우저로 열어 확인하세요.")
