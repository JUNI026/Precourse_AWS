# =====================================================
# 프롬프트 비교 실습 - 미션 2. 4원칙을 적용해 요청하기
# =====================================================
# 1) 2차 시도 프롬프트를 AI에게 보내세요. (수정해도 좋아요)
# 2) AI가 준 코드를 아래에 붙여넣고 실행해 보세요.
#
# 실행 후 기록해 보기:
# - 미션 1과 2의 가장 큰 차이 - 내가 요구한 코드와 다른 결과가 나올 수도 있음.
# - 4원칙 중 결과에 가장 크게 영향을 준 것 - 역할부여와 단계분해
# - 다음에 프롬프트 쓸 때 꼭 넣을 것

# TODO: AI가 준 코드를 여기에 붙여넣으세요.

import re  # 정규표현식(패턴 매칭)을 사용하기 위한 표준 라이브러리


def parse_line(log_line):
    """
    웹 서버 접속 로그 한 줄을 파싱해서
    IP, 시각, 메서드, URL, 상태코드를 딕셔너리로 반환하는 함수
    """

    # 1. 로그 한 줄의 구조를 그대로 표현한 정규표현식 패턴
    #    괄호()로 감싼 부분이 우리가 뽑아내고 싶은 값(그룹)이에요
    pattern = (
        r'(?P<ip>\S+)'              # IP 주소: 공백이 아닌 문자들 (\S+)
        r'\s+-\s+-\s+'              # " - - " 부분은 그냥 건너뜀
        r'\[(?P<time>[^\]]+)\]'     # [ ] 안에 있는 시각 문자열
        r'\s+"(?P<method>[A-Z]+)'  # 큰따옴표 안 첫 단어 = HTTP 메서드 (GET, POST 등)
        r'\s+(?P<url>\S+)'          # 그 다음 공백 없는 문자열 = URL
        r'\s+HTTP/[\d.]+"'          # HTTP/1.1" 부분은 형식 확인용, 값은 안 뽑음
        r'\s+(?P<status>\d+)'       # 상태코드: 숫자
    )

    # 2. 패턴과 실제 로그 문자열을 매칭시켜봄
    match = re.search(pattern, log_line)

    # 3. 매칭이 안 되면(형식이 다르면) None 반환
    if not match:
        return None

    # 4. 매칭된 그룹들을 딕셔너리로 정리해서 반환
    result = {
        "ip": match.group("ip"),
        "time": match.group("time"),
        "method": match.group("method"),
        "url": match.group("url"),
        "status": int(match.group("status")),  # 문자열 -> 정수로 변환
    }

    return result


def analyze_log_file(file_path):
    """
    로그 파일을 한 줄씩 읽어서 parse_line으로 분석하고
    결과를 리스트로 모아서 반환하는 함수
    """
    parsed_logs = []      # 파싱 성공한 결과들을 저장할 리스트
    failed_count = 0      # 파싱에 실패한 줄 개수를 셀 변수

    # 1. 파일을 열어서 한 줄씩 읽음
    #    encoding="utf-8"은 한글 등이 깨지지 않게 해주는 옵션이에요
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # 줄 끝의 개행문자(\n) 등 공백 제거

            if not line:          # 빈 줄이면 건너뜀
                continue

            # 2. parse_line 함수로 한 줄씩 분석
            result = parse_line(line)

            # 3. 파싱 성공하면 리스트에 추가, 실패하면 카운트만 증가
            if result:
                parsed_logs.append(result)
            else:
                failed_count += 1

    print(f"총 {len(parsed_logs)}줄 파싱 성공, {failed_count}줄 실패")
    return parsed_logs


# ---------- 테스트 & 실행 코드 (하나로 통합) ----------
if __name__ == "__main__":

    # 1) 먼저 parse_line 함수 하나만 잘 동작하는지 샘플 로그로 확인
    sample_log = '127.0.0.1 - - [07/Jul/2026:10:23:45 +0900] "GET /index.html HTTP/1.1" 200 1043'
    print("=== parse_line 단독 테스트 ===")
    print(parse_line(sample_log))

    # 2) 실제 로그 파일 분석
    print("\n=== 실제 로그 파일 분석 ===")
    log_path = r"C:\Users\admin\precoures\day2\1_프롬프트_비교실습\access_mini.log"
    logs = analyze_log_file(log_path)

    # 결과 중 앞부분 3개만 미리보기
    for entry in logs[:3]:
        print(entry)



# --- 미션 3: 비정상 입력 테스트 ---
# 위 코드를 붙여넣은 뒤, 아래 주석을 풀고 실행해 보세요. 
# 💥 에러가 나는 게 정상입니다!
# 에러 메시지 + 문제 입력을 "좋은 수정 요청" 형식으로 AI에게 전달하고,
# 형식에 맞지 않는 줄이 들어오면 None을 반환하도록 수정을 요청하세요.
#
# print(parse_line('127.0.0.1 - - [07/Jul/2026:10:23:45 +0900] "GET /index.html HTTP/1.1" 200 1043'))
# print(parse_line(""))                        # 빈 줄
# print(parse_line("### broken line ###"))     # 형식이 깨진 줄

# 정상 로그
print(parse_line('127.0.0.1 - - [07/Jul/2026:10:23:45 +0900] "GET /index.html HTTP/1.1" 200 1043'))

# 비정상 입력들
print(parse_line(""))                        # 빈 줄
print(parse_line("### broken line ###"))     # 형식이 깨진 줄