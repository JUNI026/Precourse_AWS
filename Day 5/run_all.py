# -*- coding: utf-8 -*-
# =====================================================
# 5일차 · run_all.py
# 로그 분석 → 대시보드 생성을 한 번에 실행하는 스크립트
#  - log_analyzer.py, generate_dashboard.py 와 같은 폴더에서 실행
# 실행: python run_all.py   (mac은 python3)
# =====================================================
import subprocess
import sys

scripts = ["log_analyzer.py", "generate_dashboard.py"]

for script in scripts:
    print(f"\n===== {script} 실행 =====")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"{script} 실행 중 오류가 발생했습니다. 위 메시지를 확인하세요.")
        sys.exit(1)

print("\n모든 작업 완료! index.html을 커밋하고 push하면 사이트가 갱신됩니다.")
