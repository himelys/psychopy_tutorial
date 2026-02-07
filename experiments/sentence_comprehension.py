#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentence Comprehension with Spatial Audio Experiment

Participants listen to sentence audio from left and right speakers,
answer a comprehension question about the right-side audio,
and results are recorded for analysis.
"""

import os
import sys
import random
import csv
import threading
from datetime import datetime
import numpy as np
import pandas as pd
import soundfile as sf
import sounddevice as sd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend first
import matplotlib.pyplot as plt
# Configure matplotlib for Korean font display on macOS
# Apply BOTH matplotlib and plt rcParams for compatibility
matplotlib.rcParams['font.sans-serif'] = ['AppleSDGothicNeo', 'AppleGothic', 'Helvetica']
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['AppleSDGothicNeo', 'AppleGothic', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11

from scipy import signal as scipy_signal
from psychopy import visual, event, core, gui, data, logging

# Suppress warnings
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import warnings
warnings.filterwarnings('ignore')
logging.console.setLevel(logging.WARNING)


class SentenceComprehensionExperiment:
    """Sentence comprehension experiment with spatial audio."""
    
    def __init__(self):
        """Initialize experiment."""
        self.window = visual.Window(size=(1200, 800), color=[-1, -1, -1], units='pix')
        self.clock = core.Clock()
        self.data_list = []
        self.used_files = set()
        self.quiz_data = {}
        self.audio_files = []
        
        # Setup directories
        self.data_dir = 'data'
        self.stimuli_dir = 'stimuli'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Load quiz data
        self._load_quiz_data()
        
        # Get available audio files
        self._get_audio_files()
    
    def _load_quiz_data(self):
        """Load quiz data from Excel file."""
        quiz_file = 'quiz.xlsx'
        try:
            df = pd.read_excel(quiz_file)
            for _, row in df.iterrows():
                filename = row['filename']
                self.quiz_data[filename] = {
                    'quiz': row['quiz'],
                    'options': [row[1], row[2], row[3], row[4]],
                    'answer': int(row['정답'])  # Load correct answer (1, 2, 3, or 4)
                }
            print(f"✓ Loaded {len(self.quiz_data)} quiz items with answers")
        except Exception as e:
            self.show_message(f"✗ Error loading quiz.xlsx: {str(e)}", color=[1, 0, 0])
            core.quit()
    
    def _get_audio_files(self):
        """Get list of available audio files from stimuli folder."""
        if not os.path.exists(self.stimuli_dir):
            os.makedirs(self.stimuli_dir)
            self.show_message(
                f"✗ Stimuli folder is empty.\nPlace .wav files in '{self.stimuli_dir}/' folder",
                color=[1, 0, 0]
            )
            core.quit()
        
        # Get all .wav and .mp3 files
        self.audio_files = [
            f for f in os.listdir(self.stimuli_dir)
            if f.lower().endswith(('.wav', '.mp3')) and f in self.quiz_data
        ]
        
        if len(self.audio_files) < 2:
            self.show_message(
                f"✗ Need at least 2 audio files in '{self.stimuli_dir}/' folder\n"
                f"Found: {len(self.audio_files)}",
                color=[1, 0, 0]
            )
            core.quit()
        
        print(f"✓ Found {len(self.audio_files)} audio files")
        print(f"  Number of trials: {len(self.audio_files) // 2}")
    
    def show_message(self, message, color=None, wait_key=None, duration=None):
        """Display a message on screen."""
        if color is None:
            color = [1, 1, 1]  # white
        
        text = visual.TextStim(
            self.window,
            text=message,
            font='AppleGothic',
            height=30,
            color=color,
            wrapWidth=1000,
            anchorHoriz='center'
        )
        
        text.draw()
        self.window.flip()
        
        if duration:
            core.wait(duration)
        elif wait_key:
            event.clearEvents()
            while True:
                keys = event.getKeys()
                if wait_key in keys:
                    break
                core.wait(0.01)
        
        event.clearEvents()
    
    def show_instructions(self):
        """Show experiment instructions."""
        instructions = """
