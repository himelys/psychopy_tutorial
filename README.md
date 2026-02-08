# 🎵 PsychoPy 청각 심리물리 실험

Python 기반 PsychoPy 플랫폼을 사용한 청각 심리물리 실험 프로그램입니다.

## 📌 프로젝트 개요

이 프로젝트는 아래와 같은 청각 실험을 제공합니다:

### 3️⃣ 문장 음성 이해 실험 (Sentence Comprehension Experiment)
- 좌우 스피커에서 서로 다른 문장 음원을 동시에 제시 (공간 음향)
- 오른쪽 음원에 대한 4지선다형 퀴즈 제시
- 정답과 오답 비교로 이해도 측정
- 반응 시간(Latency) 측정 및 정확도 계산
- 자동 데이터 수집 및 분석

---

## 🔧 요구사항

| 항목 | 버전 | 비고 |
|------|------|------|
| **Python** | 3.11 | PsychoPy 호환성: 3.8-3.11 |
| **PsychoPy** | 2025.2.4+ | 자극 및 실험 제시 |
| **NumPy** | 2.2+ | 신호 처리 |
| **SciPy** | 1.14+ | 신호 처리, 재샘플링 |
| **Pandas** | 3.0+ | 데이터 분석 |
| **Matplotlib** | 3.10+ | 결과 시각화 |
| **sounddevice** | 0.5.5+ | 오디오 재생 |
| **soundfile** | 0.12.1+ | 음성 파일 I/O |
| **openpyxl** | 3.0.0+ | 엑셀 파일 처리 (quiz.xlsx, trg_table.xlsx) |
| **tdt** | 최신 버전 | TDT Synapse 통합 (옵션) ⚙️ |

**추가 요구사항 (TDT 통합 버전):**
- TDT RZ5 또는 RZ6 프로세서
- Synapse 소프트웨어 (RPC 서버 활성화)
- `trg_table.xlsx` 파일

---

## 🚀 설치 및 실행

### 1. 가상환경 활성화
```bash
cd psychopy_tutorial
source .venv/bin/activate        # macOS/Linux
# 또는
.\.venv\Scripts\activate         # Windows
```

### 2. 필요한 패키지 설치

```bash
pip install psychopy scipy pandas matplotlib sounddevice soundfile openpyxl tdt
```

### 3. 실험 실행

#### 📝 문장 음성 이해 실험 (Sentence Comprehension Experiment)
```bash
python experiments/sentence_comprehension.py
```

**실험 절차:**
1. 피험자 정보 입력 (GUI 대화상자)
2. 실험 지시문 읽기
3. 각 시행:
   - 좌우 스피커에서 다른 문장 음원 재생 (1~3초)
   - 오른쪽 음원에 대한 4지선다형 퀴즈 제시
   - 1~4 숫자키로 정답 선택
4. 모든 음원 쌍 완료 후 자동 종료

**특징:**
- 공간 음향 (좌/우 스테레오 채널)
- 자동 정확도 계산
- 반응 시간(Latency) 측정
- 정/오 정보 저장
- 4개 그래프 자동 생성

#### 📝 문장 음성 이해 실험 - TDT 통합 버전 (Sentence Comprehension + TDT Synapse) ⚙️
```bash
python experiments/sentence_comprehension_TDT.py
```

**TDT 통합 버전의 주요 기능:**

| 기능 | 설명 |
|------|------|
| **TDT Synapse 연동** | Synapse RPC 자동 연결 (localhost:3333) |
| **트리거 신호** | 오디오 시작/종료 시 동기화된 트리거 전송 |
| **동적 트리거값** | `trg_table.xlsx`에서 오디오별 트리거값 로드 |
| **모니터 자동 감지** | 해상도 자동 감지 (pyglet → screeninfo → Quartz) |
| **UI 동적 스케일링** | 모든 UI 요소가 모니터 해상도에 맞게 자동 조정 |
| **최적화된 플로우** | 참가자 정보 → 윈도우 초기화 (순차 실행) |
| **Fixation Crosshair** | 시각적 주의 집중용 십자가 마크 표시 |
| **풀스크린 모드** | 100% 전체 화면 사용 |

