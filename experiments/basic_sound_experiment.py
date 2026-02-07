#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic Sound Detection Experiment with PsychoPy
================================================
PsychoPy GUI를 사용한 기본 청각 psychophysics 실험

실험 설명:
- 피험자에게 다양한 주파수의 음향 자극을 제시
- 각 자극에 대한 반응(감지 여부, 반응 시간) 측정
- 결과를 CSV 파일과 그래프로 저장

Author: PsychoPy Experiment
Version: 2.0 (Full PsychoPy GUI Implementation)
"""

# macOS 폰트 경고 제거
import os
import sys
import warnings
os.environ['PYGLET_FONT_MANAGER_DEBUG'] = '0'
warnings.filterwarnings('ignore', category=UserWarning)

import logging
logging.getLogger('psychopy').setLevel(logging.ERROR)
logging.getLogger('pyglet').setLevel(logging.ERROR)

from psychopy import visual, sound, event, core, gui
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sounddevice as sd
from datetime import datetime
import time

# ============================================================================
# 1. 실험 설정
# ============================================================================

class ExperimentConfig:
    """실험 설정값 관리 클래스"""
    
    def __init__(self):
        # 피험자 정보
        self.subject_id = None
        self.session = 1
        
        # 자극 설정
        self.frequencies = [440, 660, 880]  # Hz (A4, E5, A5)
        self.duration = 1.0  # 초
        self.volume = 0.3  # 0~1 (상대 음량)
        
        # 실험 설정
        self.num_trials = 9  # 주파수당 3 반복
        self.isi = 1.5  # Inter-stimulus interval (초)
        self.response_timeout = 3.0  # 반응 제한 시간 (초)


# ============================================================================
# 2. 사운드 자극 생성
# ============================================================================

class SoundStimulus:
    """음향 자극 생성 클래스"""
    
    def __init__(self, frequency, duration, volume, sr=44100):
        """
        Parameters
        ----------
        frequency : float
            주파수 (Hz)
        duration : float
            지속 시간 (초)
        volume : float
            음량 (0~1)
        sr : int
            샘플링 레이트 (Hz)
        """
        self.frequency = frequency
        self.duration = duration
        self.volume = volume
        self.sr = sr
        self.waveform = None
        self._generate_waveform()
    
    def _generate_waveform(self):
        """음향 신호 생성"""
        # 시간 벡터 생성
        n_samples = int(self.sr * self.duration)
        t = np.linspace(0, self.duration, n_samples, False)
        
        # 정현파 생성: A(t) = sin(2πft)
        waveform = np.sin(2 * np.pi * self.frequency * t)
        
        # 음량 적용
        waveform = waveform * self.volume
        
        # 한강 윈도우 적용 (음성의 시작과 끝을 부드럽게)
        attack_time = 0.1  # 100ms
        fade_samples = int(self.sr * attack_time)
        
        # Attack envelope (0에서 1로)
        attack = np.linspace(0, 1, fade_samples)
        # Decay envelope (1에서 0으로)
        decay = np.linspace(1, 0, fade_samples)
        
        waveform[:fade_samples] *= attack
        waveform[-fade_samples:] *= decay
        
        self.waveform = waveform
    
    def play(self):
        """음향 자극 재생 (사운드 카드를 통해)"""
        try:
            import sounddevice as sd
            sd.play(self.waveform, samplerate=self.sr)
            sd.wait()  # 음향 재생 완료까지 대기
        except ImportError:
            print("⚠️  sounddevice 라이브러리가 설치되지 않았습니다.")
            print("   설치하려면: pip install sounddevice")
            # 시뮬레이션만 진행
            time.sleep(self.duration)
    
    def get_waveform(self):
        """음향 파형 반환"""
        return self.waveform


# ============================================================================
# 3. 실험 클래스
# ============================================================================

class SoundExperiment:
    """기본 음향 detection 실험"""
    
    def __init__(self, window, config):
        """
        Parameters
        ----------
        window : psychopy.visual.Window
            PsychoPy 윈도우
        config : ExperimentConfig
            실험 설정 객체
        """
        self.window = window
        self.config = config
        self.data_list = []
        self.current_trial = 0
    
    def show_message(self, text, duration=None, wait_for_key=False, keys=None, color='white'):
        """메시지 표시"""
        msg = visual.TextStim(
            win=self.window,
            text=text,
            font='AppleGothic',
            height=28,
            color=color,
            wrapWidth=1000,
            anchorHoriz='center'
        )
        msg.draw()
        self.window.flip()
        
        if wait_for_key:
            event.waitKeys(keyList=keys if keys else ['space'])
        elif duration:
            core.wait(duration)
    
    def show_instructions(self):
        """실험 지시문 표시"""
        instructions = visual.TextStim(
            win=self.window,
            text="청각 Detection 실험\n\n"
                 "실험 절차:\n"
                 "1. 음향 자극이 재생됩니다\n"
                 "2. 음을 감지하면 스페이스 바를 누르세요\n"
                 "3. 반응하지 않으면 3초 후 다음 시행으로 진행합니다\n\n"
                 "준비가 되면 스페이스 바를 누르세요.",
            font='AppleGothic',
            height=26,
            color='white',
            wrapWidth=1100,
            anchorHoriz='center'
        )
        instructions.draw()
        self.window.flip()
        event.waitKeys(keyList=['space'])
        core.wait(0.5)
    
    def run_trial(self, trial_num, frequency):
        """
        단일 시행 실행
        
        Parameters
        ----------
        trial_num : int
            시행 번호
        frequency : float
            자극 주파수 (Hz)
        
        Returns
        -------
        dict
            시행 데이터
        """
        # 자극 생성
        stimulus = SoundStimulus(
            frequency=frequency,
            duration=self.config.duration,
            volume=self.config.volume
        )
        
        # ISI (Inter-stimulus interval) 표시
        ready_text = visual.TextStim(
            win=self.window,
            text=f"시행 {trial_num}/{len(self.trial_list)}\n\n"
                 f"주파수: {frequency}Hz\n\n"
                 f"준비 중...",
            font='AppleGothic',
            height=24,
            color='lightGray',
            wrapWidth=800,
            anchorHoriz='center'
        )
        
        # ISI 동안 카운트다운 표시
        isi_start = time.time()
        while time.time() - isi_start < self.config.isi:
            remaining = self.config.isi - (time.time() - isi_start)
            ready_text.text = f"시행 {trial_num}/{len(self.trial_list)}\n\n주파수: {frequency}Hz\n\n{remaining:.1f}초"
            ready_text.draw()
            self.window.flip()
            core.wait(0.1)
        
        # 음향 자극 재생
        playing_text = visual.TextStim(
            win=self.window,
            text="▶ 음향 자극 재생 중...",
            font='AppleGothic',
            height=28,
            color='yellow',
            anchorHoriz='center'
        )
        playing_text.draw()
        self.window.flip()
        
        trial_start = time.time()
        stimulus.play()
        
        # 반응 대기 화면
        response_text = visual.TextStim(
            win=self.window,
            text="응답 대기 중...\n\n스페이스 바를 누르세요\n(또는 3초 대기)",
            font='AppleGothic',
            height=26,
            color='white',
            wrapWidth=800,
            anchorHoriz='center'
        )
        response_text.draw()
        self.window.flip()
        
        # 반응 대기
        response_detected = False
        reaction_time = None
        event.clearEvents()
        
        response_start = time.time()
        keys = event.waitKeys(maxWait=self.config.response_timeout, keyList=['space', 'escape'], clearEvents=True)
        
        if keys:
            if 'escape' in keys:
                return None  # 실험 중단
            if 'space' in keys:
                response_detected = True
                reaction_time = time.time() - response_start
        
        # 반응 피드백
        if response_detected:
            feedback = visual.TextStim(
                win=self.window,
                text=f"✓ 감지됨!\n반응시간: {reaction_time:.3f}초",
                font='AppleGothic',
                height=26,
                color='green',
                anchorHoriz='center'
            )
        else:
            feedback = visual.TextStim(
                win=self.window,
                text="✗ 반응 없음",
                font='AppleGothic',
                height=26,
                color='red',
                anchorHoriz='center'
            )
        
        feedback.draw()
        self.window.flip()
        core.wait(1.0)
        
        # 데이터 저장
        trial_data = {
            'trial_num': trial_num,
            'frequency': frequency,
            'duration': self.config.duration,
            'volume': self.config.volume,
            'response_detected': response_detected,
            'reaction_time': reaction_time if reaction_time else np.nan,
            'timestamp': datetime.now().isoformat()
        }
        
        return trial_data
    
    def create_trial_list(self):
        """시행 목록 생성"""
        trials = []
        trial_num = 1
        
        # 각 주파수마다 반복
        for freq in self.config.frequencies:
            for _ in range(self.config.num_trials // len(self.config.frequencies)):
                trials.append((trial_num, freq))
                trial_num += 1
        
        # 무작위로 섞기
        np.random.shuffle(trials)
        
        return trials
    
    def run(self):
        """전체 실험 실행"""
        self.show_instructions()
        
        # 시행 목록 생성
        self.trial_list = self.create_trial_list()
        
        progress_text = visual.TextStim(
            win=self.window,
            text=f"실험 시작\n\n피험자ID: {self.config.subject_id}\n총 시행 수: {len(self.trial_list)}",
            font='AppleGothic',
            height=28,
            color='white',
            anchorHoriz='center'
        )
        progress_text.draw()
        self.window.flip()
        core.wait(2)
        
        # 각 시행 실행
        for trial_num, frequency in self.trial_list:
            try:
                trial_data = self.run_trial(trial_num, frequency)
                if trial_data is None:  # ESC로 중단
                    break
                self.data_list.append(trial_data)
            except KeyboardInterrupt:
                break
        
        # 결과 표시
        result_msg = f"실험 완료!\n\n총 시행: {len(self.data_list)}\n\n스페이스를 누르면 종료됩니다."
        result_text = visual.TextStim(
            win=self.window,
            text=result_msg,
            font='AppleGothic',
            height=28,
            color='green',
            wrapWidth=1000,
            anchorHoriz='center'
        )
        result_text.draw()
        self.window.flip()
        event.waitKeys(keyList=['space'])
        
        self.teardown()
    
    def teardown(self):
        """실험 종료 처리"""
        if self.data_list:
            self.save_data()
    
    def save_data(self):
        """실험 데이터를 CSV 파일로 저장"""
        # DataFrame 생성
        df = pd.DataFrame(self.data_list)
        
        # 저장 디렉토리 생성
        os.makedirs('./data', exist_ok=True)
        
        # 파일명: subject_session_timestamp.csv
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"./data/{self.config.subject_id}_session{self.config.session}_{timestamp}.csv"
        
        # CSV 저장
        df.to_csv(csv_file, index=False)
        print(f"\n✓ 데이터가 저장되었습니다: {csv_file}")
        
        # 결과 요약
        print(f"\n결과 요약:")
        print(f"  • 총 시행: {len(df)}")
        print(f"  • 감지된 자극: {df['response_detected'].sum()}")
        print(f"  • 감지율: {df['response_detected'].mean():.1%}")
        
        if df['reaction_time'].notna().sum() > 0:
            print(f"  • 평균 반응시간: {df['reaction_time'].mean():.3f}초")
        
        # 주파수별 성능
        print(f"\n주파수별 성능:")
        for freq in sorted(df['frequency'].unique()):
            freq_data = df[df['frequency'] == freq]
            detection_count = freq_data['response_detected'].sum()
            total_count = len(freq_data)
            detection_rate = freq_data['response_detected'].mean()
            print(f"  • {freq}Hz: 감지 {detection_count}/{total_count} ({detection_rate:.0%})")
        
        # 그래프 생성
        self.plot_results(df, csv_file)
    
    def plot_results(self, df, csv_file):
        """결과 시각화"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle(f'음향 Detection 실험 결과 - {self.config.subject_id}', fontsize=14, fontweight='bold')
        
        # 그래프 1: 주파수별 감지율
        freq_stats = df.groupby('frequency')['response_detected'].agg(['sum', 'count', 'mean'])
        colors = ['#ff9999', '#99ccff', '#99ff99']
        
        bars = ax1.bar(freq_stats.index.astype(str), freq_stats['mean'], 
                       color=colors[:len(freq_stats)], alpha=0.8, width=0.6)
        ax1.set_ylabel('감지율', fontsize=12)
        ax1.set_xlabel('주파수 (Hz)', fontsize=12)
        ax1.set_title('주파수별 감지율', fontsize=12)
        ax1.set_ylim([0, 1.1])
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 값 레이블 추가
        for bar, val in zip(bars, freq_stats['mean']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.0%}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 그래프 2: 반응시간 분포
        valid_rt = df[df['reaction_time'].notna()]['reaction_time']
        if len(valid_rt) > 0:
            ax2.hist(valid_rt, bins=10, color='#6495ED', alpha=0.7, edgecolor='black')
            ax2.axvline(valid_rt.mean(), color='red', linestyle='--', linewidth=2, label=f'평균: {valid_rt.mean():.3f}초')
            ax2.set_xlabel('반응시간 (초)', fontsize=12)
            ax2.set_ylabel('빈도', fontsize=12)
            ax2.set_title('반응시간 분포', fontsize=12)
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
        else:
            ax2.text(0.5, 0.5, '반응시간 데이터 없음', 
                    ha='center', va='center', transform=ax2.transAxes, fontsize=14)
        
        plt.tight_layout()
        
        # 그래프 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        graph_file = f"./data/{self.config.subject_id}_detection_{timestamp}.png"
        plt.savefig(graph_file, dpi=150, bbox_inches='tight')
        print(f"✓ 그래프가 저장되었습니다: {graph_file}")
        plt.close()


