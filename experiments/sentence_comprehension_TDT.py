#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentence Comprehension with Spatial Audio Experiment - TDT Integration

Participants listen to sentence audio from left and right speakers,
answer a comprehension question about the right-side audio.
Trigger signals are sent to TDT (Tucker-Davis Technologies) system during audio playback.

Requirements:
- tdt (TDT package): pip install tdt
- TDT RZ5 or RZ6 system with RPCo enabled
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

# Try to import tdt for TDT integration
TDT_AVAILABLE = False
SYNAPSE = None

try:
    import tdt
    TDT_AVAILABLE = True
    print("✓ tdt module found - TDT integration enabled")
except ImportError:
    print("⚠ tdt module not found - TDT integration disabled")
    print("  Install with: pip install tdt")


class TDTSynapseManager:
    """Manages communication with TDT Synapse via tdt package (SynapseAPI)."""
    
    def __init__(self):
        """Initialize TDT Synapse connection."""
        self.synapse = None
        self.connected = False
        self._connect()
    
    def _connect(self):
        """Connect to Synapse API."""
        if not TDT_AVAILABLE:
            print("⚠ TDT connection not available (tdt package not installed)")
            return
        
        print("=========== Setting Configuration ===========")
        try:
            # Connect to local Synapse API
            self.synapse = tdt.SynapseAPI()
            self.connected = True
            print("1. TDT Synapse connection successful")
        except Exception as e:
            print(f"TDT Synapse connection failed: {e}")
            print(f"  Make sure Synapse application is running.")
            # Abort experiment if TDT connection fails
            core.quit()
    
    def configure(self, subject_id, session):
        """Configure TDT Tank, Block, and start recording."""
        if not self.connected or self.synapse is None:
            return

        try:
            print("=========== TDT Configuration ===========")
            # 1. Switch to Idle mode first
            if self.synapse.getMode() != 0:
                self.synapse.setMode(0)
            
            # 2. Set User & Experiment
            user = "Psychopy"
            experiment = "SentenceComp"
            
            self.synapse.setCurrentUser(user)
            print(f"2. Setting user ({user}) done")
            self.synapse.setCurrentExperiment(experiment)
            print(f"3. Setting experiment ({experiment}) done")
            
            # 3. Tank Check
            current_tank = self.synapse.getCurrentTank()
            print(f"4. Tank setup ({current_tank}) done")
            
            # 4. Set Subject
            # createSubject(name, date_str, type)
            self.synapse.createSubject(subject_id, f'Session_{session}', 'Human')
            self.synapse.setCurrentSubject(subject_id)
            current_subject = self.synapse.getCurrentSubject()
            print(f"5. Subject setup ({current_subject}) done")
            
            # 5. Set Block
            clean_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            block_name = f"{subject_id}_S{session}_{clean_datetime}"
            self.synapse.setCurrentBlock(block_name)
            print(f"6. Block setup ({block_name}) done")
            
            # 6. Record Mode
            self.synapse.setMode(3)
            print("7. TDT Recording mode started")
            print("=========== TDT Configuration Done ===========")
            
        except Exception as e:
            print(f"⚠ TDT Configuration failed: {e}")
            core.quit()

    def stop_recording(self):
        """Stop TDT recording (switch to Idle)."""
        if self.connected and self.synapse:
            try:
                self.synapse.setMode(0)
                print("✓ TDT switched to Idle mode - Recording stopped")
            except Exception as e:
                print(f"⚠ Error stopping TDT recording: {e}")

    def send_trigger(self, trigger_value):
        """Send trigger signal to TDT system.
        
        Args:
            trigger_value: Integer value to send (from trg_table.xlsx)
        """
        if not self.connected or self.synapse is None:
            return False
        
        try:
            # Trigger sequence based on tutorial
            self.synapse.setParameterValue('TTL2Int1', 'IntegerValue', int(trigger_value))
            self.synapse.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
            core.wait(0.01)
            self.synapse.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
            
            print("=============================================")
            print(f"✓ Trigger sent: {trigger_value}")
            print("=============================================")
            return True
        except Exception as e:
            print(f"⚠ Failed to send trigger: {e}")
            return False
    
    def close(self):
        """Close Synapse connection."""
        if self.synapse is not None:
            self.stop_recording()
            try:
                self.synapse = None
                print("✓ Synapse connection closed")
            except Exception as e:
                print(f"⚠ Error closing connection: {e}")


