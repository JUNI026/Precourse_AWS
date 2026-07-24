# =====================================================
# 로그 분석 만들기 실습 - log_analyzer.py
# =====================================================
# 오늘의 미션: 아래 4단계를 순서대로 완성하세요.
# access.log를 파싱해 상태코드별/시간대별/에러 URL 통계를 내고
# results.json으로 저장합니다. (내일 대시보드에서 사용)

# ❗단계마다 commit 합니다.
# - 터미널로 commit 한다면
#    git add . 
#    git commit -m "precourse day3: 단계N ... 완료"
# - vscode로 commit 한다면
#    코드 저장(ctrl + s) -> 소스 컨트롤 탭 누르기 -> 파일 stage 올리기 -> 커밋 메세지 작성 -> 커밋 버튼

# --- 단계 1. 파싱 ---
# 요구사항
#   - access.log를 한 줄씩 읽는다
#   - 각 줄에서 IP, 시각 문자열, HTTP 메서드, URL, 상태코드(정수)를 추출한다
#   - 확인용으로 처음 5줄의 추출 결과를 출력한다
#   - 마지막에 전체 줄 수를 출력한다 (단계 2의 검산에 사용)
# ⚠️ 이 로그에는 형식이 깨진 줄이 섞여 있습니다! IndexError/ValueError가 나면
#    2일차처럼 에러 메시지를 AI에게 전달하고, 깨진 줄은 건너뛰고
#    건너뛴 줄 수를 출력하도록 수정을 요청하세요.
# 🏁 처음 5줄의 파싱 결과와 건너뛴 줄 수가 출력되면 성공!

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기

"""
로그 분석 실습 - 1단계
access.log 파일을 한 줄씩 읽어서 IP, 시각, HTTP 메서드, URL, 상태코드를 추출한다.

로그 예시:
203.0.113.45 - - [07/Jul/2026:14:23:45 +0900] "GET /products/list HTTP/1.1" 200 5321
"""

from fileinput import filename
from typing import Optional
import re
import os
import json

# 로그 한 줄을 매칭하기 위한 정규표현식
# 그룹 1: IP 주소
# 그룹 2: 시각 (대괄호 안의 문자열)
# 그룹 3: HTTP 메서드
# 그룹 4: 요청 URL
# 그룹 5: 상태 코드

LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+'      # IP 주소 (예: 203.0.113.45)
    r'-\s+-\s+'                                # 사용하지 않는 필드 2개 (- -)
    r'\[(?P<time>[^\]]+)\]\s+'                 # [07/Jul/2026:14:23:45 +0900]
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+HTTP/[\d.]+"\s+'  # "GET /products/list HTTP/1.1"
    r'(?P<status>\d{3})'                       # 상태 코드 (예: 200)
)


def parse_line(line: str) -> Optional[dict]:
    """
    로그 한 줄을 받아서 필요한 정보를 딕셔너리로 반환한다.
    형식에 맞지 않는 줄이면 None을 반환한다.
    """
    match = LOG_PATTERN.search(line)
    if not match:
        return None

    return {
        "ip": match.group("ip"),
        "time": match.group("time"),
        "method": match.group("method"),
        "url": match.group("url"),
        "status": match.group("status"),
    }

def count_status_codes(status_counts: dict, status: str) -> None:
    """
    status_counts 딕셔너리에 상태코드 등장 횟수를 누적한다.
    - 처음 등장한 상태코드면 0에서 시작해서 1을 더한다.
    - 이미 있던 상태코드면 기존 값에 1을 더한다.
    딕셔너리는 참조로 전달되므로, 함수 안에서 수정하면 원본도 바뀐다 (반환값 없음).
    """
    status_counts[status] = status_counts.get(status, 0) + 1
 
 
def print_status_summary(status_counts: dict, success_count: int) -> None:
    """
    상태코드별 집계 결과를 보기 좋게 출력하고,
    합계가 파싱 성공 줄 수와 일치하는지 확인해서 알려준다.
    """
    print("\n== 상태 코드별 요청 수 ==")
 
    # 상태코드(문자열)를 기준으로 정렬해서 출력 (200, 301, 404, 500 순서)
    for status in sorted(status_counts.keys()):
        count = status_counts[status]
        print(f"{status} : {count}개")
 
    total_by_status = sum(status_counts.values())
 
    print()
    if total_by_status == success_count:
        print(f"일치 (상태코드별 합계 {total_by_status} == 파싱 성공 수 {success_count})")
    else:
        print(f"불일치 (상태코드별 합계 {total_by_status} != 파싱 성공 수 {success_count})")


