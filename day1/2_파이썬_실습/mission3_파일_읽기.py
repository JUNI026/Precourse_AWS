# =====================================================
# 파이썬 실습 - 미션 3. 파일 읽기
# =====================================================
# 1) 먼저 연습용 파일 mini.log를 이 폴더에 직접 만드세요. (강의자료 참고)
# 2) mini.log를 읽어 다음을 출력하세요.
#    - 전체 줄 수
#    - ERROR가 포함된 줄 수
#
# 🤔 힌트: 특정 단어 포함 여부는  if "ERROR" in line:  으로 확인
#
# 기대 출력
#   전체 줄 수: 7
#   에러 줄 수: 3

# TODO: 수업 코드를 따라 여기에 작성해 보세요.

Tline = 0 
Eline = 0 

with open("mini.log","r",encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            Eline = Eline+1
        Tline = Tline + 1

print(f"전체 줄 수: {Tline}")
print(f"에러 줄 수: {Eline}")