**필수 파일 (`trg_table.xlsx` 예제):**
```
filename          | trigger val
-----------------|-------------
Sen_01.wav       | 1
Sen_02.wav       | 2
Sen_03.wav       | 3
...              | ...
```



---

## 📁 폴더 구조

```
psychopy_program/
│
├── experiments/                              # 🔬 실험 프로그램
│   ├── sentence_comprehension.py            # 문장 음성 이해 실험
│   ├── sentence_comprehension_TDT.py        # 문장 음성 이해 + TDT 통합 ⚙️
│   └── sound_utilities.py                   # 음향 유틸리티
│
├── data/                                     # 📊 실험 결과
│   ├── *.csv                                # 실험 데이터
│   └── *.png                                # 결과 그래프
│
├── stimuli/                                  # 🔊 음성 자극 파일
├── .venv/                                    # 🐍 Python 3.11
│
├── README.md                                 # 📖 이 파일
├── COMPLETION_REPORT.md                      # ✅ 완성 보고서
├── GUIDE.md                                  # 📚 상세 가이드
├── trg_table.xlsx                            # TDT 트리거값 매핑 ⚙️
├── quiz.xlsx                                 # 📋 퀴즈 데이터
└── requirements.txt                          # 📋 의존성
```

---

## 📊 실험 결과

각 실험 후 `data/` 폴더에 자동으로 저장됩니다:

### 문장 음성 이해 실험
- `{Subject_ID}_session{N}_{timestamp}.csv` - 각 시행의 정답/오답/반응시간 데이터
- `sentence_comprehension_{timestamp}.png` - 4개 그래프 (정확도 변화, 반응시간 변화, 반응시간 분포, 정확도 요약)

**CSV 컬럼 (문장 음성 이해 실험):**
- `trial_num`: 시행 번호
- `left_file`: 좌측 음원 파일명
- `right_file`: 우측 음원 파일명
- `correct_answer`: 정답 (1~4)
- `user_response`: 피험자 답변
- `is_correct`: 정/오 여부 (True/False)
- `latency_sec`: 반응 시간 (초)
- `timestamp`: 실험 시간

---

## 🎮 사용 예시

### 문장 음성 이해 실험 데이터 분석
```python
import pandas as pd

df = pd.read_csv('data/S001_session1_20250207_123456.csv')

# 정확도 계산
accuracy = df['is_correct'].mean() * 100
print(f"정확도: {accuracy:.1f}%")

# 반응시간 통계
print(f"평균 반응시간: {df['latency_sec'].mean():.2f}초")
print(f"범위: {df['latency_sec'].min():.2f}~{df['latency_sec'].max():.2f}초")

# 정답별 성능
for ans in sorted(df['correct_answer'].unique()):
    subset = df[df['correct_answer'] == ans]
    acc = subset['is_correct'].mean() * 100
    print(f"문제 {ans}: {acc:.0f}% ({subset['is_correct'].sum()}/{len(subset)})")
```

---

## 💡 주의사항

| 항목 | 설명 |
|------|------|
| 🔊 **스피커/헤드폰** | 음향 자극 재생을 위해 필수 |
| 🤫 **환경 소음** | 조용한 환경에서 실행 |
| 🎚️ **음량 조절** | 피험자에게 편안한 음량으로 조정 |
| ⏰ **반응 시간** | 기본값 3초 |

---

## 🔧 트러블슈팅

### "Font Manager failed to load file" 경고
무해한 macOS 폰트 경고입니다. AppleGothic 폰트로 한글이 정상 표시됩니다.

### 음향이 재생되지 않음
```bash
pip install sounddevice --force-reinstall
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### 실험 실행 오류
```bash
source .venv/bin/activate
pip install psychopy scipy pandas matplotlib
```

---

## 📚 관련 문서

- **[COMPLETION_REPORT.md](COMPLETION_REPORT.md)** - 완성 보고서
- **[GUIDE.md](GUIDE.md)** - 상세 가이드
- **[PsychoPy 공식 문서](https://www.psychopy.org/)** - 공식 문서

---

**버전**: 2.0 | **Python**: 3.11+ | **PsychoPy**: 2025.2.4+  
**상태**: ✅ 완성 및 테스트 완료
