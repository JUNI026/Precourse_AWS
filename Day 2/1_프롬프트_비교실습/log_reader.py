# =====================================================
# 프롬프트 비교 실습 - 심화미션. 파일 전체 파싱
# =====================================================
# 지금까지는 로그 한 줄을 처리했지만, 실제 서버 로그는 쌓여서 파일이 됩니다.
# 어제 배운 파일 읽기와 오늘 만든 parse_line을 합쳐 파일 전체를 파싱합니다.
# 직접 작성해도 좋고, AI에게 시켜도 좋습니다.
#
# 요구사항
#   - access_mini.log 파일을 한줄씩 읽어 parse_line으로 파싱한다.
#   - 결과가 none이면 건너뛰고, 전체 줄 수와 파싱 성공한 줄, 건너띈 줄을 센다.
#
# 기대 출력
#   전체 줄 수 : 15
#   파싱 성공 : 12
#   건너뛴 줄 : 3

# --- 1. 완성한 parse_line 함수 붙여넣기 ---
# TODO: log_parser_v3.py에서 완성한 parse_line 함수를 붙여넣으세요

import re  # 정규표현식(패턴 매칭)을 사용하기 위한 표준 라이브러리


def parse_line(log_line):
    """
    웹 서버 접속 로그 한 줄을 파싱해서
    IP, 시각, 메서드, URL, 상태코드를 딕셔너리로 반환하는 함수
    """
    pattern = (
        r'(?P<ip>\S+)'
        r'\s+-\s+-\s+'
        r'\[(?P<time>[^\]]+)\]'
        r'\s+"(?P<method>[A-Z]+)'
        r'\s+(?P<url>\S+)'
        r'\s+HTTP/[\d.]+"'
        r'\s+(?P<status>\d+)'
    )

    match = re.search(pattern, log_line)

    if not match:
        return None

    result = {
        "ip": match.group("ip"),
        "time": match.group("time"),
        "method": match.group("method"),
        "url": match.group("url"),
        "status": int(match.group("status")),
    }

    return result



# --- 2. 파일 전체 파싱하기 ---
# TODO: AI가 준 코드를 여기에 붙여넣으세요. 직접 작성해봐도 좋습니다.

def analyze_log_file(file_path):
    """
    로그 파일을 한 줄씩 읽어서 parse_line으로 분석하고,
    전체 줄 수 / 성공 줄 수 / 건너뛴 줄 수를 계산하는 함수
    (빈 줄도 '건너뛴 줄'로 포함해서 셈)
    """
    parsed_logs = []   # 파싱 성공한 결과들을 저장할 리스트
    total_count = 0    # 파일 전체 줄 수 (빈 줄 포함)
    skipped_count = 0  # None이 나와서 건너뛴 줄 수 (빈 줄 + 형식 깨진 줄)

    # 1. 파일을 열어서 한 줄씩 읽음
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            total_count += 1       # 줄을 하나 읽을 때마다 전체 줄 수 +1
            line = line.strip()    # 줄 끝의 개행문자(\n) 등 공백 제거

            # 2. parse_line으로 파싱 시도
            #    (빈 줄이어도 그냥 parse_line에 넘겨서 결과가 None인지로 판단)
            result = parse_line(line)

            # 3. 결과가 None이면 건너뛰고 카운트만 증가
            if result is None:
                skipped_count += 1
                continue

            # 4. 성공한 결과는 리스트에 추가
            parsed_logs.append(result)

    # 5. 최종 결과 출력
    print(f"전체 줄 수: {total_count}")
    print(f"파싱 성공: {len(parsed_logs)}줄")
    print(f"건너뛴 줄: {skipped_count}줄")

    return parsed_logs


# ---------- 실행 코드 ----------
if __name__ == "__main__":
    log_path = r"C:\Users\admin\precoures\day2\1_프롬프트_비교실습\access_mini.log"
    logs = analyze_log_file(log_path)
