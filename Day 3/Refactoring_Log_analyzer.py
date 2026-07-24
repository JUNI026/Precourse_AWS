"""
로그 분석 실습 - 최종 리팩토링 버전
access.log 파일을 파싱해서 상태코드/시간대/에러URL/IP/메서드별 통계를 낸 뒤
results.json으로 저장한다.

로그 예시:
203.0.113.45 - - [07/Jul/2026:14:23:45 +0900] "GET /products/list HTTP/1.1" 200 5321

구성 순서
1. 정규식 패턴
2. 파싱 함수 (parse_line, extract_hour)
3. 집계 함수 (count_*)
4. 계산 함수 (calculate_error_rate)
5. 출력 함수 (print_*)
6. main() - 위 함수들을 순서대로 호출
"""

from typing import Optional
import re
import os
import json


# =====================================================
# 1. 정규식 패턴
# =====================================================

# 로그 한 줄을 매칭하기 위한 정규표현식
# 그룹 1: IP 주소 / 그룹 2: 시각 / 그룹 3: 메서드 / 그룹 4: URL / 그룹 5: 상태코드
LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+'      # IP 주소 (예: 203.0.113.45)
    r'-\s+-\s+'                                # 사용하지 않는 필드 2개 (- -)
    r'\[(?P<time>[^\]]+)\]\s+'                 # [07/Jul/2026:14:23:45 +0900]
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+HTTP/[\d.]+"\s+'  # "GET /products/list HTTP/1.1"
    r'(?P<status>\d{3})'                       # 상태 코드 (예: 200)
)


# =====================================================
# 2. 파싱 함수
# =====================================================

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


def extract_hour(time_str: str) -> Optional[str]:
    """
    "07/Jul/2026:14:23:45 +0900" 형태의 문자열에서 시(Hour) 부분만 뽑아 "14"처럼 반환한다.
    ':' 기준으로 나누면 인덱스 1번이 시(Hour)에 해당한다.
    """
    parts = time_str.split(":")
    if len(parts) < 2:
        return None

    hour = parts[1]
    if not hour.isdigit():
        return None

    return hour


# =====================================================
# 3. 집계 함수 (딕셔너리 카운팅 패턴)
# =====================================================

def count_status_codes(status_counts: dict, status: str) -> None:
    """상태코드 등장 횟수를 누적한다."""
    status_counts[status] = status_counts.get(status, 0) + 1


def count_hourly(hourly_counts: dict, hour: str) -> None:
    """시간대(00~23)별 등장 횟수를 누적한다."""
    hourly_counts[hour] = hourly_counts.get(hour, 0) + 1


def count_error_url(error_url_counts: dict, status: str, url: str) -> None:
    """
    상태코드가 400 이상인 요청에 한해 URL별 발생 횟수를 누적한다.
    status는 문자열이므로 반드시 int()로 변환한 뒤 크기 비교해야 한다.
    (문자열끼리 비교하면 "9" > "400" 처럼 자릿수 때문에 잘못된 결과가 나올 수 있다)
    """
    if int(status) >= 400:
        error_url_counts[url] = error_url_counts.get(url, 0) + 1


def count_ip(ip_counts: dict, ip: str) -> None:
    """IP별 요청 등장 횟수를 누적한다."""
    ip_counts[ip] = ip_counts.get(ip, 0) + 1


def count_method(method_counts: dict, method: str) -> None:
    """HTTP 메서드(GET, POST 등) 등장 횟수를 누적한다."""
    method_counts[method] = method_counts.get(method, 0) + 1


# =====================================================
# 4. 계산 함수
# =====================================================

def calculate_error_rate(error_count: int, success_count: int) -> float:
    """
    전체 요청(파싱 성공 기준) 중 에러(400 이상) 요청의 비율을 퍼센트로 계산한다.
    분모가 0이면(파싱 성공한 줄이 하나도 없으면) ZeroDivisionError를 방지하기 위해 0.0을 반환한다.
    """
    if success_count == 0:
        return 0.0
    return (error_count / success_count) * 100


# =====================================================
# 5. 출력 함수
# =====================================================

def print_status_summary(status_counts: dict, success_count: int) -> None:
    """
    상태코드별 집계 결과를 출력하고,
    합계가 파싱 성공 줄 수와 일치하는지 확인해서 알려준다.
    """
    print("\n== 상태 코드별 요청 수 ==")

    for status in sorted(status_counts.keys()):
        count = status_counts[status]
        print(f"{status} : {count}개")

    total_by_status = sum(status_counts.values())

    print()
    if total_by_status == success_count:
        print(f"일치 (상태코드별 합계 {total_by_status} == 파싱 성공 수 {success_count})")
    else:
        print(f"불일치 (상태코드별 합계 {total_by_status} != 파싱 성공 수 {success_count})")