# ============================================================================
# 4. 메인 함수
# ============================================================================

def main():
    """메인 함수 - PsychoPy GUI 모드"""
    
    print("\n" + "="*70)
    print("청각 Detection 실험 (주파수 감지)")
    print("="*70)
    
    # GUI 대화상자로 피험자 정보 입력
    dlg = gui.DlgFromDict(
        dictionary={
            'Subject ID': 'S001',
            'Session': 1,
            'Num Trials': 9
        },
        title='음향 Detection 실험',
        fixed=['Num Trials']
    )
    
    if not dlg.OK:
        print("\n실험이 취소되었습니다.")
        return
    
    # 사용자 입력 처리
    try:
        subject_id = str(dlg.data['Subject ID']).strip()
        session = int(float(dlg.data['Session']))
        num_trials = int(float(dlg.data['Num Trials']))
    except (ValueError, KeyError, TypeError) as e:
        print(f"\n❌ 입력 데이터 오류: {e}")
        print(f"수신된 데이터: {dlg.data}")
        return
    
    # 설정 객체 생성
    config = ExperimentConfig()
    config.subject_id = subject_id
    config.session = session
    config.num_trials = num_trials
    
    print(f"\n피험자 ID: {subject_id}")
    print(f"세션: {session}")
    print(f"시행 수: {num_trials}")
    print("-" * 70)
    
    # PsychoPy 윈도우 생성
    window = visual.Window(
        size=(1200, 800),
        color=[-1, -1, -1],
        units='pix',
        fullscr=False,
        monitor=None
    )
    
    try:
        # 실험 객체 생성 및 실행
        experiment = SoundExperiment(window, config)
        experiment.run()
        
        window.close()
        
    except KeyboardInterrupt:
        print("\n\n실험이 중단되었습니다.")
        window.close()
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        window.close()


if __name__ == '__main__':
    print("\n참고: sounddevice 라이브러리가 설치되면 실제 음향이 재생됩니다.")
    
    try:
        import sounddevice
        print("✓ sounddevice가 설치되어 있습니다.\n")
    except ImportError:
        print("⚠️  sounddevice 미설치 - pip install sounddevice\n")
    
    main()