class SentenceComprehensionExperimentTDT:
    """Sentence comprehension experiment with spatial audio and TDT integration."""
    
    def __init__(self, use_tdt=True):
        """Initialize experiment (window will be created after participant info is collected)."""
        # Initialize window as None (will be created in run() after collecting participant info)
        self.window = None
        self.screen_width = None
        self.screen_height = None
        self.scale = None
        self.scale_x = None
        self.scale_y = None
        
        self.clock = None
        self.data_list = []
        self.used_files = set()
        self.quiz_data = {}
        self.audio_files = []
        
        # Setup directories
        self.data_dir = 'data'
        self.stimuli_dir = 'stimuli'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Store TDT settings
        self.use_tdt = use_tdt
        self.tdt_manager = None
        
        # Load quiz data before window is created
        self._load_quiz_data()
        
        # Get available audio files
        self._get_audio_files()
    
    def _initialize_window(self, subject_id=None, session=None):
        """Initialize PsychoPy window and TDT connection."""
        # Detect screen resolution
        self.screen_width, self.screen_height = self._detect_screen_resolution()
        print(f"✓ Display resolution detected: {self.screen_width}x{self.screen_height}")
        
        # Create window at 100% of screen size (fullscreen)
        window_width = self.screen_width
        window_height = self.screen_height
        print(f"✓ Window size set to 100% (fullscreen): {window_width}x{window_height}")
        
        self.window = visual.Window(
            size=(window_width, window_height),
            color=[-1, -1, -1],
            units='pix',
            fullscr=True
        )
        
        # Update effective screen size for scaling calculations
        self.screen_width = window_width
        self.screen_height = window_height
        
        self.clock = core.Clock()
        
        # Calculate scaling factors based on screen size
        # Reference resolution: 1920x1080
        self.scale_x = self.screen_width / 1920
        self.scale_y = self.screen_height / 1080
        self.scale = min(self.scale_x, self.scale_y)  # Use minimum to maintain aspect ratio
        
        # Initialize TDT connection if requested
        if self.use_tdt and TDT_AVAILABLE:
            self.tdt_manager = TDTSynapseManager()
            if subject_id is not None:
                self.tdt_manager.configure(subject_id, session)
        elif self.use_tdt and not TDT_AVAILABLE:
            self.show_message(
                "⚠ TDT requested but tdt package not available\nContinuing without TDT",
                color=[1, 1, 0],
                duration=3
            )
        
        # Load quiz data
        self._load_quiz_data()
        
        # Load trigger mapping table
        self._load_trigger_table()
        
        # Get available audio files
        self._get_audio_files()
    
    def _detect_screen_resolution(self):
        """Detect monitor resolution automatically."""
        try:
            try:
                # Try using pyglet for cross-platform display detection
                import pyglet
                display = pyglet.canvas.get_display()
                screen = display.get_screens()[0]
                width = int(screen.width)
                height = int(screen.height)
                print(f"✓ Using pyglet to detect resolution: {width}x{height}")
                return width, height
            except Exception as e:
                print(f"⚠ pyglet detection failed ({e}), trying alternative method...")
                
                # Fallback: Try using screeninfo (if available)
                try:
                    import screeninfo
                    monitors = screeninfo.get_monitors()
                    if monitors:
                        monitor = monitors[0]
                        width = monitor.width
                        height = monitor.height
                        print(f"✓ Using screeninfo to detect resolution: {width}x{height}")
                        return width, height
                except Exception as e2:
                    print(f"⚠ screeninfo detection failed ({e2}), using default...")
                
                # Final fallback for macOS using Quartz
                try:
                    from Quartz import CGDisplayBounds
                    main_display_id = CGDisplayBounds(0)
                    width = int(main_display_id.size.width)
                    height = int(main_display_id.size.height)
                    print(f"✓ Using Quartz to detect resolution: {width}x{height}")
                    return width, height
                except Exception as e3:
                    print(f"⚠ Quartz detection failed ({e3}), using default resolution")
                    return 1920, 1080  # Default fallback
                    
        except Exception as e:
            print(f"⚠ Unexpected error in resolution detection: {e}")
            return 1920, 1080  # Default fallback
    
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
    
    def _load_trigger_table(self):
        """Load trigger table from Excel file to map audio files to trigger values."""
        trigger_file = 'trg_table.xlsx'
        self.trigger_table = {}
        try:
            df = pd.read_excel(trigger_file)
            for _, row in df.iterrows():
                filename = row['filename']
                trigger_val = int(row['trigger val'])
                self.trigger_table[filename] = trigger_val
            print(f"✓ Loaded {len(self.trigger_table)} trigger mappings from {trigger_file}")
        except Exception as e:
            print(f"⚠ Warning: Could not load trigger table ({trigger_file}): {e}")
            print("  Using default trigger values (1 for start, 0 for stop)")
            self.trigger_table = {}
    
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
                f"✗ Not enough audio files.\nFound {len(self.audio_files)}, need at least 2",
                color=[1, 0, 0]
            )
            core.quit()
        
        random.shuffle(self.audio_files)
        print(f"✓ Found {len(self.audio_files)} audio files")
    
    def get_trigger_value(self, filename):
        """Get trigger value for audio filename from trigger table.
        
        Args:
            filename: Audio filename (e.g., 'Sen_01.wav')
        
        Returns:
            Trigger value as integer, or None if not found
        """
        if filename in self.trigger_table:
            return self.trigger_table[filename]
        return None
    
    def show_message(self, message, color=None, duration=None, wait_key=None):
        """Display a message on screen with dynamic scaling."""
        if color is None:
            color = [1, 1, 1]
        
        # Scale text height based on screen resolution
        text_height = int(35 * self.scale)
        
        text_stim = visual.TextStim(
            self.window,
            text=message,
            font='AppleGothic',
            height=text_height,
            color=color,
            wrapWidth=int(self.screen_width * 0.9),
            anchorHoriz='center'
        )
        
        event.clearEvents()
        
        if duration is not None:
            # Show for specified duration
            start_time = self.clock.getTime()

            while self.clock.getTime() - start_time < duration:
                text_stim.draw()
                self.window.flip()
                core.wait(0.05)
        elif wait_key is not None:
            # Wait for key press
            while True:
                text_stim.draw()
                self.window.flip()
                keys = event.getKeys(keyList=[wait_key])
                if keys:
                    break
                core.wait(0.05)
        else:
            # Just display once
            text_stim.draw()
            self.window.flip()
    
    def show_instructions(self):
        """Show experimental instructions."""
        instructions = """
=== 문장 음성 이해 실험 ===

실험 절차:
1. 왼쪽과 오른쪽에서 각각 문장이 나옵니다
2. 오른쪽 문장이 끝난 후 문제가 나옵니다
3. 1, 2, 3, 4 중 정답 번호를 입력하세요
4. 모든 문제에 답할 때까지 반복됩니다

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
    
    def play_audio(self, stereo_data, sample_rate, right_file=None):
        """
        Play stereo audio and show crosshair fixation.
        Sends TDT trigger signal when audio starts (with value from trg_table.xlsx).
        """
        if stereo_data is None:
            return
        
        # Set background to gray
        self.window.color = [0.3, 0.3, 0.3]
        
        # Create crosshair with white color (scaled based on screen resolution)
        crosshair_size = int(17 * self.scale)  # Dynamic crosshair size
        circle_radius = int(2 * self.scale)    # Dynamic circle radius
        
        # Vertical line
        v_line = visual.Line(
            self.window,
            start=(0, crosshair_size),
            end=(0, -crosshair_size),
            lineColor=[1, 1, 1],
            lineWidth=2
        )
        # Horizontal line
        h_line = visual.Line(
            self.window,
            start=(crosshair_size, 0),
            end=(-crosshair_size, 0),
            lineColor=[1, 1, 1],
            lineWidth=2
        )
        # Center circle
        circle = visual.Circle(
            self.window,
            radius=circle_radius,
            fillColor=[1, 1, 1],
            lineColor=[1, 1, 1]
        )
        
        # Calculate duration
        duration = len(stereo_data) / sample_rate
        
        # Get trigger value from table for this audio file
        trigger_value = None
        if right_file is not None and self.tdt_manager is not None:
            trigger_value = self.get_trigger_value(right_file)
        
        # Send trigger signal START with appropriate value
        if self.tdt_manager is not None:
            if trigger_value is not None:
                print(f"\n>>> Sending TDT trigger START for {right_file}: value = {trigger_value} ({duration:.2f}s)")
                self.tdt_manager.send_trigger(trigger_value)
            else:
                print(f"\n>>> Sending TDT trigger START for audio playback ({duration:.2f}s)")
                print(f"    (No trigger value found for {right_file})")
        
        # Start playback in background thread
        event_flag = threading.Event()
        def play_thread():
            sd.play(stereo_data, samplerate=sample_rate)
            sd.wait()
            event_flag.set()
        
        thread = threading.Thread(target=play_thread, daemon=True)
        thread.start()
        
        start_time = self.clock.getTime()
        
        # Show crosshair during playback
        while self.clock.getTime() - start_time < duration:
            v_line.draw()
            h_line.draw()
            circle.draw()
            self.window.flip()
            core.wait(0.05)
        
        # Wait for playback to finish
        event_flag.wait(timeout=1.0)
        
        # Send trigger signal STOP (value = 0)
        if self.tdt_manager is not None:
            print(f">>> Sending TDT trigger STOP after audio playback (value = 0)")
            self.tdt_manager.send_trigger(0)
        
        self.window.color = [-1, -1, -1]  # Reset background
    
    def show_quiz(self, right_file):
        """Show and collect quiz response with latency measurement with dynamic scaling."""
        if right_file not in self.quiz_data:
            return None, None, None
        
        quiz_info = self.quiz_data[right_file]
        quiz_text = quiz_info['quiz']
        options = quiz_info['options']
        correct_answer = quiz_info['answer']  # Get correct answer
        
        # Scale text and positions based on screen resolution
        question_height = int(35 * self.scale)
        option_height = int(28 * self.scale)
        instruction_height = int(24 * self.scale)
        wrap_width = int(self.screen_width * 0.85)
        
        # Scale y positions
        question_y = int(250 * self.scale_y)
        option_y_positions = [int(y * self.scale_y) for y in [150, 50, -50, -150]]
        instruction_y = int(-280 * self.scale_y)
        
        # Prepare quiz display
        question_text = visual.TextStim(
            self.window,
            text=f"문제: {quiz_text}",
            font='AppleGothic',
            height=question_height,
            color=[1, 1, 1],
            pos=(0, question_y),
            wrapWidth=wrap_width,
            anchorHoriz='center'
        )
        
        # Display options
        option_stims = []
        for i, (option, y) in enumerate(zip(options, option_y_positions)):
            opt_text = visual.TextStim(
                self.window,
                text=f"{i+1}. {option}",
                font='AppleGothic',
                height=option_height,
                color=[1, 1, 1],
                pos=(0, y),
                wrapWidth=wrap_width,
                anchorHoriz='center'
            )
            option_stims.append(opt_text)
        
        instruction_text = visual.TextStim(
            self.window,
            text="1, 2, 3, 4 중 정답 번호를 입력하세요",
            font='AppleGothic',
            height=instruction_height,
            color=[1, 1, 0],
            pos=(0, instruction_y),
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
        
        # Play audio (with TDT trigger signals based on right_file)
        self.play_audio(stereo_data, sample_rate, right_file=right_file)
        
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
        # Get participant info FIRST (before window initialization)
        print(f"\n{'='*50}")
        print("피험자 정보 입력 중...")
        print(f"{'='*50}\n")
        
        dlg = gui.DlgFromDict(
            {'Subject ID': 'S001', 'Session': 1},
            title='Sentence Comprehension Experiment (TDT Integration)'
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
        
        print(f"\n{'='*50}")
        print(f"실험 참가자 정보")
        print(f"{'='*50}")
        print(f"Subject ID: {subject_id}")
        print(f"Session: {session}")
        print(f"{'='*50}\n")
        
        # NOW initialize the window and TDT after participant info is collected
        print("PsychoPy 화면 초기화 중...")
        self._initialize_window(subject_id, session)
        print("✓ PsychoPy 화면 준비 완료\n")
        
        # Show experiment screen ready message
        self.show_message(
            "📊 실험 화면으로 이동합니다\n\n스페이스바를 누르면 시작합니다",
            color=[1, 1, 1],
            wait_key='space'
        )
        
        # Show TDT status
        if self.tdt_manager is not None:
            if self.tdt_manager.connected:
                self.show_message(
                    "✓ TDT Connected\n\nTrigger signals will be sent during audio playback",
                    color=[0, 1, 0],
                    duration=2
                )
            else:
                self.show_message(
                    "⚠ TDT Not Connected\n\nRunning experiment without trigger signals",
                    color=[1, 1, 0],
                    duration=2
                )
        
        # Show instructions
        self.show_instructions()
        
        # Calculate number of trials
        num_trials = len(self.audio_files) // 2
        
        try:
            # Run trials
            trial_count = 0
            for trial_num in range(1, num_trials + 1):
                success = self.run_trial(trial_num, num_trials)
                if success:
                    trial_count += 1
                    # Save data after every trial to prevent data loss
                    self.save_data(subject_id, session)
                else:
                    break
            
            # Show completion message
            self.show_message(
                f"✓ 실험 완료!\n총 {trial_count}/{num_trials} 시행 완료",
                color=[0, 1, 0],
                duration=2
            )
            
            # Plot results
            self.plot_results()
            
        finally:
            # Close TDT connection and Window safely
            if self.tdt_manager is not None:
                self.tdt_manager.close()
            
            if self.window is not None:
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
        filename = os.path.join(self.data_dir, f"sentence_comprehension_TDT_{timestamp}.png")
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Results saved: {filename}")


if __name__ == '__main__':
    # Run experiment with TDT integration
    # Parameters:
    #   use_tdt: Enable TDT trigger signals (default: True) 
    
    exp = SentenceComprehensionExperimentTDT(
        use_tdt=True           # Set to False to disable TDT
    )
    exp.run()