def main():
    # 이 스크립트 파일이 있는 폴더를 기준으로 access.log 경로를 만든다
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, "access.log")

    total_lines = 0     # 전체 읽은 줄 수
    success_count = 0   # 파싱 성공한 줄 수
    fail_count = 0       # 파싱 실패(건너뜀)한 줄 수
    preview_count = 0    # 미리보기로 출력한 줄 수
    status_counts = {}   # 상태코드별 개수를 저장할 딕셔너리
    hourly_counts = {f"{h:02d}": 0 for h in range(24)}
    error_url_counts = {}  # 에러(400+) 상태코드의 URL별 개수를 저장할 딕셔너리
    ip_counts = {}         # IP별 요청 개수를 저장할 딕셔너리
    method_counts = {}     # HTTP 메서드별 요청 개수를 저장할 딕셔너리

    print("== 처음 5줄 파싱 ==")

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            total_lines += 1
            result = parse_line(line)

            # 파싱 성공/실패 카운트
            if result is not None:
                success_count += 1
                count_status_codes(status_counts, result["status"])

                hour = extract_hour(result["time"])
                if hour is not None:
                    count_hourly(hourly_counts, hour)

                # 4단계: 400 이상 상태코드만 URL별로 집계
                count_error_url(error_url_counts, result["status"], result["url"])
                count_ip(ip_counts, result["ip"])
                count_method(method_counts, result["method"])
            else:
                fail_count += 1

            # 확인용으로 첫 5줄의 파싱 결과만 출력
            if preview_count < 5:
                print(result, "\n")
                preview_count += 1

    # 최종 통계 출력
    print("== 결과 요약 ==")
    print(f"전체 읽은 줄 수: {total_lines}")
    print(f"파싱 성공 줄 수: {success_count}")
    print(f"건너뛴 줄 수: {fail_count}")

    # 2단계: 상태코드별 집계 출력
    print_status_summary(status_counts, success_count)

    # 3단계: 시간대별 집계 출력
    print_hourly_summary(hourly_counts)

    # 4단계: 에러 최다 URL TOP 5 출력 (반환값으로 정렬된 리스트를 받음)
    top5_urls = print_top_error_urls(error_url_counts, top_n=5)
    top_error_urls = [list(t) for t in top5_urls]

    # 5단계: 요청 최다 IP TOP 5 출력
    top5_ips = print_top_ips(ip_counts, top_n=5)
    top_ips = [list(t) for t in top5_ips]

    # 5단계: 메서드별 집계 출력
    print_method_summary(method_counts)

    # 5단계: 에러율 계산 및 출력
    error_count = sum(error_url_counts.values())
    print_error_rate(error_count, success_count)

    # 상태코드별 집계, 시간대별 집계, 에러 TOP5를 하나의 딕셔너리로 묶어서 저장
    results = {
        "status_counts": status_counts,
        "hourly_counts": hourly_counts,
        "top_error_urls": top_error_urls,
        "top_ips": top_ips,
        "method_counts": method_counts,
        "error_rate_percent": round(calculate_error_rate(error_count, success_count), 2),
    }
    output_path = os.path.join(base_dir, "results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        # ensure_ascii=False : 한글/특수문자가 유니코드 이스케이프(\uXXXX)로 깨져 보이지 않게 함
        # indent=2 : 사람이 보기 좋게 들여쓰기
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nresults.json 저장 완료: {output_path}")


# --- 단계 2. 상태코드별 집계 ---
# 요구사항: 전체 로그의 상태코드별 요청 수를 집계해 출력한다
# 🤔 힌트: 1일차의 딕셔너리 카운팅 패턴
#   status_counts[code] = status_counts.get(code, 0) + 1
# 기대 출력 형식
#   === 상태코드별 요청 수 ===
#   200: 1523
#   404: 87
# 🏁 개수의 총합이 (전체 줄 수 - 건너뛴 줄 수)와 일치하면 성공!

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기

    # 2단계: 상태코드별 집계 출력

    print_status_summary(status_counts, success_count)
    print_hourly_summary(hourly_counts)
    print_top_error_urls(error_url_counts, top_n=5)



# # --- 단계 3. 시간대별 집계 ---
# 요구사항: 시각 문자열에서 시(hour)만 추출해 0~23시 요청 수를 집계해 출력한다
# 🤔 힌트: "07/Jul/2026:14:23:45 +0900" 을 콜론(:)으로 자르면 두 번째 파트가 시
#   hour = time_str.split(":")[1]     # "14"
#   정렬 출력: for hour in sorted(hourly_counts.keys()): ...
#   변수 이름은 hourly_counts 로 해주세요. (마무리의 json 저장에서 사용합니다)
#   시(hour)를 int()로 바꾸지 마세요. "00" 같은 두 자리 문자열이어야 내일 대시보드와 연결됩니다.
# 기대 출력 형식
#   === 시간대별 요청 수 ===
#   00시: 12
#   ...
#   23시: 31
# 🏁 0~23시 순서대로 정렬되어 출력되면 성공!

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기

def extract_hour(time_str: str) -> Optional[str]:
    """
    "07/Jul/2026:14:23:45 +0900" 형태의 문자열에서 시(Hour) 부분만 뽑아 "14"처럼 반환한다.
    ':' 기준으로 나누면 인덱스 1번이 시(Hour)에 해당한다.
    형식이 이상해서 시를 뽑을 수 없으면 None을 반환한다.
    """
    parts = time_str.split(":")
    if len(parts) < 2:
        return None
 
    hour = parts[1]
    if not hour.isdigit():
        return None
 
    return hour
 
 
def count_hourly(hourly_counts: dict, hour: str) -> None:
    """
    hourly_counts 딕셔너리에 시간대별 등장 횟수를 누적한다.
    hourly_counts는 미리 "00" ~ "23" 키로 0 초기화되어 있다고 가정한다.
    """
    hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
 
 
def print_hourly_summary(hourly_counts: dict) -> None:
    """
    시간대별(00~23시) 집계 결과를 정수 순서대로 정렬해서 출력한다.
    """
    print("\n== 시간대 별 요청 수 ==")
 
    # 키가 문자열("00", "01", ...)이므로 int로 변환해서 정렬 기준으로 사용
    for hour in sorted(hourly_counts.keys(), key=int):
        count = hourly_counts[hour]
        print(f"{hour}시 : {count}개")


# --- 단계 4. 에러 URL TOP 5 ---
# 요구사항
#   - 상태코드가 400 이상인 요청만 대상으로 URL별 발생 횟수를 집계한다
#   - 발생 횟수가 많은 순서로 상위 5개를 출력한다
# 🤔 힌트: 값 기준 내림차순 정렬 후 상위 5개 자르기
#   top5 = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
#   for rank, (url, cnt) in enumerate(top5, start=1):
#       print(f"{rank}위: {url} ({cnt}회)")
#   lambda가 낯설다면 AI에게 이 두 줄의 동작 설명을 요청해 보세요.
# 기대 출력 형식
#   === 에러 최다 URL TOP 5 ===
#   1위: /api/payment (37회)
# 🏁 에러 URL 상위 5개가 횟수와 함께 출력되면 성공!
# ⚠️ 출력까지 끝났다면, 마무리의 json 저장에서 쓸 수 있도록
#    아래 한 줄을 추가해 top_error_urls 변수를 만들어 두세요.
#   top_error_urls = [list(t) for t in top5]   # [[URL, 횟수], ...] 형태

# TODO: AI에게 받은 코드를 검증 후 여기에 붙여넣기

def count_error_url(error_url_counts: dict, status: str, url: str) -> None:
    """
    상태코드가 400 이상인 요청에 한해 URL별 발생 횟수를 누적한다.
    status는 문자열이므로 반드시 int()로 변환한 뒤 크기 비교해야 한다.
    (문자열끼리 비교하면 "9" > "400" 처럼 자릿수 때문에 잘못된 결과가 나올 수 있다)
    """
    if int(status) >= 400:
        error_url_counts[url] = error_url_counts.get(url, 0) + 1
 
 
def print_top_error_urls(error_url_counts: dict, top_n: int = 5) -> None:
    """
    에러(400 이상) 발생 횟수가 많은 URL을 상위 top_n개까지 순위와 함께 출력한다.
    """
    print("\n== 에러 최다 URL TOP 5 ==")
 
    # error_url_counts.items() -> [(url, count), (url, count), ...] 형태의 리스트
    # key=lambda item: item[1] : 각 튜플(item)에서 두 번째 값(count)을 정렬 기준으로 사용
    # reverse=True : 개수가 많은 순서(내림차순)로 정렬
    sorted_urls = sorted(error_url_counts.items(), key=lambda item: item[1], reverse=True)
 
    top_urls = sorted_urls[:top_n]  # 상위 top_n개만 잘라냄
 
    for rank, (url, count) in enumerate(top_urls, start=1):
        print(f"{rank}위: {url} ({count}회)")





# --- 마무리. 결과를 results.json으로 저장 ---
# 단계 4까지 완성한 뒤, 아래 주석을 해제하세요.
# ★ 키 이름(status_counts / hourly_counts / top_error_urls)은
#   한 글자도 바꾸지 마세요. 내일 대시보드와 연결되는 이름입니다.


def print_top_error_urls(error_url_counts: dict, top_n: int = 5) -> list:
    """
    에러(400 이상) 발생 횟수가 많은 URL을 상위 top_n개까지 순위와 함께 출력한다.
    이후 JSON 저장 등에서 재사용할 수 있도록 top_urls 리스트를 반환한다.
    반환 형태: [(url, count), (url, count), ...]
    """
    print("\n== 에러 최다 URL TOP 5 ==")

    # error_url_counts.items() -> [(url, count), (url, count), ...] 형태의 리스트
    # key=lambda item: item[1] : 각 튜플(item)에서 두 번째 값(count)을 정렬 기준으로 사용
    # reverse=True : 개수가 많은 순서(내림차순)로 정렬
    sorted_urls = sorted(error_url_counts.items(), key=lambda item: item[1], reverse=True)

    top_urls = sorted_urls[:top_n]  # 상위 top_n개만 잘라냄

    for rank, (url, count) in enumerate(top_urls, start=1):
        print(f"{rank}위: {url} ({count}회)")

    return top_urls

def count_ip(ip_counts: dict, ip: str) -> None:
    """
    ip_counts 딕셔너리에 IP별 요청 등장 횟수를 누적한다.
    """
    ip_counts[ip] = ip_counts.get(ip, 0) + 1


def print_top_ips(ip_counts: dict, top_n: int = 5) -> list:
    """
    요청 수가 많은 IP를 상위 top_n개까지 순위와 함께 출력한다.
    반환 형태: [(ip, count), (ip, count), ...]
    """
    print("\n== 요청 최다 IP TOP 5 (의심 트래픽 확인용) ==")

    sorted_ips = sorted(ip_counts.items(), key=lambda item: item[1], reverse=True)
    top_ips = sorted_ips[:top_n]

    for rank, (ip, count) in enumerate(top_ips, start=1):
        print(f"{rank}위: {ip} ({count}회)")

    return top_ips


def count_method(method_counts: dict, method: str) -> None:
    """
    method_counts 딕셔너리에 HTTP 메서드(GET, POST 등) 등장 횟수를 누적한다.
    """
    method_counts[method] = method_counts.get(method, 0) + 1


def print_method_summary(method_counts: dict) -> None:
    """
    HTTP 메서드별 집계 결과를 알파벳 순서로 정렬해서 출력한다.
    """
    print("\n== 메서드별 요청 수 ==")

    for method in sorted(method_counts.keys()):
        count = method_counts[method]
        print(f"{method} : {count}개")


def calculate_error_rate(error_count: int, success_count: int) -> float:
    """
    전체 요청 중 에러(400 이상) 요청의 비율을 퍼센트로 계산한다.
    """
    if success_count == 0:
        return 0.0
    return (error_count / success_count) * 100


def print_error_rate(error_count: int, success_count: int) -> None:
    """
    에러율을 계산해서 소수점 둘째 자리까지 출력한다.
    """
    rate = calculate_error_rate(error_count, success_count)
    print("\n== 에러율 ==")
    print(f"전체 {success_count}건 중 에러 {error_count}건 -> {rate:.2f}%")


if __name__ == "__main__":
    main()


# import json
#
# results = {
#     "status_counts": status_counts,
#     "hourly_counts": hourly_counts,
#     "top_error_urls": top_error_urls
# }
#
# with open("results.json", "w", encoding="utf-8") as f:
#     json.dump(results, f, ensure_ascii=False, indent=2)
#
# print("results.json 저장 완료")
