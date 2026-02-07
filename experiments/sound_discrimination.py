#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sound Frequency Discrimination Experiment with PsychoPy
======================================================
주파수 판별 실험 - 두 개의 음향 자극을 비교하는 실험

실험 설명:
- 기준음(reference tone)과 비교음(test tone) 제시
- 피험자가 비교음이 더 높은지/낮은지 판단
- 상향식(ascending) 방법으로 역치 추정
- 결과를 그래프로 시각화

Requirements:
- Python 3.11+ (PsychoPy requirement: 3.8-3.11)
- psychopy >= 2024.1.0
- numpy, scipy, pandas, matplotlib, sounddevice

Author: PsychoPy Experiment
Version: 3.0 (Full PsychoPy Native Implementation)
"""

# macOS 폰트 경고 제거 (Font Manager 메시지 비활성화)
import os
import sys
import warnings

# Pyglet 폰트 관련 경고 제거
os.environ['PYGLET_FONT_MANAGER_DEBUG'] = '0'
warnings.filterwarnings('ignore', category=UserWarning)

# 로깅 설정 (PsychoPy 경고 최소화)
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
# 1. 음향 자극 생성
# ============================================================================

class ToneGenerator:
    """순음 및 음향 자극 생성"""
    
    @staticmethod
    def create_tone(frequency, duration, volume=0.3, sr=44100):
        """
        순음(tone) 생성
        
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
        
        Returns
        -------
        numpy.ndarray
            음성 신호 배열
        """
        n_samples = int(sr * duration)
        t = np.linspace(0, duration, n_samples, False)
        waveform = np.sin(2 * np.pi * frequency * t) * volume
        
        # Hann window를 사용한 fade-in/out
        attack_decay_time = 0.05
        fade_samples = int(sr * attack_decay_time)
        
        attack = np.linspace(0, 1, fade_samples)
        decay = np.linspace(1, 0, fade_samples)
        
        waveform[:fade_samples] *= attack
        waveform[-fade_samples:] *= decay
        
        return waveform
    
    @staticmethod
    def play_tone(waveform, sr=44100):
        """음향 자극 재생"""
        sd.play(waveform, samplerate=sr)
        sd.wait()


# ============================================================================
# 2. 상향식 방법 (Ascending Method)
# ============================================================================

class AscendingMethod:
    """
    상향식 방법으로 감각역치 추정
    
    시작: 탐지 불가능한 자극
    방향: 강도 증가
    종료: 역전(reversal)이 지정된 횟수에 도달할 때
    """
    
    def __init__(self, window, reference_freq=440, start_freq=300, 
                 step_size=5, max_freq=600):
        """
        Parameters
        ----------
        window : psychopy.visual.Window
            PsychoPy 윈도우
        reference_freq : float
            기준음 주파수 (Hz)
        start_freq : float
            시작 주파수 (Hz)
        step_size : float
            매 시행마다 조정할 주파수 (Hz)
        max_freq : float
            최대 주파수 (Hz)
        """
        self.window = window
        self.reference_freq = reference_freq
        self.current_freq = start_freq
        self.step_size = step_size
        self.max_freq = max_freq
        self.threshold = None
        self.trials = []
    
    def show_message(self, text, duration=None, wait_for_key=False, keys=None):
        """메시지 표시"""
        msg = visual.TextStim(
            win=self.window,
            text=text,
            font='AppleGothic',
            height=28,
            color='white',
            wrapWidth=1000,
            anchorHoriz='center'
        )
        msg.draw()
        self.window.flip()
        
        if wait_for_key:
            event.waitKeys(keyList=keys if keys else ['space'])
        elif duration:
            core.wait(duration)
    
    def run_trial(self):
        """
        단일 시행 실행
        
        Returns
        -------
        int
            피험자 반응 (1: 높음, -1: 낮음, 0: 같음)
        """
        # 기준음과 비교음 생성
        gen = ToneGenerator()
        ref_waveform = gen.create_tone(self.reference_freq, 0.5)
        test_waveform = gen.create_tone(self.current_freq, 0.5)
        
        # 기준음 재생
        self.show_message("▶ 기준음 재생 중...", duration=0.1)
        gen.play_tone(ref_waveform)
        core.wait(0.3)  # ISI (Interstimulus Interval)
        
        # 비교음 재생
        self.show_message("▶ 비교음 재생 중...", duration=0.1)
        gen.play_tone(test_waveform)
        
        # 반응 수집
        response = self._get_response()
        
        # 시행 데이터 저장
        trial_data = {
            'trial': len(self.trials) + 1,
            'reference_freq': self.reference_freq,
            'test_freq': self.current_freq,
            'response': response,
            'response_label': ['낮음', '같음', '높음'][response + 1]
        }
        self.trials.append(trial_data)
        
        return response
    
    def _get_response(self):
        """반응 수집"""
        response_text = visual.TextStim(
            win=self.window,
            text="비교음이 기준음보다:\n\n"
                 "↑ (위쪽 화살표) = 높음\n"
                 "↓ (아래쪽 화살표) = 낮음\n"
                 "SPACE = 같음",
            font='AppleGothic',
            height=25,
            color='yellow',
            wrapWidth=900,
            anchorHoriz='center'
        )
        response_text.draw()
        self.window.flip()
        
        event.clearEvents()
        response = None
        while response is None:
            keys = event.getKeys(keyList=['up', 'down', 'space', 'escape'])
            
            if 'escape' in keys:
                return None
            if 'up' in keys:
                response = 1  # 높음
            elif 'down' in keys:
                response = -1  # 낮음
            elif 'space' in keys:
                response = 0  # 같음
            
            core.wait(0.01)
        
        return response
    
    def run(self, max_reversals=4):
        """
        상향식 방법 전체 실행
        
        Parameters
        ----------
        max_reversals : int
            정지할 역전(reversal) 수
        
        Returns
        -------
        bool
            실험 완료 여부
        """
        # 시작 메시지
        start_msg = (f"상향식 방법 시작\n\n"
                    f"기준음: {self.reference_freq}Hz\n"
                    f"시작 주파수: {self.current_freq}Hz\n\n"
                    f"스페이스를 누르면 시작합니다.")
        self.show_message(start_msg, wait_for_key=True)
        core.wait(0.5)
        
        reversals = 0
        last_response = None
        
        while reversals < max_reversals:
            # 시행 실행
            response = self.run_trial()
            
            if response is None:  # ESC로 실험 중단
                return False
            
            # 주파수 조정
            if response == 1:  # 비교음이 높음
                self.current_freq += self.step_size
            else:  # 비교음이 낮거나 같음
                self.current_freq -= self.step_size
            
            # 역전 감지
            if last_response is not None and last_response != response and last_response != 0:
                reversals += 1
                
                reversal_msg = f"✓ 역전 {reversals}/{max_reversals}"
                self.show_message(reversal_msg, duration=0.5)
            
            last_response = response
            
            # 범위 확인
            self.current_freq = max(self.reference_freq + 1, 
                                   min(self.current_freq, self.max_freq))
            
            # 진행 상황 표시
            progress_msg = (f"시행: {len(self.trials)}\n"
                          f"주파수: {self.current_freq:.1f}Hz\n"
                          f"반응: {['낮음', '같음', '높음'][response+1]}")
            self.show_message(progress_msg, duration=0.3)
        
        # 역치 계산
        self.estimate_threshold()
        return True
    
    def estimate_threshold(self):
        """역치 추정 (마지막 역전들의 평균)"""
        if len(self.trials) < 2:
            self.threshold = self.current_freq
            return
        
        # 마지막 역전들의 주파수 평균
        reversals_freqs = [trial['test_freq'] for trial in self.trials[-4:]]
        self.threshold = np.mean(reversals_freqs)


# ============================================================================
# 3. 결과 분석 및 시각화
# ============================================================================

def plot_results(trials, threshold, reference_freq, subject_id="S001", save_path='./data'):
    """
    실험 결과 시각화
    
    Parameters
    ----------
    trials : list
        시행 데이터 리스트
    threshold : float
        추정된 역치
    reference_freq : float
        기준음 주파수
    subject_id : str
        피험자 ID
    save_path : str
        저장 경로
    """
    os.makedirs(save_path, exist_ok=True)
    
    df = pd.DataFrame(trials)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'음향 판별 실험 결과 - {subject_id}', fontsize=14, fontweight='bold')
    
    # 그래프 1: 시행별 자극 주파수
    ax1.plot(df['trial'], df['test_freq'], 'o-', markersize=8, linewidth=2, 
             label='자극 주파수', color='#1f77b4')
    ax1.axhline(reference_freq, color='red', linestyle='--', linewidth=2, 
                label=f'기준음 ({reference_freq}Hz)')
    if threshold:
        ax1.axhline(threshold, color='green', linestyle='--', linewidth=2, 
                    label=f'추정 역치 ({threshold:.1f}Hz)')
    ax1.set_xlabel('시행 번호', fontsize=12)
    ax1.set_ylabel('주파수 (Hz)', fontsize=12)
    ax1.set_title('상향식 방법 - 주파수 변화', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    
    # 그래프 2: 반응 분포
    response_counts = df['response_label'].value_counts()
    colors = ['#ff9999', '#99ccff', '#99ff99']
    bars = ax2.bar(response_counts.index, response_counts.values, 
                   color=colors[:len(response_counts)], alpha=0.8)
    ax2.set_ylabel('횟수', fontsize=12)
    ax2.set_title('반응 분포', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 값 레이블 추가
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    # 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_file = os.path.join(save_path, f'{subject_id}_discrimination_{timestamp}.png')
    plt.savefig(save_file, dpi=150, bbox_inches='tight')
    print(f"\n📊 그래프가 저장되었습니다: {save_file}")
    plt.close()


# ============================================================================
# 4. 메인 함수
# ============================================================================

def main():
    """메인 함수 - PsychoPy GUI 모드로 실행"""
    
    print("\n" + "="*70)
    print("음향 판별 실험 (주파수 판별)")
    print("상향식 방법을 사용한 감각역치 추정")
    print("="*70)
    
    # GUI 대화상자로 피험자 정보 입력
    dlg = gui.DlgFromDict(
        dictionary={
            'Subject ID': 'S001',
            'Reference Frequency (Hz)': 440,
            'Start Frequency (Hz)': 300,
            'Step Size (Hz)': 5,
            'Max Reversals': 4
        },
        title='음향 판별 실험 (상향식 방법)',
        fixed=['Max Reversals']
    )
    
    if not dlg.OK:
        print("\n실험이 취소되었습니다.")
        return
    
    # dlg.data는 dictionary이므로 키로 접근
    try:
        subject_id = str(dlg.data['Subject ID']).strip()
        ref_freq = int(float(dlg.data['Reference Frequency (Hz)']))
        start_freq = int(float(dlg.data['Start Frequency (Hz)']))
        step_size = int(float(dlg.data['Step Size (Hz)']))
        max_reversals = int(float(dlg.data['Max Reversals']))
        
    except (ValueError, KeyError, TypeError) as e:
        print(f"\n❌ 입력 데이터 오류: {e}")
        print(f"수신된 데이터: {dlg.data}")
        return
    
    print(f"\n피험자 ID: {subject_id}")
    print(f"기준음 주파수: {ref_freq}Hz")
    print(f"시작 주파수: {start_freq}Hz")
    print(f"단계 크기: {step_size}Hz")
    print(f"최대 역전 수: {max_reversals}")
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
        # 지시문 표시
        instructions = visual.TextStim(
            win=window,
            text="음향 판별 실험\n\n"
                 "두 개의 음향 자극을 순서대로 듣게 됩니다.\n\n"
                 "1. 기준음 (440Hz 또는 입력한 주파수)\n"
                 "2. 비교음 (변함)\n\n"
                 "비교음이 기준음보다:\n"
                 "  ↑ = 높은가?\n"
                 "  ↓ = 낮은가?\n"
                 "  SPACE = 같은가?\n\n"
                 "준비가 되면 스페이스 바를 누르세요.",
            font='AppleGothic',
            height=28,
            color='white',
            wrapWidth=1100,
            anchorHoriz='center'
        )
        instructions.draw()
        window.flip()
        
        event.waitKeys(keyList=['space'])
        core.wait(0.5)
        
        # 실험 객체 생성 및 실행
        method = AscendingMethod(
            window=window,
            reference_freq=ref_freq,
            start_freq=start_freq,
            step_size=step_size
        )
        
        success = method.run(max_reversals=max_reversals)
        
        if success:
            # 결과 표시
            result_text = visual.TextStim(
                win=window,
                text=f"✓ 실험 완료!\n\n"
                     f"추정된 역치: {method.threshold:.1f}Hz\n"
                     f"기준음과의 차이: {method.threshold - ref_freq:.1f}Hz\n\n"
                     f"스페이스 바를 누르면 종료합니다.",
                font='AppleGothic',
                height=28,
                color='green',
                wrapWidth=1100,
                anchorHoriz='center'
            )
            result_text.draw()
            window.flip()
            
            event.waitKeys(keyList=['space'])
            
            # 데이터 저장
            df = pd.DataFrame(method.trials)
            os.makedirs('./data', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_file = f"./data/{subject_id}_discrimination_{timestamp}.csv"
            df.to_csv(csv_file, index=False)
            
            print(f"\n✓ 데이터가 저장되었습니다: {csv_file}")
            
            # 결과 시각화
            plot_results(method.trials, method.threshold, ref_freq, 
                        subject_id=subject_id)
            
            # 요약 통계 출력
            print(f"\n결과 요약:")
            print(f"  • 총 시행: {len(df)}")
            print(f"  • 추정 역치: {method.threshold:.1f}Hz")
            print(f"  • 기준음과의 차이: {method.threshold - ref_freq:.1f}Hz")
            print(f"  • 반응 분포:")
            print(f"    - 높음: {(df['response_label'] == '높음').sum()}회")
            print(f"    - 같음: {(df['response_label'] == '같음').sum()}회")
            print(f"    - 낮음: {(df['response_label'] == '낮음').sum()}회")
            print("\n" + "="*70)
        
        window.close()
    
    except KeyboardInterrupt:
        print("\n\n부주의로 실험이 중단되었습니다.")
        window.close()
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        window.close()


if __name__ == '__main__':
    main()
