#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Refactored Tutorial Experiment for EEG/Psychophysics
----------------------------------------------------
This script runs a tutorial experiment involving TDT integration, Audio playback, and EEG impedance checking.

Structure:
1. TDTManager: Handles connection to TDT Synapse and sending triggers.
2. TutorialExperiment: Manages the PsychoPy window, stimuli, and experiment flow.

How to add a new routine:
1. Define a new method in TutorialExperiment (e.g., `run_new_task(self)`).
2. Inside, set up your stimuli (text, sound, etc.).
3. Use `self.present_routine()` to show text/wait for keys.
4. Add `self.run_new_task()` to the `run()` method sequence.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
import numpy as np
import pandas as pd

from psychopy import visual, core, event, data, gui, sound, logging, prefs
from psychopy.hardware import keyboard

# TDT Integration
try:
    import tdt
    TDT_AVAILABLE = True
except ImportError:
    TDT_AVAILABLE = False
    print("Warning: 'tdt' package not found. TDT integration disabled.")


class TDTManager:
    """Manages TDT Synapse connection and triggers."""
    def __init__(self, gizmo='TTL2Int1'):
        self.syn = None
        self.gizmo = gizmo
        self.connected = False
        
        if TDT_AVAILABLE:
            try:
                self.syn = tdt.SynapseAPI()
                self.connected = True
                print("✓ TDT Synapse Connected")
            except Exception as e:
                print(f"⚠ TDT Connection Failed: {e}")

    def configure(self, user, experiment, subject, block):
        """Configure TDT Tank, Block, and Subject."""
        if not self.connected: return
        try:
            if self.syn.getMode() != 0:
                self.syn.setMode(0)  # Idle
            
            self.syn.setCurrentUser(user)
            self.syn.setCurrentExperiment(experiment)
            self.syn.createSubject(subject, f'datetime_{datetime.now().strftime("%Y%m%d")}', 'mouse')
            self.syn.setCurrentSubject(subject)
            self.syn.setCurrentBlock(block)
            print(f"✓ TDT Configured: {experiment} / {subject} / {block}")
        except Exception as e:
            print(f"⚠ TDT Configuration Error: {e}")

    def start_recording(self):
        if self.connected:
            self.syn.setMode(3)  # Record
            print("✓ TDT Recording Started")

    def stop_recording(self):
        if self.connected:
            self.syn.setMode(0)  # Idle
            print("✓ TDT Recording Stopped")

    def send_trigger(self, val):
        """Send a pulse trigger."""
        if not self.connected: return
        try:
            self.syn.setParameterValue(self.gizmo, 'IntegerValue', int(val))
            self.syn.setParameterValue(self.gizmo, 'ManualTrigger', 1)
            core.wait(0.01)
            self.syn.setParameterValue(self.gizmo, 'ManualTrigger', 0)
            print(f"  -> Trigger Sent: {val}")
        except Exception as e:
            print(f"⚠ Trigger Error: {e}")


