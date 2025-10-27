# Playwright (Python) test scaffold

간단한 Playwright + pytest 테스트 자동화 스캐폴딩입니다.

설치 및 실행 (PowerShell):

```powershell
# 1) 가상환경 생성
python -m venv .venv

# 2) 가상환경 활성화
.\.venv\Scripts\Activate.ps1

# 3) 의존성 설치
pip install -r requirements.txt

# 4) Playwright 브라우저 설치
python -m playwright install

# 5) 테스트 실행
pytest -q
```

파일 설명:

- `requirements.txt` - 필요한 패키지 목록 (playwright, pytest, pytest-playwright)
- `pytest.ini` - pytest 설정
- `conftest.py` - 공통 fixture (예: `base_url`)
- `tests/test_example.py` - 예제 테스트
- `.gitignore` - 환경 파일 무시

주의:

- CI 환경에서는 브라우저 설치(`python -m playwright install`)를 스텝에 추가하세요.
- 필요하면 `conftest.py`에서 `base_url`을 환경변수로 읽게 수정하세요.

추가로 원하면 다음 작업을 도와드릴게요:

- GitHub Actions / Azure Pipelines용 CI 설정
- 테스트 페이지 객체 패턴(PO) 템플릿
- TypeScript/Node 기반 Playwright로의 전환 가이드
