# PsychoPy 청각 Psychophysics 실험 가이드

PsychoPy를 사용하여 청각 심리 실험을 구축하기 위한 완벽한 가이드입니다.

## 📋 목차

1. [설치 및 시작](#설치-및-시작)
2. [프로젝트 구조](#프로젝트-구조)
3. [기본 실험 프로그램](#기본-실험-프로그램)
4. [고급 실험](#고급-실험)
5. [유틸리티 사용법](#유틸리티-사용법)
6. [데이터 분석](#데이터-분석)
7. [트러블슈팅](#트러블슈팅)

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
│   ├── basic_sound_experiment.py  # 기본 음향 detection 실험
│   ├── sound_discrimination.py    # 상향식 방법으로 역치 추정 실험
│   └── sound_utilities.py         # 음향 자극 생성 및 분석 유틸리티
├── data/                          # 실험 결과 CSV 파일 저장
├── stimuli/                       # 음성 파일 저장 디렉토리
├── .venv/                         # Python 3.11 가상환경
├── README.md                      # 프로젝트 설명
├── GUIDE.md                       # 이 파일
└── requirements.txt               # Python 의존성
```

---

## 기본 실험 프로그램

### 개요

`experiments/basic_sound_experiment.py`는 음향 감지(Detection) 실험을 제공합니다.

**실험 절차:**
1. 다양한 주파수의 음향 자극 제시
2. 피험자의 감지 반응 수집
3. 반응 시간 측정
4. 결과를 CSV로 저장

**주파수:** 440Hz, 660Hz, 880Hz

### 실행 방법

```bash
python experiments/basic_sound_experiment.py
```

**GUI 입력:**
- **Subject ID**: 피험자 아이디 (예: S001)
- **Session**: 세션 번호 (기본값: 1)
- **Number of Trials**: 시행 수 (기본값: 9)

### 결과 해석

생성되는 CSV 파일의 컬럼:

| 컬럼 | 설명 |
|------|------|
| trial_num | 시행 번호 |
| frequency | 자극 주파수 (Hz) |
| duration | 자극 지속 시간 (초) |
| volume | 음량 (0~1) |
| response_detected | 반응 감지 여부 (True/False) |
| reaction_time | 반응 시간 (초) |
| timestamp | 시간 정보 |

### 코드 예제: 기본 실험 커스터마이징

```python
import sys
sys.path.insert(0, 'experiments')
from basic_sound_experiment import ExperimentConfig, SoundExperiment

# 설정 수정
config = ExperimentConfig()
config.frequencies = [500, 1000, 2000]  # 다른 주파수
config.duration = 0.5  # 음향 지속 시간 변경
config.volume = 0.5  # 음량 증가
config.num_trials = 15  # 시행 수 증가

# 실험 실행
experiment = SoundExperiment(config)
experiment.run()
```

---

## 고급 실험

### 음향 판별 실험 (상향식 방법)

`experiments/sound_discrimination.py`는 상향식 방법으로 주파수 역치를 추정합니다.

**실험 방식:**
- **기준음**: 처음 제시되는 음 (기준)
- **비교음**: 변하는 음 (상향식으로 증가)
- **피험자 과제**: 비교음이 기준음보다 높은지/낮은지 판단

**역치 추정:**
- 피험자의 반응이 바뀌는 지점 감지 (역전)
- 마지막 역전들의 평균으로 역치 추정

### 실행 방법

```bash
python experiments/sound_discrimination.py
```

**결과:**
- CSV 파일: 각 시행의 자극 주파수와 반응
- PNG 그래프: 
  - 시행별 주파수 변화
  - 반응 분포

---

## 유틸리티 사용법

### 음향 자극 생성

`sound_utilities.py`의 `ToneGenerator` 클래스 사용:

#### 1. 순음(Pure Tone)

```python
from experiments.sound_utilities import ToneGenerator
from psychopy import sound

# 440Hz 순음 생성
waveform = ToneGenerator.pure_tone(frequency=440, duration=1.0, volume=0.3)

# PsychoPy Sound 객체로 변환
psychopy_sound = sound.Sound(waveform, sampleRate=44100)
psychopy_sound.play()
```

#### 2. 스윕음(Sweep Tone) - 주파수가 변하는 소리

```python
# 200Hz에서 800Hz로 변하는 음
waveform = ToneGenerator.sweep_tone(200, 800, duration=1.0)

psychopy_sound = sound.Sound(waveform, sampleRate=44100)
psychopy_sound.play()
```

#### 3. 복합음(Complex Tone) - 여러 주파수 조합

```python
# 기본음(440Hz) + 배음들(880Hz, 1320Hz)
waveform = ToneGenerator.complex_tone(
    frequencies=[440, 880, 1320],
    amplitudes=[0.5, 0.3, 0.2],
    duration=1.0
)

psychopy_sound = sound.Sound(waveform, sampleRate=44100)
psychopy_sound.play()
```

#### 4. 백색/분홍색 소음

```python
# 백색 소음
white_noise = ToneGenerator.white_noise(duration=1.0)

# 분홍색 소음 (더 자연스러움)
pink_noise = ToneGenerator.pink_noise(duration=1.0)

psychopy_sound = sound.Sound(white_noise, sampleRate=44100)
psychopy_sound.play()
```

### 신호 처리

`SoundProcessor` 클래스 사용:

#### 1. Envelope 적용 (음성 시작/끝 부드럽게)

```python
from experiments.sound_utilities import SoundProcessor, ToneGenerator

# 순음 생성
tone = ToneGenerator.pure_tone(440, 1.0)

# Envelope 적용
processed = SoundProcessor.apply_envelope(
    tone,
    envelope_type='linear',  # 'linear', 'exp', 'hann'
    attack=0.1,    # 100ms 안내
    release=0.2    # 200ms 종료
)
```

#### 2. 필터 적용

```python
# Low-pass filter: 1000Hz 이상 제거
filtered = SoundProcessor.apply_filter(
    tone,
    filter_type='lowpass',
    cutoff_freq=1000
)

# Band-pass filter: 400-600Hz만 유지
filtered = SoundProcessor.apply_filter(
    tone,
    filter_type='bandpass',
    cutoff_freq=(400, 600)
)
```

#### 3. 진폭 변조(Amplitude Modulation)

```python
# 5Hz로 진폭이 변하는 음
modulated = SoundProcessor.apply_amplitude_modulation(
    tone,
    mod_frequency=5,
    mod_depth=0.5
)
```

### 신호 분석

`SoundAnalyzer` 클래스 사용:

```python
from experiments.sound_utilities import SoundAnalyzer

tone = ToneGenerator.pure_tone(440, 1.0)

# 지배적 주파수 찾기
dominant_freq = SoundAnalyzer.find_dominant_frequency(tone)
print(f"주파수: {dominant_freq:.1f}Hz")

# 음량 계산 (dB)
loudness = SoundAnalyzer.compute_loudness(tone)
print(f"음량: {loudness:.1f}dB")

# 스펙트럼 계산
frequencies, power = SoundAnalyzer.compute_spectrum(tone)

# 시각화
SoundAnalyzer.plot_waveform(tone, title='Pure Tone 440Hz')
SoundAnalyzer.plot_spectrum(tone, title='Power Spectrum')
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

## 커스텀 실험 만들기

### 예제: 진폭 차이 역치(Amplitude Discrimination Threshold) 실험

```python
from psychopy import visual, sound, event, core, gui, data
import numpy as np
from experiments.sound_utilities import ToneGenerator, SoundProcessor

class AmplitudeDiscriminationExperiment:
    def __init__(self):
        self.window = visual.Window(size=(800, 600), color=[-1, -1, -1])
        self.data = []
    
    def run_trial(self, reference_amplitude, test_amplitude):
        """기준 진폭과 테스트 진폭 비교"""
        
        # 자극 생성
        ref_tone = ToneGenerator.pure_tone(440, 0.5, volume=reference_amplitude)
        test_tone = ToneGenerator.pure_tone(440, 0.5, volume=test_amplitude)
        
        # 자극 제시
        ref = sound.Sound(ref_tone, sampleRate=44100)
        test = sound.Sound(test_tone, sampleRate=44100)
        
        ref.play()
        core.wait(0.5)
        core.wait(0.3)  # ISI
        test.play()
        core.wait(0.5)
        
        # 반응 수집
        instructions = visual.TextStim(
            self.window,
            text="두 번째 음이 더 크면 SPACE, 작으면 S를 누르세요",
            color='white'
        )
        instructions.draw()
        self.window.flip()
        
        event.clearEvents()
        response = None
        while response is None:
            keys = event.getKeys(keyList=['space', 's'])
            if 'space' in keys:
                response = 'louder'
            elif 's' in keys:
                response = 'quieter'
            core.wait(0.01)
        
        return {
            'reference_amplitude': reference_amplitude,
            'test_amplitude': test_amplitude,
            'response': response
        }
    
    def run(self, num_trials=20):
        """실험 실행"""
        ref_amp = 0.3
        
        for trial in range(num_trials):
            # 상향식: 약간 다른 진폭부터 시작
            test_amp = ref_amp + (trial * 0.02)
            
            result = self.run_trial(ref_amp, test_amp)
            self.data.append(result)
        
        self.window.close()
        
        # 데이터 저장
        import pandas as pd
        df = pd.DataFrame(self.data)
        df.to_csv('data/amplitude_discrimination.csv', index=False)

# 실험 실행
if __name__ == '__main__':
    exp = AmplitudeDiscriminationExperiment()
    exp.run()
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