class TutorialExperiment:
    """Main experiment class handling window, stimuli, and flow."""
    
    def __init__(self):
        # 1. Setup Window
        self.win = visual.Window(
            size=[1920, 1080], fullscr=True, screen=0,
            winType='pyglet', allowGUI=False,
            color=[0, 0, 0], units='height'
        )
        self.win.mouseVisible = False
        
        # 2. Setup Input
        self.keyboard = keyboard.Keyboard()
        
        # 3. Setup Audio
        prefs.hardware['audioLib'] = 'pygame'
        self.sound = sound.Sound('A', secs=-1, stereo=True)
        
        # 4. Setup TDT
        self.tdt = TDTManager()
        
        # 5. Common Stimuli (Reuse these)
        self.text_stim = visual.TextStim(self.win, text='', height=0.05, color='white')
        
        # 6. Data Handler
        self.exp_info = {'participant': '999999', 'session': '001'}
        self.this_exp = None
        
        # Paths
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

    def show_dialog(self):
        """Show participant info dialog."""
        dlg = gui.DlgFromDict(dictionary=self.exp_info, title='Tutorial Experiment')
        if not dlg.OK:
            core.quit()
        
        # Setup Data Saving
        data_dir = os.path.join(self.root_dir, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        date_str = data.getDateStr()
        filename = os.path.join(data_dir, f"{self.exp_info['participant']}_Tutorial_{date_str}")
        self.this_exp = data.ExperimentHandler(
            name='Tutorial', version='2.0',
            extraInfo=self.exp_info,
            dataFileName=filename,
            savePickle=True, saveWideText=True
        )

    def present_routine(self, text=None, duration=None, key_list=None, trigger=None):
        """
        Generic routine runner.
        - Displays text (optional)
        - Sends trigger at start (optional)
        - Waits for duration OR key press
        """
        # Setup
        if text:
            self.text_stim.text = text
        
        # Send Trigger
        if trigger is not None:
            self.tdt.send_trigger(trigger)
            
        # Clear events
        self.keyboard.clearEvents()
        timer = core.Clock()
        keys = []
        
        # Loop
        while True:
            # Draw
            if text:
                self.text_stim.draw()
            self.win.flip()
            
            # Check Time
            if duration and timer.getTime() >= duration:
                break
                
            # Check Keys
            if key_list:
                keys = self.keyboard.getKeys(keyList=key_list, waitRelease=False)
                if keys:
                    break
            
            # Escape check
            if 'escape' in event.getKeys():
                self.cleanup()
                core.quit()
                
        return keys

    def run_start(self):
        """Start Routine."""
        # TDT Configuration
        clean_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        block_name = f"{self.exp_info['participant']}_{clean_datetime}"
        
        self.tdt.configure("Tutorial", "Tutorial", self.exp_info['participant'], block_name)
        self.tdt.start_recording()
        self.tdt.send_trigger(9999)  # EXP_START
        
        msg = ("Tutorial start.\n\n"
               "- Setting up experiment successful.\n"
               "- Connecting TDT and configuring settings successful.\n\n"
               "(If you are willing to proceed, please press '0'.)")
        self.present_routine(text=msg, key_list=['0'])

    def run_gelling(self):
        """Gelling Routine with external app launch."""
        self.tdt.send_trigger(9000)  # GELLING_START
        
        msg = "(If gelling is finished and you are willing to proceed, please press '9'.)"
        
        # Launch Impedance Checker
        # Windows 환경 설정: 임피던스 체커 경로 (실제 경로 확인 필요)
        imp_path = "C:/Users/KIST/Desktop/임피던스체커 패키지/check_realtime_imp.exe"
        proc = None
        if os.path.exists(imp_path):
            self.win.winHandle.minimize()
            try:
                proc = subprocess.Popen([imp_path])
                print("Launched Impedance Checker")
            except Exception as e:
                print(f"Failed to launch checker: {e}")
        
        # Wait for key
        self.present_routine(text=msg, key_list=['9'])
        
        # Cleanup
        if proc:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)])
        self.win.winHandle.activate()
        self.win.winHandle.maximize()
        
        self.tdt.send_trigger(9001)  # GELLING_END
        
        # Gelling End Message (20s wait)
        msg_wait = "It takes about 20 seconds to stabilize EEG signals..."
        self.present_routine(text=msg_wait, duration=20.0)

    def run_erp_block(self):
        """ERP Block Loop."""
        self.present_routine(text="ERP session starts.\nPress '0' to continue.", key_list=['0'], trigger=8000)
        
        # Load Conditions
        cond_file = os.path.join(self.root_dir, 'erp_stimuli', 'erp_stimuli.csv')
        if not os.path.exists(cond_file):
            print(f"Error: {cond_file} not found.")
            return
            
        trials = data.importConditions(cond_file)
        
        for trial in trials:
            # 1. Trigger & Sound
            trig_id = int(trial['trigger_id'])
            sound_file = trial['fname']
            isi = float(trial['isi']) if 'isi' in trial else 1.0
            
            self.tdt.send_trigger(trig_id)
            
            # Play sound
            self.sound.setSound(sound_file)
            self.sound.play()
            
            # Show fixation during sound
            self.present_routine(text='+', duration=self.sound.getDuration())
            
            # ISI
            self.present_routine(text='.', duration=isi)
            
            # Save data
            self.this_exp.addData('trigger_id', trig_id)
            self.this_exp.nextEntry()
            
        self.present_routine(text="ERP session finished.\nPress '0'.", key_list=['0'], trigger=8999)

    def run_main_block(self):
        """Main Block Loop with Quiz."""
        self.present_routine(text="Main session starts.\nPress '0'.", key_list=['0'], trigger=0)
        
        cond_file = os.path.join(self.root_dir, 'main_stimuli', 'main_stimuli.csv')
        if not os.path.exists(cond_file):
            return
            
        trials = data.importConditions(cond_file)
        
        for trial in trials:
            trig_id = int(trial['trigger_id'])
            sound_file = trial['fname']
            ans = str(trial['ans'])
            quiz_content = trial['quiz_content']
            
            # 1. Stimulus
            self.tdt.send_trigger(trig_id)
            self.sound.setSound(sound_file)
            self.sound.play()
            self.present_routine(text='+', duration=self.sound.getDuration())
            
            # 2. Quiz
            quiz_trig = trig_id + 1000
            self.tdt.send_trigger(quiz_trig)
            
            keys = self.present_routine(text=quiz_content, key_list=['1','2','3','4'])
            
            # Check Answer
            resp = keys[0].name if keys else None
            corr = 1 if resp == ans else 0
            
            # Feedback Trigger
            fb_trig = 2001 if corr else 2002
            self.tdt.send_trigger(fb_trig)
            
            # 3. Rest
            self.present_routine(text="Rest.\nPress '0' to continue.", key_list=['0'])
            
            # Save
            self.this_exp.addData('main_trigger', trig_id)
            self.this_exp.addData('response', resp)
            self.this_exp.addData('correct', corr)
            self.this_exp.nextEntry()
            
        self.present_routine(text="Main session finished.\nPress '0'.", key_list=['0'], trigger=1999)

    def run_finish(self):
        """Finish Routine."""
        self.present_routine(text="Please wait... Wrapping up.", duration=10.0)
        
        self.tdt.send_trigger(9998) # EXP_END
        self.tdt.stop_recording()
        
        self.present_routine(text="Experiment Completed.\nPress '0' to exit.", key_list=['0'])
        self.cleanup()

    def cleanup(self):
        """Close window and save."""
        if self.this_exp:
            self.this_exp.close()
        self.win.close()
        core.quit()

    def run(self):
        """Main Execution Flow."""
        self.show_dialog()
        
        # --- Experiment Sequence ---
        self.run_start()
        self.run_gelling()
        self.run_erp_block()
        self.run_main_block()
        self.run_finish()


if __name__ == '__main__':
    exp = TutorialExperiment()
    exp.run()