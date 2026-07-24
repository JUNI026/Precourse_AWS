# -*- coding: utf-8 -*-
# =====================================================
# [체크포인트 · 단계 3] 의심 IP 차트까지 4종 완성 버전
# 사용법: 이 폴더의 두 파일(generate_dashboard.py, dashboard_template.html)을
#         day4 폴더에 복사해 둘 다 덮어쓰세요. (템플릿에 네 번째 차트가 들어 있습니다)
#  - 같은 폴더에 results.json 필요 (top_ips 키 포함 — 아래 안내 참고)
# 실행: python generate_dashboard.py   (mac은 python3)
# =====================================================
import json

# 1. 집계 결과 읽기
with open("results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

# top_ips 키 확인 (단계 3의 4-1에서 3일차 스크립트로 추가하는 키)
if "top_ips" not in results:
    raise SystemExit(
        "results.json에 top_ips 키가 없습니다.\n"
        "→ 방법 1: 실습 4-1의 코드를 3일차 log_analyzer.py에 추가하고 재실행해\n"
        "          results.json을 다시 만든 뒤 day4로 복사하세요.\n"
        "→ 방법 2: 배포된 results_예시.json의 이름을 results.json으로 바꿔 사용하세요."
    )

# 2. 템플릿 읽기
with open("dashboard_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 3. 상태코드 데이터 삽입
status_counts = results["status_counts"]
status_labels = list(status_counts.keys())
status_data = list(status_counts.values())

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

# 6. 의심 IP TOP 5 데이터 삽입 (top_error_urls와 같은 [IP, 횟수] 구조)
top_ips = results["top_ips"]
ip_labels = [item[0] for item in top_ips]
ip_data = [item[1] for item in top_ips]

html = html.replace("__IP_LABELS__", json.dumps(ip_labels))
html = html.replace("__IP_DATA__", json.dumps(ip_data))

# 7. 작성자 이름 삽입  ★ "본인 이름"을 실제 이름으로 바꾸세요
html = html.replace("__AUTHOR__", "본인 이름")

# 8. 완성본 저장
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html 생성 완료. 브라우저로 열어 확인하세요. (차트 4개)")
