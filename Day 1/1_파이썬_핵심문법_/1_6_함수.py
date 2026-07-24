# =====================================================
# 파이썬 핵심 문법 - 06. 함수
# =====================================================
# 함수란? 반복해서 쓸 코드에 이름을 붙이는 것

# --- 함수 정의와 호출 ---
# TODO: 수업 코드를 따라 여기에 작성해 보세요.
def is_error(status):
    return status >= 400

print(is_error(200))    # False
print(is_error(500))    # True

# --- 카운팅을 함수로 만들기 ---
# TODO: 수업 코드를 따라 여기에 작성해 보세요.

def count_items(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts

result = count_items(["a", "b", "a"])
print(result)    # {'a': 2, 'b': 1}