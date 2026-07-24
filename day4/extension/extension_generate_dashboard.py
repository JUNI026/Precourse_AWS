# -*- coding: utf-8 -*-
# =====================================================
# 4일차 확장 미션 · 프로 대시보드 완성본
# 파일: generate_dashboard_pro.py
#  - 같은 폴더에 results.json, dashboard_template_pro.html 필요
#  - results.json에 top_ips 키가 있어야 합니다 (필수 단계 참고)
# 실행: python generate_dashboard_pro.py   (mac은 python3)
# =====================================================
import json
from datetime import datetime

# 1. 집계 결과 읽기
with open("results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

# 2. 템플릿 읽기
with open("dashboard_template_pro.html", "r", encoding="utf-8") as f:
    html = f.read()

# 3. 상태코드 (도넛 차트)
status_counts = results["status_counts"]
status_labels = sorted(status_counts.keys())            # 정렬해서 보기 좋게
status_data = [status_counts[c] for c in status_labels]
html = html.replace("__STATUS_LABELS__", json.dumps(status_labels))
html = html.replace("__STATUS_DATA__", json.dumps(status_data))

# 4. 시간대별 (선 차트)
hourly = results["hourly_counts"]
hourly_labels = sorted(hourly.keys())                   # ["00", ..., "23"]
hourly_data = [hourly[h] for h in hourly_labels]
html = html.replace("__HOURLY_LABELS__", json.dumps(hourly_labels))
html = html.replace("__HOURLY_DATA__", json.dumps(hourly_data))

# 5. 에러 URL TOP 5 (가로 막대)
top_errors = results["top_error_urls"]
error_labels = [item[0] for item in top_errors]
error_data = [item[1] for item in top_errors]
html = html.replace("__ERROR_LABELS__", json.dumps(error_labels))
html = html.replace("__ERROR_DATA__", json.dumps(error_data))

# 6. 의심 IP TOP 5 (가로 막대) — 필수 단계에서 results.json에 추가한 키
top_ips = results["top_ips"]
ip_labels = [item[0] for item in top_ips]
ip_data = [item[1] for item in top_ips]
html = html.replace("__IP_LABELS__", json.dumps(ip_labels))
html = html.replace("__IP_DATA__", json.dumps(ip_data))

# 7. 요약 숫자 카드: 전체 요청 수 / 에러 건수 / 에러율
total = sum(status_counts.values())
error_total = sum(cnt for code, cnt in status_counts.items() if int(code) >= 400)
error_rate = error_total / total * 100
html = html.replace("__TOTAL_COUNT__", f"{total:,}")
html = html.replace("__ERROR_COUNT__", f"{error_total:,}")
html = html.replace("__ERROR_RATE__", f"{error_rate:.2f}")

# 8. 경고 배지: 에러율이 기준치를 넘으면 표시
#    (이번 로그의 에러율은 4.55% — 기준 4%면 배지가 뜨고, 5%면 안 뜹니다.
#     기준을 바꿔 재실행하며 배지가 나타나고 사라지는 것을 확인해 보세요!)
THRESHOLD = 4.0
if error_rate > THRESHOLD:
    html = html.replace("__WARN_DISPLAY__", "block")
    html = html.replace("__WARN_TEXT__",
        f"경고: 에러율이 {error_rate:.2f}%로 기준치({THRESHOLD}%)를 초과했습니다")
else:
    html = html.replace("__WARN_DISPLAY__", "none")
    html = html.replace("__WARN_TEXT__", "")

# 9. 작성자 + 생성 시각
html = html.replace("__AUTHOR__", "본인 이름")
html = html.replace("__GENERATED_AT__", datetime.now().strftime("%Y-%m-%d %H:%M"))

# 10. 완성본 저장
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html 생성 완료. 브라우저로 열어 확인하세요.")
print(f"전체 {total:,}건 / 에러 {error_total:,}건 / 에러율 {error_rate:.2f}%")
