# =====================================================
# 파이썬 실습 - 미션 2. 딕셔너리 카운팅
# =====================================================
# 각 HTTP 메서드가 몇 번 등장하는지 딕셔너리로 집계해 출력하세요.
#
# 기대 출력
#   GET: 5
#   POST: 3
#   DELETE: 1
#   PUT: 1

methods = ["GET", "POST", "GET", "GET", "DELETE", "POST", "GET", "PUT", "GET", "POST"]

# --- 딕셔너리 카운팅 ---
# TODO: 수업 코드를 따라 여기에 작성해 보세요.

""" counts = {}
for i in methods:
    counts[i] = counts.get(i,0) + 1

for j in counts:
    print(f"{j} : {counts[j]}")
"""

counts = {}
for m in methods:
    counts[m] = counts.get(m,0)+1
for key, value in counts.items():
    print(f"{key} : {value}")

# --- 추가 목표: 가장 많이 등장한 메서드 하나를 찾아 출력하세요 ---
# 🤔 힌트: top = max(counts, key=counts.get)
# TODO: 수업 코드를 따라 여기에 작성해 보세요.

top = max(counts, key=counts.get)
print(f"가장 큰 많이 등장한 메소드는 {top}")