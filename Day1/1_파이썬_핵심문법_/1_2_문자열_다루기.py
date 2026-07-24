# =====================================================
# 파이썬 핵심 문법 - 02. 문자열 다루기
# =====================================================
# strip / split / f-string
# 🔗 3일차에서 로그를 파싱하는 데 사용됩니다.

# --- strip: 앞뒤 공백 제거 ---
# TODO: 수업 코드를 따라 여기에 작성해 보세요.
text = '   안녕하세요,     ***입니다. \n'
print(text.strip())

# --- split: 문자열 자르기 ---
# TODO: 수업 코드를 따라 여기에 작성해 보세요.
line = 'GET /index.html 200'
parts = line.split()
print(parts)

part2 = line.split(".")
print(part2[0])


# --- f-string: 변수와 문자열 조합 ---
# TODO: 수업 코드를 따라 여기에 작성해 보세요.
print(f"상태코드는 {parts[2]}입니다")