# =====================================================
# 파이썬 실습 - 심화 미션 1. 에러 줄만 추출
# =====================================================
# mini.log에서 ERROR가 포함된 줄만 골라 errors.log라는 새 파일로 저장하세요.
#
# 🤔 힌트: 파일 쓰기는 open의 두 번째 인자를 "w"로 합니다.
#   with open("errors.log", "w", encoding="utf-8") as f:
#       f.write(line + "\n")

# TODO: 수업 코드를 따라 여기에 작성해 보세요.

Tline = 0
Eline = 0
Rline = []

with open("mini.log","r",encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            Eline = Eline+1
            Rline = Rline + line
        Tline = Tline + 1


with open("error.log", "w", encoding = "utf-8") as f:
    for i in Rline:
        f.write(i + "\n")

print(f"전체 줄 수: {Tline}")
print(f"에러 줄 수: {Eline}")