문장 음성 이해 실험

🎧 실험 설명:
• 매 시행마다 좌우 스피커에서 다른 음원이 들립니다
• 오른쪽 음원이 끝난 후 그 음원에 대한 문제가 제시됩니다
• 1, 2, 3, 4 숫자키로 정답을 선택해주세요
• 모든 시행이 끝날 때까지 계속됩니다

⏱️ 시간: 약 10-15분
🔊 헤드폰을 착용하고 시작해주세요

스페이스바를 누르면 시작합니다
        """
        self.show_message(instructions, color=[1, 1, 1], wait_key='space')
    
    def select_trial_stimuli(self):
        """Select two unused audio files for current trial."""
        available = [f for f in self.audio_files if f not in self.used_files]
        
        if len(available) < 2:
            return None, None
        
        selected = random.sample(available, 2)
        for f in selected:
            self.used_files.add(f)
        
        return selected[0], selected[1]
    
    def _resample_audio(self, audio_data, original_sr, target_sr):
        """Resample audio to target sample rate."""
        if original_sr == target_sr:
            return audio_data
        
        # Calculate resampling ratio
        ratio = target_sr / original_sr
        num_samples = int(len(audio_data) * ratio)
        
        # Resample using scipy
        resampled = scipy_signal.resample(audio_data, num_samples)
        return resampled.astype(np.float32)
    
    def load_stereo_audio(self, left_file, right_file):
        """Load audio files and create stereo channel."""
        left_path = os.path.join(self.stimuli_dir, left_file)
        right_path = os.path.join(self.stimuli_dir, right_file)
        
        target_sr = 44100  # Target sample rate
        
        try:
            # Load both audio files using soundfile
            left_data, sr_left = sf.read(left_path)
            right_data, sr_right = sf.read(right_path)
            
            # Convert to mono if stereo
            if len(left_data.shape) > 1:
                left_data = np.mean(left_data, axis=1)
            if len(right_data.shape) > 1:
                right_data = np.mean(right_data, axis=1)
            
            # Resample if necessary
            if sr_left != target_sr:
                print(f"  Resampling {left_file}: {sr_left}Hz → {target_sr}Hz")
                left_data = self._resample_audio(left_data, sr_left, target_sr)
            
            if sr_right != target_sr:
                print(f"  Resampling {right_file}: {sr_right}Hz → {target_sr}Hz")
                right_data = self._resample_audio(right_data, sr_right, target_sr)
            
            # Use target sample rate
            sr = target_sr
            
            # Pad to same length
            max_len = max(len(left_data), len(right_data))
            left_padded = np.zeros(max_len)
            right_padded = np.zeros(max_len)
            left_padded[:len(left_data)] = left_data
            right_padded[:len(right_data)] = right_data
            
            # Create stereo audio (left channel, right channel)
            # Shape should be (samples, channels)
            stereo_data = np.column_stack((left_padded, right_padded))
            
            return stereo_data, sr, right_file
        except Exception as e:
            print(f"✗ Error loading audio: {e}")
            return None, None, None
    
    def show_trial_start(self):
        """Show trial start screen."""
        message = "다음 시행을 시작합니다\n\n스페이스바를 눌러주세요"
        self.show_message(message, color=[1, 1, 1], wait_key='space')
    
    def play_audio(self, stereo_data, sample_rate):
        """Play stereo audio and show countdown."""
        if stereo_data is None:
            return
        
        self.window.color = [-0.5, -0.5, -0.5]  # Slightly lighter background
        
        # Show "listening" indicator
        listening_text = visual.TextStim(
            self.window,
            text="🎧 음원을 듣고 있습니다...",
            font='AppleGothic',
            height=40,
            color=[0, 1, 0]
        )
        
        # Calculate duration
        duration = len(stereo_data) / sample_rate
        
        # Start playback in background thread
        event_flag = threading.Event()
        def play_thread():
            sd.play(stereo_data, samplerate=sample_rate)
            sd.wait()
            event_flag.set()
        
        thread = threading.Thread(target=play_thread, daemon=True)
        thread.start()
        
        start_time = self.clock.getTime()
        
        # Show progress during playback
        while self.clock.getTime() - start_time < duration:
            elapsed = self.clock.getTime() - start_time
            remaining = duration - elapsed
            
            listening_text.text = f"🎧 음원을 듣고 있습니다... ({remaining:.1f}초 남음)"
            listening_text.draw()
            self.window.flip()
            core.wait(0.05)
        
        # Wait for playback to finish
        event_flag.wait(timeout=1.0)
        
        self.window.color = [-1, -1, -1]  # Reset background
    
    def show_quiz(self, right_file):
        """Show and collect quiz response with latency measurement."""
        if right_file not in self.quiz_data:
            return None, None, None
        
        quiz_info = self.quiz_data[right_file]
        quiz_text = quiz_info['quiz']
        options = quiz_info['options']
        correct_answer = quiz_info['answer']  # Get correct answer
        
        # Prepare quiz display
        question_text = visual.TextStim(
            self.window,
            text=f"문제: {quiz_text}",
            font='AppleGothic',
            height=35,
            color=[1, 1, 1],
            pos=(0, 250),
            wrapWidth=1000,
            anchorHoriz='center'
        )
        
        # Display options
        option_stims = []
        y_positions = [150, 50, -50, -150]
        for i, (option, y) in enumerate(zip(options, y_positions)):
            opt_text = visual.TextStim(
                self.window,
                text=f"{i+1}. {option}",
                font='AppleGothic',
                height=28,
                color=[1, 1, 1],
                pos=(0, y),
                wrapWidth=1000,
                anchorHoriz='center'
            )
            option_stims.append(opt_text)
        
        instruction_text = visual.TextStim(
            self.window,
            text="1, 2, 3, 4 중 정답 번호를 입력하세요",
            font='AppleGothic',
            height=24,
            color=[1, 1, 0],
            pos=(0, -280),
            anchorHoriz='center'
        )
        
        # Collect response with latency measurement
        event.clearEvents()
        response = None
        response_time = None
        latency = None
        response_start_time = self.clock.getTime()  # Start timing when quiz appears
        
        while response is None:
            question_text.draw()
            for opt in option_stims:
                opt.draw()
            instruction_text.draw()
            self.window.flip()
            
            keys = event.getKeys(keyList=['1', '2', '3', '4'])
            if keys:
                response = int(keys[0])
                response_time = self.clock.getTime()
                latency = response_time - response_start_time  # Calculate latency
            
            core.wait(0.01)
        
        return response, latency, correct_answer
    
    def run_trial(self, trial_num, total_trials):
        """Run a single trial."""
        # Select stimuli
        left_file, right_file = self.select_trial_stimuli()
        if left_file is None:
            return False
        
        # Show trial start screen
        self.show_trial_start()
        
        # Load stereo audio
        stereo_data, sample_rate, right_file_confirmed = self.load_stereo_audio(left_file, right_file)
        if stereo_data is None:
            return False
        
        # Play audio
        self.play_audio(stereo_data, sample_rate)
        
        # Brief pause after audio
        core.wait(0.5)
        
        # Show quiz and collect response
        response, latency, correct_answer = self.show_quiz(right_file)
        
        # Calculate accuracy
        is_correct = (response == correct_answer)
        
        # Record trial data
        self.data_list.append({
            'trial_num': trial_num,
            'total_trials': total_trials,
            'left_file': left_file,
            'right_file': right_file,
            'correct_answer': correct_answer,
            'user_response': response,
            'is_correct': is_correct,
            'latency_sec': latency,
            'timestamp': datetime.now().isoformat()
        })
        
        return True
    
    def run(self):
        """Run the entire experiment."""
        # Get participant info
        dlg = gui.DlgFromDict(
            {'Subject ID': 'S001', 'Session': 1},
            title='Sentence Comprehension Experiment'
        )
        
        if not dlg.OK:
            core.quit()
            return
        
        try:
            subject_id = str(dlg.data[0])
            session = int(dlg.data[1])
        except:
            subject_id = str(dlg.data['Subject ID'])
            session = int(float(dlg.data['Session']))
        
        # Show instructions
        self.show_instructions()
        
        # Calculate number of trials
        num_trials = len(self.audio_files) // 2
        
        # Run trials
        trial_count = 0
        for trial_num in range(1, num_trials + 1):
            success = self.run_trial(trial_num, num_trials)
            if success:
                trial_count += 1
            else:
                break
        
        # Save data
        self.save_data(subject_id, session)
        
        # Show completion message
        self.show_message(
            f"✓ 실험 완료!\n총 {trial_count}/{num_trials} 시행 완료",
            color=[0, 1, 0],
            duration=2
        )
        
        # Plot results
        self.plot_results()
        
        self.window.close()
    
    def save_data(self, subject_id, session):
        """Save experimental data to CSV."""
        if not self.data_list:
            print("✗ No data to save")
            return
        
        df = pd.DataFrame(self.data_list)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.data_dir, f"{subject_id}_session{session}_{timestamp}.csv")
        
        df.to_csv(filename, index=False)
        print(f"✓ Data saved: {filename}")
    
    def plot_results(self):
        """Plot experimental results."""
        if not self.data_list:
            return
        
        df = pd.DataFrame(self.data_list)
        
        # Calculate statistics
        accuracy = df['is_correct'].mean() * 100
        avg_latency = df['latency_sec'].mean()
        
        print()
        print("=" * 50)
        print("실험 결과 통계")
        print("=" * 50)
        print(f"총 시행 수: {len(df)}")
        print(f"정확도: {accuracy:.1f}% ({df['is_correct'].sum()}/{len(df)})")
        print(f"평균 반응 시간: {avg_latency:.2f}초")
        print(f"최소 반응 시간: {df['latency_sec'].min():.2f}초")
        print(f"최대 반응 시간: {df['latency_sec'].max():.2f}초")
        print("=" * 50)
        print()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Accuracy over trials
        ax1.plot(df['trial_num'], df['is_correct'].astype(int), 'go-', linewidth=2, markersize=8)
        ax1.set_xlabel('Trial Number', fontsize=11)
        ax1.set_ylabel('Correct (1) / Incorrect (0)', fontsize=11)
        ax1.set_title('정확도 변화 (Accuracy Over Trials)', fontsize=12, fontweight='bold')
        ax1.set_ylim(-0.1, 1.1)
        ax1.grid(True, alpha=0.3)
        
        # 2. Latency over trials
        ax2.plot(df['trial_num'], df['latency_sec'], 'bs-', linewidth=2, markersize=8)
        ax2.set_xlabel('Trial Number', fontsize=11)
        ax2.set_ylabel('Latency (seconds)', fontsize=11)
        ax2.set_title('반응 시간 변화 (Latency Over Trials)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. Latency distribution histogram
        ax3.hist(df['latency_sec'], bins=10, color='skyblue', edgecolor='black')
        ax3.axvline(avg_latency, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg_latency:.2f}s')
        ax3.set_xlabel('Latency (seconds)', fontsize=11)
        ax3.set_ylabel('Frequency', fontsize=11)
        ax3.set_title('반응 시간 분포 (Latency Distribution)', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.legend()
        
        # 4. Accuracy summary
        correct_count = df['is_correct'].sum()
        incorrect_count = len(df) - correct_count
        colors = ['#2ecc71', '#e74c3c']
        sizes = [correct_count, incorrect_count]
        labels = [f'맞음 ({correct_count})', f'틀림 ({incorrect_count})']
        
        ax4.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
        ax4.set_title(f'정확도 요약 ({accuracy:.1f}%)', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        # Save figure
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.data_dir, f"sentence_comprehension_{timestamp}.png")
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Results saved: {filename}")
        
        plt.show()


if __name__ == '__main__':
    exp = SentenceComprehensionExperiment()
    exp.run()