def print_hourly_summary(hourly_counts: dict) -> None:
    """시간대별(00~23시) 집계 결과를 정수 순서대로 정렬해서 출력한다."""
    print("\n== 시간대 별 요청 수 ==")

    for hour in sorted(hourly_counts.keys(), key=int):
        count = hourly_counts[hour]
        print(f"{hour}시 : {count}개")


def print_top_error_urls(error_url_counts: dict, top_n: int = 5) -> list:
    """
    에러(400 이상) 발생 횟수가 많은 URL을 상위 top_n개까지 순위와 함께 출력한다.
    이후 JSON 저장 등에서 재사용할 수 있도록 정렬된 리스트를 반환한다.
    반환 형태: [(url, count), (url, count), ...]
    """
    print("\n== 에러 최다 URL TOP 5 ==")

    sorted_urls = sorted(error_url_counts.items(), key=lambda item: item[1], reverse=True)
    top_urls = sorted_urls[:top_n]

    for rank, (url, count) in enumerate(top_urls, start=1):
        print(f"{rank}위: {url} ({count}회)")

    return top_urls


def print_top_ips(ip_counts: dict, top_n: int = 5) -> list:
    """
    요청 수가 많은 IP를 상위 top_n개까지 순위와 함께 출력한다.
    비정상적으로 요청 수가 많은 IP는 크롤러나 공격 트래픽일 가능성이 있으므로
    의심 IP를 눈으로 확인하는 용도로 사용한다.
    반환 형태: [(ip, count), (ip, count), ...]
    """
    print("\n== 요청 최다 IP TOP 5 (의심 트래픽 확인용) ==")

    sorted_ips = sorted(ip_counts.items(), key=lambda item: item[1], reverse=True)
    top_ips = sorted_ips[:top_n]

    for rank, (ip, count) in enumerate(top_ips, start=1):
        print(f"{rank}위: {ip} ({count}회)")

    return top_ips


def print_method_summary(method_counts: dict) -> None:
    """HTTP 메서드별 집계 결과를 알파벳 순서로 정렬해서 출력한다."""
    print("\n== 메서드별 요청 수 ==")
    #test

    for method in sorted(method_counts.keys()):
        count = method_counts[method]
        print(f"{method} : {count}개")


def print_error_rate(error_count: int, success_count: int) -> None:
    """에러율을 계산해서 소수점 둘째 자리까지 보기 좋게 출력한다."""
    rate = calculate_error_rate(error_count, success_count)
    print("\n== 에러율 ==")
    print(f"전체 {success_count}건 중 에러 {error_count}건 -> {rate:.2f}%")


# =====================================================
# 6. main() - 파싱 -> 집계 -> 출력 -> 저장 순서로 실행
# =====================================================

def main():
    # 이 스크립트 파일이 있는 폴더를 기준으로 access.log 경로를 만든다
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, "access.log")

    total_lines = 0      # 전체 읽은 줄 수
    success_count = 0    # 파싱 성공한 줄 수
    fail_count = 0        # 파싱 실패(건너뜀)한 줄 수
    preview_count = 0     # 미리보기로 출력한 줄 수

    status_counts = {}     # 상태코드별 개수
    hourly_counts = {f"{h:02d}": 0 for h in range(24)}  # 00~23시 미리 0으로 초기화
    error_url_counts = {}  # 에러(400+) 상태코드의 URL별 개수
    ip_counts = {}          # IP별 요청 개수
    method_counts = {}      # HTTP 메서드별 요청 개수

    print("== 처음 5줄 파싱 ==")

    # --- 파싱 & 집계 단계 ---
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            total_lines += 1
            result = parse_line(line)

            if result is not None:
                success_count += 1

                count_status_codes(status_counts, result["status"])
                count_error_url(error_url_counts, result["status"], result["url"])
                count_ip(ip_counts, result["ip"])
                count_method(method_counts, result["method"])

                hour = extract_hour(result["time"])
                if hour is not None:
                    count_hourly(hourly_counts, hour)
            else:
                fail_count += 1

            # 확인용으로 첫 5줄의 파싱 결과만 출력
            if preview_count < 5:
                print(result, "\n")
                preview_count += 1

    # --- 기본 통계 출력 ---
    print("== 결과 요약 ==")
    print(f"전체 읽은 줄 수: {total_lines}")
    print(f"파싱 성공 줄 수: {success_count}")
    print(f"건너뛴 줄 수: {fail_count}")

    # --- 항목별 집계 출력 ---
    print_status_summary(status_counts, success_count)
    print_hourly_summary(hourly_counts)

    top5_urls = print_top_error_urls(error_url_counts, top_n=5)
    top_error_urls = [list(t) for t in top5_urls]

    top5_ips = print_top_ips(ip_counts, top_n=5)
    top_ips = [list(t) for t in top5_ips]

    print_method_summary(method_counts)

    error_count = sum(error_url_counts.values())
    print_error_rate(error_count, success_count)

    # --- 결과를 하나의 딕셔너리로 묶어서 JSON 저장 ---
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
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nresults.json 저장 완료: {output_path}")


if __name__ == "__main__":
    main()