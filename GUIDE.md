# PsychoPy 청각 Psychophysics 실험 가이드

PsychoPy를 사용하여 청각 심리 실험을 구축하기 위한 완벽한 가이드입니다.

## 📋 목차

1. [설치 및 시작](#설치-및-시작)
2. [프로젝트 구조](#프로젝트-구조)
3. [TDT Synapse 통합 버전](#tdt-synapse-통합-버전-⚙️) ⚙️
4. [문장 음성 이해 실험](#문장-음성-이해-실험-sentence-comprehension-experiment)
5. [데이터 분석](#데이터-분석)
6. [트러블슈팅](#트러블슈팅)

---

## 설치 및 시작

### 초기 설정

```bash
# Python 가상 환경 활성화
source .venv/bin/activate

# 패키지 설치 확인
pip install -r requirements.txt
```

### 기본 실험 실행

```bash
python experiments/basic_sound_experiment.py
```

---

## 프로젝트 구조

```
psychopy_program/
├── experiments/
│   ├── sentence_comprehension.py  # 문장 음성 이해 실험
│   ├── sentence_comprehension_TDT.py  # 문장 음성 이해 + TDT 통합
├── data/                          # 실험 결과 CSV 파일 저장
├── stimuli/                       # 음성 파일 저장 디렉토리
├── .venv/                         # Python 3.11 가상환경
├── README.md                      # 프로젝트 설명
├── GUIDE.md                       # 이 파일
├── quiz.xlsx                      # 퀴즈 데이터
├── trg_table.xlsx                 # TDT 트리거값 매핑
└── requirements.txt               # Python 의존성
```

---

## TDT Synapse 통합 버전 ⚙️

문장 음성 이해 실험에 TDT(Tucker-Davis Technologies) 시스템을 통합한 고급 버전입니다. 신경생리학 실험에서 뇌 활동을 실시간으로 기록하면서 동시에 동기화된 오디오 자극을 제시할 때 사용됩니다.

### 주요 기능

| 기능 | 설명 |
|------|------|
| **TDT Synapse 연동** | RPC 연결을 통한 자동 Synapse 통신 |
| **동기화 트리거** | 오디오 재생 시작/종료 시 트리거 신호 전송 |
| **동적 트리거값** | `trg_table.xlsx`에서 오디오별 트리거값 동적 로드 |
| **모니터 자동 감지** | 해상도 자동 감지 (3단계 fallback) |
| **UI 동적 스케일링** | 모든 UI 요소 해상도에 맞게 자동 조정 |
| **Flow 최적화** | 참가자 정보 → 윈도우 초기화 순서 개선 |
| **Fixation Crosshair** | 시각적 주의 집중용 십자가 마크 |
| **Fullscreen 모드** | 전체 화면 사용 (100% 해상도) |

### 설치 및 준비

**1단계: TDT 관련 패키지 설치**
```bash
source .venv/bin/activate
pip install -r requirements.txt  # pysynapse 포함
```

**2단계: TDT 하드웨어 및 소프트웨어 설정**
- RZ5 또는 RZ6 프로세서 연결
- Synapse 소프트웨어 실행 (localhost:3333에서 대기)
- RPC 서버 활성화 확인

**3단계: 트리거값 파일 준비 (`trg_table.xlsx`)**

프로젝트 루트에 `trg_table.xlsx` 파일 생성:

```
filename          | trigger val
-----------------|-------------
Sen_01.wav       | 10
Sen_02.wav       | 20
Sen_03.wav       | 30
Sen_04.wav       | 40
```

파일 위치: `/Users/yoonseoblim/Documents/Python_Program/psychopy_program/trg_table.xlsx`

### 실행 방법

**기본 실행**
```bash
python experiments/sentence_comprehension_TDT.py
```

**실행 순서:**
1. 콘솔에서 참가자 정보 입력 (Subject ID, Session)
2. 참가자 정보 검증 및 표시
3. "Initializing PsychoPy screen..." 메시지
4. 모니터 해상도 자동 감지 및 콘솔에 인쇄
5. PsychoPy 윈도우 열기
6. 실험 화면에 시작 메시지 표시
7. 스페이스바 입력 대기
8. 실험 시작

### TDTSynapseManager 클래스

오디오 재생 시 자동으로 TDT 트리거를 전송하는 관리자 클래스:

**주요 메서드:**
```python
# TDT 연결
manager = TDTSynapseManager(host='localhost', port=3333)
manager.connect()  # 자동으로 호출됨

# 트리거 신호 전송
manager.send_trigger(trigger_value=10)  # 오디오 시작
manager.send_trigger(trigger_value=0)   # 오디오 종료

# 연결 상태 확인
if manager.is_connected():
    print("TDT 연결됨")
```

**연결 실패 시:**
- pysynapse 미설치 → 경고 후 TDT 기능 비활성화
- Synapse 미실행 → 경고 후 트리거 없이 실험 진행
- **기본 실험은 정상 작동**

### 모니터 해상도 자동 감지

실험 시작 시 자동으로 모니터 해상도를 감지합니다:

**감지 순서 (Fallback):**
```
1. pyglet 라이브러리
   ↓ (실패 시)
2. screeninfo 라이브러리
   ↓ (실패 시)
3. macOS Quartz (macOS 전용)
   ↓ (실패 시)
4. 기본값: 1920x1080
```

**콘솔 출력 예시:**
```
Using pyglet backend
Detected screen resolution: 2560x1440
Scale factor: 1.20x (window will scale to 120% of reference size)
```

### 동적 UI 스케일링

모든 UI 요소가 감지된 해상도에 맞게 자동으로 스케일링됩니다:

**기준 해상도: 1920x1080**
- 텍스트 높이: `35 * scale`
- 십자가 크기: `17 * scale`
- Y 위치: `y * scale_y`
- 텍스트 줄바꿈 너비: `screen_width * 90%`

**예시:**
```
감지 해상도: 2560x1440
기준 해상도: 1920x1080
Scale: min(2560/1920, 1440/1080) = 1.20

텍스트 높이: 35 * 1.20 = 42
십자가 크기: 17 * 1.20 = 20
```

### Fixation Crosshair

오디오 재생 중 시각적 주의 집중을 위해 십자가 마크가 표시됩니다:

**외형:**
- 배경: 회색 (0.3, 0.3, 0.3) 또는 검은색
- 십자가: 흰색 (1, 1, 1)
- 구성: 수평선 + 수직선 + 중심점
- 크기: 동적 스케일링 적용 (기본 17px)

**코드:**
```python
# 십자가 크기 커스터마이징
crosshair_size = int(30 * scale)  # 17에서 30으로 변경
```

### 참가자 정보 수집 Flow

새로운 최적화된 플로우:

**이전 (Traditional):**
```
윈도우 생성 → 참가자 정보 입력 (블로킹) → 실험 시작
```

**현재 (Optimized):**
```
콘솔에서 참가자 정보 입력 (빠름) → 윈도우 생성 → 실험 시작
```

**장점:**
- PsychoPy 윈도우가 미리 열리지 않음 (부자연스러움 제거)
- 참가자 정보 입력이 터미널에서 진행 (더 빠름)
- 윈도우가 준비되면 실험 화면 즉시 표시

### 문제 해결

**Q: TDT 연결 안 됨**
```
A: Synapse 소프트웨어가 실행 중인지 확인
   host='localhost', port=3333 설정 확인
   콘솔에 "TDT 연결 실패" 메시지 출력 → 일반 모드로 진행
```

**Q: 모니터 해상도 잘못 감지됨**
```
A: 콘솔에 감지된 해상도 확인
   필요시 코드에서 수동으로 설정:
   self.screen_width = 2560
   self.screen_height = 1440
```

**Q: 십자가가 너무 크거나 작음**
```
A: experiments/sentence_comprehension_TDT.py에서
   crosshair_size = int(17 * self.scale)  # 17을 다른 값으로 변경
```

**Q: pysynapse 설치 안 됨**
```
A: pip install --upgrade pysynapse>=0.0.3
   또는 TDT 기능 없이 실험 진행 (자동으로 폴백)
```

### 데이터 출력

TDT 버전도 기본 버전과 동일한 데이터 형식:

```
trial_num        : 시행 번호
total_trials     : 전체 시행 수
left_file        : 좌측 음원 파일명
right_file       : 우측 음원 파일명
correct_answer   : 정답 (1-4)
user_response    : 피험자 응답 (1-4)
is_correct       : 정답 여부 (True/False)
latency_sec      : 반응 시간 (초)
timestamp        : 실험 시간 (ISO 형식)
```

**추가 정보 (콘솔 로그):**
```
Detected screen resolution: 2560x1440
TDT 연결됨
트리거값 테이블 로드됨 (25개 파일)
Scale: 1.20x
```

---

## 문장 음성 이해 실험 (Sentence Comprehension Experiment)

문장 음성 이해 실험은 공간 음향(spatial audio)을 활용하여 피험자의 음성 문장 이해 능력을 측정하는 고급 실험입니다. 양쪽 스피커/헤드폰에서 서로 다른 문장을 재생하고, 그에 해당하는 객관식 문제에 답하는 방식으로 진행됩니다.

### 실험 절차

**1단계: 피험자 정보 입력**
```python
# 프로그램 시작 시 다음 정보 입력
- 피험자 ID (Subject ID): 예) S001
- 세션 번호 (Session): 예) 1
- 시작 시간 (UTC)가 자동 기록됨
```

**2단계: 실험 설명**
- 화면에 실험 절차 및 주의사항 표시
- "스페이스 바를 눌러 계속" 대기

**3단계: 문장 재생 및 이해도 테스트**
각 시행마다:
- 좌측(Left) 스피커: 첫 번째 문장 재생
- 우측(Right) 스피커: 두 번째 문장 재생 (약 0.5초 지연)
- 음성 재생 완료 후 4지선다형 문제 표시
- 피험자 응답 수집 (1~4 키 입력)
- 반응 시간(latency) 자동 측정

**4단계: 결과 저장 및 시각화**
- CSV 파일: `data/{Subject_ID}_session{N}_{timestamp}.csv`
- 결과 그래프: `data/sentence_comprehension_{timestamp}.png` (4개 그래프)

### 퀴즈 데이터 형식 (quiz.xlsx)

퀴즈 데이터는 `quiz.xlsx` 파일에 저장됩니다:

| 열 이름 | 설명 | 예시 |
|--------|------|------|
| filename | 음성 파일명 | Sen_01.wav |
| quiz | 질문 텍스트 (한글) | 어디에 가서 물건을 샀나요? |
| 1 | 1번 선택지 | 백화점 |
| 2 | 2번 선택지 | 마트 |
| 3 | 3번 선택지 | 시장 |
| 4 | 4번 선택지 | 편의점 |
| 정답 | 정답 (1-4) | 3 |

### 결과 CSV 형식

실험 결과는 다음 열로 저장됩니다:

```
trial_num        : 시행 번호
total_trials     : 전체 시행 수
left_file        : 좌측 스피커 음성 파일명
right_file       : 우측 스피커 음성 파일명
correct_answer   : 정답 (1-4)
user_response    : 피험자 응답 (1-4)
is_correct       : 정답 여부 (True/False)
latency_sec      : 반응 시간 (초)
timestamp        : 실험 시간 (ISO 형식)
```

### 데이터 분석 예제

**1. 기본 성능 통계**
```python
import pandas as pd

# 데이터 로드
df = pd.read_csv('data/S001_session1_20260207_205636.csv')

# 정확도 출력
accuracy = df['is_correct'].sum() / len(df) * 100
print(f"정확도: {accuracy:.1f}% ({df['is_correct'].sum()}/{len(df)})")

# 반응시간 통계
print(f"평균 반응시간: {df['latency_sec'].mean():.2f}초")
print(f"최소 반응시간: {df['latency_sec'].min():.2f}초")
print(f"최대 반응시간: {df['latency_sec'].max():.2f}초")
```

**2. 질문별 성능 분석**
```python
# 각 질문별 정확도
quiz_performance = df.groupby('right_file').agg({
    'is_correct': ['sum', 'count', 'mean']
})
quiz_performance.columns = ['정답수', '총수', '정확도']
print(quiz_performance)
```

**3. 반응시간 분석**
```python
# 정답/오답별 반응시간 비교
correct_latency = df[df['is_correct']]['latency_sec'].mean()
incorrect_latency = df[~df['is_correct']]['latency_sec'].mean()

print(f"정답 시 평균 반응시간: {correct_latency:.2f}초")
print(f"오답 시 평균 반응시간: {incorrect_latency:.2f}초")
```

**4. 성과 추이 분석**
```python
# 시행 진행에 따른 성과
df['cumulative_correct'] = df['is_correct'].cumsum()
df['cumulative_accuracy'] = df['cumulative_correct'] / (df.index + 1)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['cumulative_accuracy'])
plt.xlabel('시행 번호')
plt.ylabel('누적 정확도')
plt.title('시행 진행에 따른 정확도 변화')
plt.grid(True)
plt.show()
```

### 음향 처리 기술

실험은 다음 기술을 사용하여 고음질 공간 음향을 제공합니다:

**1. 음파일 로딩 (soundfile)**
```python
import soundfile as sf
audio_data, sample_rate = sf.read('stimuli/audio.wav')
```

**2. 자동 재샘플링 (scipy.signal.resample)**
- 모든 음파일은 자동으로 44100 Hz로 정규화됨
- 다양한 샘플율(22050, 48000, 16000 등) 지원
- 음질 손상 최소화

```python
from scipy import signal
resampled = signal.resample(audio_data, int(len(audio_data) * 44100 / original_sr))
```

**3. 스테레오 채널 혼합 (numpy.column_stack)**
```python
import numpy as np
# 좌측과 우측 채널 결합
stereo_audio = np.column_stack([left_channel, right_channel])
```

**4. 백그라운드 재생 (sounddevice)**
```python
import sounddevice as sd
# 비동기 재생 (프로그램 계속 실행)
stream = sd.play(stereo_audio, samplerate=44100)
```

### 실험 커스터마이징

**변수 수정 (experiments/sentence_comprehension.py 상단)**
```python
# 시행 수 변경
num_trials = 20  # 기본값: 10

# CSV 저장 경로 변경
csv_file = 'data/custom_output.csv'

# 음성 폴더 경로 변경
stimuli_folder = 'stimuli/'  # 음성 파일들이 있는 폴더
```

**음성 파일 추가**
1. `stimuli/` 폴더에 WAV 파일 복사
2. `quiz.xlsx`에 해당 파일명 및 질문 추가
3. 프로그램 재실행

**그래프 설정 변경**
```python
# plot_results() 메서드에서 수정:
plt.figure(figsize=(15, 10))  # 그래프 크기 변경
# 색상 변경 (green → blue, etc)
plt.plot(indices, accuracies, color='blue')
```

**반응시간 제한 추가**
```python
# show_quiz() 메서드 수정
max_time = 5.0  # 5초 제한
if latency_sec > max_time:
    response = 0  # 시간 초과 시 무응답 처리
```

### 실행 방법

**기본 실행**
```bash
cd /Users/yoonseoblim/Documents/Python_Program/psychopy_program
source .venv/bin/activate
python experiments/sentence_comprehension.py
```

**결과 빠르게 확인**
```bash
# 생성된 CSV 파일 확인
ls -la data/S*.csv

# 생성된 그래프 확인
ls -la data/sentence_comprehension_*.png
```

---

## 데이터 분석

### CSV 파일 읽기

```python
import pandas as pd

# 데이터 로드
df = pd.read_csv('data/S001_session1_20260207_120000.csv')

# 기본 통계
print(f"총 시행: {len(df)}")
print(f"감지율: {df['response_detected'].mean():.1%}")
print(f"평균 반응시간: {df['reaction_time'].mean():.3f}초")

# 주파수별 성능
performance_by_freq = df.groupby('frequency').agg({
    'response_detected': ['count', 'sum', 'mean'],
    'reaction_time': 'mean'
})
print(performance_by_freq)
```

### 결과 시각화

```python
import matplotlib.pyplot as plt

# 반응시간 분포
plt.figure(figsize=(10, 5))
plt.hist(df['reaction_time'].dropna(), bins=15)
plt.xlabel('반응시간 (초)')
plt.ylabel('빈도')
plt.title('반응시간 분포')
plt.show()

# 주파수별 감지율
freq_detection = df.groupby('frequency')['response_detected'].mean()
plt.figure(figsize=(10, 5))
freq_detection.plot(kind='bar')
plt.xlabel('주파수 (Hz)')
plt.ylabel('감지율')
plt.title('주파수별 감지율')
plt.tight_layout()
plt.show()
```

---

## 트러블슈팅

### 문제: 소리가 들리지 않음

**해결책:**
1. 시스템 음량 확인
2. 스피커/헤드폰 연결 확인
3. 코드에서 `volume` 값 증가:
   ```python
   config.volume = 0.8  # 0~1 범위
   ```

### 문제: GUI 대화상자가 나타나지 않음

**해결책:**
- macOS: 권한 설정 확인
- 또는 코드에서 직접 설정:
  ```python
  config = ExperimentConfig()
  config.subject_id = 'S001'
  experiment = SoundExperiment(config)
  experiment.run()
  ```

### 문제: CSV 파일이 저장되지 않음

**해결책:**
1. `data/` 디렉토리 존재 확인 (자동 생성됨)
2. 쓰기 권한 확인:
   ```bash
   ls -la data/
   ```

### 문제: PsychoPy 관련 오류

**해결책:**
```bash
# 가상환경 재활성화
source .venv/bin/activate

# PsychoPy 재설치
pip install --upgrade psychopy
```

---

## 참고 자료

- [PsychoPy 공식 문서](https://www.psychopy.org/)
- [PsychoPy API 레퍼런스](https://www.psychopy.org/api/)
- [청각 신호 처리](https://en.wikipedia.org/wiki/Digital_signal_processing)

---

**마지막 업데이트:** 2026년 2월 7일
