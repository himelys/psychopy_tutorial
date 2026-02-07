# 🎵 PsychoPy 음향 판별 실험 - 완성 보고서

## 📋 작업 완료 현황

### ✅ 완료된 작업

#### 1. **Python 환경 구성** 
- ✓ Python 3.12 → **Python 3.11로 업그레이드** (PsychoPy 호환성 요구사항)
- ✓ `~/.venv/` 에 새로운 가상환경 생성
- ✓ PsychoPy 2025.2.4 설치 완료

#### 2. **패키지 설치**
```
✓ psychopy       2025.2.4
✓ numpy          2.2.6
✓ scipy          1.14.1
✓ pandas         3.0.0
✓ matplotlib     3.10.8
✓ sounddevice    0.5.5
✓ pynput         1.8.1
```

#### 3. **sound_discrimination.py 완전 재작성**
기존 하이브리드 코드 → **순수 PsychoPy 네이티브 구현**

**주요 개선사항:**
- `ToneGenerator` 클래스: 깨끗한 음향 생성 인터페이스
- `AscendingMethod` 클래스: 상향식 방법의 완전한 구현
- 모든 GUI 요소이 PsychoPy로 통일
- 조건부 import 제거 (PsychoPy 필수)
- 명확한 에러 처리 및 상태 표시

#### 4. **실험 기능**
```
✓ 순음 생성 (특정 주파수)
✓ 기준음 vs 비교음 제시
✓ 실시간 반응 수집
✓ 상향식 역치 추정
✓ 역전(reversal) 감지
✓ CSV 데이터 저장
✓ 결과 그래프 자동 생성
```

---

## 🚀 사용 방법

### 1. 실험 실행 (권장)
```bash
cd /Users/yoonseoblim/Documents/Python_Program/psychopy_program
./.venv/bin/python experiments/sound_discrimination.py
```

**실험 흐름:**
1. 피험자 정보 입력 (GUI 대화상자)
2. 지시문 읽기
3. 스페이스 바로 시작
4. 각 시행마다:
   - 기준음 → ISI(300ms) → 비교음 제시
   - 피험자가 비교음이 높음/낮음/같음 응답
   - 자동으로 주파수 조정
5. 4회 역전 후 자동 종료
6. 결과 저장 (CSV) 및 그래프 생성

### 2. 빠른 테스트
```bash
./.venv/bin/python quick_start.py
```

### 3. 설정 확인
```bash
./.venv/bin/python check_setup.py
```

---

## 📁 파일 구조

```
psychopy_program/
├── experiments/
│   ├── sound_discrimination.py  ← NEW: 순수 PsychoPy 구현
│   └── sound_utilities.py        ← 음향 유틸리티
├── basic_sound_experiment.py
├── demo_sound.py
├── quick_start.py
├── check_setup.py
├── test_discrimination.py
├── data/                         ← CSV 결과 저장
├── stimuli/
├── .venv/                        ← Python 3.11 가상환경
├── requirements.txt
├── README.md
└── GUIDE.md
```

---

## 🎯 주요 특징

### AscendingMethod 클래스
```python
method = AscendingMethod(
    window=window,           # PsychoPy Window
    reference_freq=440,      # 기준음 주파수 (Hz)
    start_freq=300,          # 시작 주파수 (Hz)
    step_size=5,             # 단계 크기 (Hz)
    max_freq=600             # 최대 주파수 (Hz)
)

success = method.run(max_reversals=4)  # 4회 역전까지 실행
```

### 실험 결과
- **CSV 파일**: `data/{subject_id}_discrimination_{timestamp}.csv`
- **그래프**: 주파수 변화 및 반응 분포
- **console 출력**: 통계 요약

---

## 📊 데이터 형식

### CSV 출력 (각 시행마다 1행)
```csv
trial,reference_freq,test_freq,response,response_label
1,440,300,1,높음
2,440,305,-1,낮음
3,440,300,0,같음
...
```

**응답 코드:**
- `1` = 높음 (up arrow)
- `0` = 같음 (space)
- `-1` = 낮음 (down arrow)

---

## ✨ 개선 사항 (이전 버전 대비)

| 항목 | 이전 | 현재 |
|------|------|------|
| 구현 방식 | 하이브리드 (GUI/Terminal) | 순수 PsychoPy |
| 조건부 import | Yes | No |
| 터미널 폴백 | Yes | No |
| 코드 복잡도 | 높음 (6개 메서드) | 낮음 (3개 메서드) |
| 유지보수성 | 낮음 | 높음 |
| 가독성 | 낮음 | 높음 |
| PsychoPy 기능 활용 | 부분적 | 전체 |

---

## 🔧 기술 스택

**필수 요구사항:**
- macOS / Linux / Windows
- Python 3.11 (PsychoPy 호환성)
- 스피커 또는 헤드폰 (음향 재생)

**핵심 라이브러리:**
- **PsychoPy** - GUI 및 실험 프레임워크
- **NumPy** - 신호 처리
- **SciPy** - 신호 분석
- **Pandas** - 데이터 저장
- **Matplotlib** - 결과 시각화
- **Sounddevice** - 오디오 재생

---

## 📝 다음 단계 (선택사항)

1. **기본 실험 업그레이드** (`basic_sound_experiment.py`)
   - 현재: 하이브리드 코드
   - 목표: 순수 PsychoPy로 리팩토링

2. **고급 기능 추가**
   - 다양한 역치 추정 방법 (예: 계단식 방법)
   - 실시간 데이터 시각화
   - 연속 세션 지원

3. **데이터 분석 도구**
   - 자동 통계 분석
   - 그룹 비교 분석
   - 시간 경과에 따른 추이 분석

---

## 🐛 문제 해결

### PsychoPy 윈도우가 나타나지 않음
```bash
# 몇 초 기다린 후 다시 시도
# PsychoPy는 첫 로드 시 초기화에 시간 소요
```

### 음향이 재생되지 않음
```bash
# sounddevice 설치 확인
./.venv/bin/pip install sounddevice

# 오디오 장치 확인
./.venv/bin/python -c "import sounddevice as sd; print(sd.query_devices())"
```

### "No module named 'psychopy'" 오류
```bash
# 가동원 환경 사용 확인
source .venv/bin/activate
python experiments/sound_discrimination.py
```

---

## 📚 참고자료

- [PsychoPy 공식 문서](https://www.psychopy.org/documentation.html)
- `README.md` - 프로젝트 개요
- `GUIDE.md` - 상세 가이드

---

## ✅ 확인 체크리스트

- [x] Python 3.11 설치
- [x] 가상환경 생성
- [x] 모든 패키지 설치
- [x] sound_discrimination.py 순수 PsychoPy 구현
- [x] 구문 검사 완료
- [x] 모듈 임포트 테스트 완료
- [ ] 실제 실험 운영 테스트 (GUI 필요)

---

**완성일:** 2025-02-07  
**Python 버전:** 3.11.14  
**PsychoPy 버전:** 2025.2.4  

**준비 완료! 🎉**
