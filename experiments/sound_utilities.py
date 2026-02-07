#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sound Generation and Analysis Utilities
========================================
음향 자극 생성 및 분석을 위한 유틸리티 함수 모음

주요 기능:
- 다양한 종류의 음향 자극 생성 (순음, 소음 등)
- 음향 신호 처리 (필터링, 변조 등)
- 청각 신호 분석

Author: PsychoPy Utility
Version: 1.0
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

try:
    from psychopy import sound
    PSYCHOPY_AVAILABLE = True
except ImportError:
    PSYCHOPY_AVAILABLE = False


# ============================================================================
# 1. 기본 음향 자극 생성
# ============================================================================

class ToneGenerator:
    """다양한 종류의 순음 생성"""
    
    @staticmethod
    def pure_tone(frequency, duration, volume=0.3, sr=44100):
        """
        순음(Pure Tone) 생성
        
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
            음성 신호
        """
        n_samples = int(sr * duration)
        t = np.linspace(0, duration, n_samples, False)
        waveform = np.sin(2 * np.pi * frequency * t) * volume
        return waveform
    
    @staticmethod
    def sweep_tone(freq_start, freq_end, duration, volume=0.3, sr=44100):
        """
        스윕음(Sweep Tone) 생성 - 주파수가 변하는 음
        
        Parameters
        ----------
        freq_start : float
            시작 주파수 (Hz)
        freq_end : float
            종료 주파수 (Hz)
        duration : float
            지속 시간 (초)
        volume : float
            음량 (0~1)
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        numpy.ndarray
            음성 신호
        """
        n_samples = int(sr * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        # 주파수 선형 변화
        frequency = np.linspace(freq_start, freq_end, n_samples)
        
        # 위상 계산 (frequency의 적분)
        phase = 2 * np.pi * np.cumsum(frequency) / sr
        
        waveform = np.sin(phase) * volume
        return waveform
    
    @staticmethod
    def complex_tone(frequencies, amplitudes, duration, sr=44100):
        """
        복합음(Complex Tone) 생성 - 여러 주파수의 조합
        
        Parameters
        ----------
        frequencies : list or array
            주파수 리스트 (Hz)
        amplitudes : list or array
            각 주파수의 진폭 리스트 (합이 1.0 이하)
        duration : float
            지속 시간 (초)
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        numpy.ndarray
            음성 신호
        """
        n_samples = int(sr * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        waveform = np.zeros(n_samples)
        
        for freq, amp in zip(frequencies, amplitudes):
            waveform += np.sin(2 * np.pi * freq * t) * amp
        
        return waveform
    
    @staticmethod
    def white_noise(duration, volume=0.3, sr=44100):
        """
        백색 소음(White Noise) 생성
        
        Parameters
        ----------
        duration : float
            지속 시간 (초)
        volume : float
            음량 (0~1)
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        numpy.ndarray
            음성 신호
        """
        n_samples = int(sr * duration)
        waveform = np.random.normal(0, 1, n_samples) * volume
        return waveform
    
    @staticmethod
    def pink_noise(duration, volume=0.3, sr=44100):
        """
        분홍색 소음(Pink Noise) 생성 - 자연스러운 소음
        
        Parameters
        ----------
        duration : float
            지속 시간 (초)
        volume : float
            음량 (0~1)
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        numpy.ndarray
            음성 신호
        """
        n_samples = int(sr * duration)
        
        # 백색 소음 생성
        white = np.random.normal(0, 1, n_samples)
        
        # Low-pass filter를 적용하여 pink noise 생성
        # 간단한 방법: 이전 샘플과의 이동 평균
        pink = np.zeros(n_samples)
        pink[0] = white[0]
        
        for i in range(1, n_samples):
            pink[i] = 0.99 * pink[i-1] + 0.01 * white[i]
        
        # 정규화
        pink = pink / np.max(np.abs(pink)) * volume
        
        return pink


# ============================================================================
# 2. 음향 신호 처리
# ============================================================================

class SoundProcessor:
    """음향 신호 처리"""
    
    @staticmethod
    def apply_envelope(waveform, envelope_type='linear', attack=0.05, 
                       release=0.05, sr=44100):
        """
        진폭 곡선(Envelope) 적용
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        envelope_type : str
            'linear', 'exp', 'hann' 중 선택
        attack : float
            상승 시간 (초)
        release : float
            하강 시간 (초)
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        numpy.ndarray
            envelope가 적용된 신호
        """
        n_samples = len(waveform)
        attack_samples = int(sr * attack)
        release_samples = int(sr * release)
        
        envelope = np.ones(n_samples)
        
        # Attack
        if envelope_type == 'linear':
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        elif envelope_type == 'exp':
            envelope[:attack_samples] = np.exp(np.linspace(-5, 0, attack_samples))
        elif envelope_type == 'hann':
            envelope[:attack_samples] = np.hanning(2*attack_samples)[:attack_samples]
        
        # Release
        if envelope_type == 'linear':
            envelope[-release_samples:] = np.linspace(1, 0, release_samples)
        elif envelope_type == 'exp':
            envelope[-release_samples:] = np.exp(np.linspace(0, -5, release_samples))
        elif envelope_type == 'hann':
            envelope[-release_samples:] = np.hanning(2*release_samples)[release_samples:]
        
        return waveform * envelope
    
    @staticmethod
    def apply_filter(waveform, filter_type='lowpass', cutoff_freq=1000, 
                     order=4, sr=44100):
        """
        필터 적용 (Low-pass, High-pass, Band-pass)
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        filter_type : str
            'lowpass', 'highpass', 'bandpass' 중 선택
        cutoff_freq : float or tuple
            차단 주파수 (Hz)
            - lowpass/highpass: float
            - bandpass: (low_freq, high_freq) tuple
        order : int
            필터 차수
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        numpy.ndarray
            필터링된 신호
        """
        nyquist = sr / 2
        
        if filter_type == 'lowpass':
            normalized_cutoff = cutoff_freq / nyquist
            b, a = signal.butter(order, normalized_cutoff, btype='low')
        elif filter_type == 'highpass':
            normalized_cutoff = cutoff_freq / nyquist
            b, a = signal.butter(order, normalized_cutoff, btype='high')
        elif filter_type == 'bandpass':
            low_freq, high_freq = cutoff_freq
            normalized_cutoff = [low_freq / nyquist, high_freq / nyquist]
            b, a = signal.butter(order, normalized_cutoff, btype='band')
        
        filtered = signal.filtfilt(b, a, waveform)
        return filtered
    
    @staticmethod
    def apply_amplitude_modulation(waveform, mod_frequency, 
                                   mod_depth=0.5, sr=44100):
        """
        진폭 변조(Amplitude Modulation) 적용
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        mod_frequency : float
            변조 주파수 (Hz)
        mod_depth : float
            변조 깊이 (0~1)
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        numpy.ndarray
            진폭 변조된 신호
        """
        n_samples = len(waveform)
        t = np.arange(n_samples) / sr
        
        # 변조 신호: 1 + depth*sin(2πf_mod*t)
        modulation = 1 + mod_depth * np.sin(2 * np.pi * mod_frequency * t)
        
        return waveform * modulation


# ============================================================================
# 3. 음향 신호 분석
# ============================================================================

class SoundAnalyzer:
    """음향 신호 분석"""
    
    @staticmethod
    def compute_spectrum(waveform, sr=44100):
        """
        동력 스펙트럼(Power Spectrum) 계산
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        frequencies : numpy.ndarray
            주파수 배열 (Hz)
        power : numpy.ndarray
            동력 스펙트럼
        """
        n = len(waveform)
        fft = np.fft.fft(waveform)
        power = np.abs(fft[:n//2])**2
        frequencies = np.fft.fftfreq(n, 1/sr)[:n//2]
        
        return frequencies, power
    
    @staticmethod
    def find_dominant_frequency(waveform, sr=44100):
        """
        지배적 주파수(Dominant Frequency) 찾기
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        sr : int
            샘플링 레이트 (Hz)
        
        Returns
        -------
        float
            지배적 주파수 (Hz)
        """
        frequencies, power = SoundAnalyzer.compute_spectrum(waveform, sr)
        idx = np.argmax(power)
        return frequencies[idx]
    
    @staticmethod
    def compute_loudness(waveform):
        """
        음량(Loudness) 계산 (RMS 기반)
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        
        Returns
        -------
        float
            음량 (dB)
        """
        rms = np.sqrt(np.mean(waveform**2))
        
        # dB로 변환 (reference: 1.0)
        db = 20 * np.log10(rms + 1e-10)
        
        return db
    
    @staticmethod
    def plot_spectrum(waveform, sr=44100, title='Power Spectrum'):
        """
        스펙트럼 시각화
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        sr : int
            샘플링 레이트 (Hz)
        title : str
            그래프 제목
        """
        frequencies, power = SoundAnalyzer.compute_spectrum(waveform, sr)
        
        plt.figure(figsize=(10, 4))
        plt.semilogy(frequencies, power)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_waveform(waveform, sr=44100, title='Waveform'):
        """
        파형 시각화
        
        Parameters
        ----------
        waveform : numpy.ndarray
            입력 음성 신호
        sr : int
            샘플링 레이트 (Hz)
        title : str
            그래프 제목
        """
        t = np.arange(len(waveform)) / sr
        
        plt.figure(figsize=(10, 4))
        plt.plot(t, waveform, linewidth=0.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


# ============================================================================
# 4. 테스트 및 데모
# ============================================================================

def demo():
    """데모: 다양한 음향 자극 생성 및 분석"""
    
    print("음향 자극 생성 및 분석 데모\n")
    
    # 1. 순음 생성
    print("1. 순음(Pure Tone) 생성: 440Hz, 1초")
    tone = ToneGenerator.pure_tone(440, 1.0)
    print(f"   신호 크기: {len(tone)} samples")
    
    # 2. 스윕음 생성
    print("\n2. 스윕음(Sweep Tone) 생성: 200Hz → 800Hz")
    sweep = ToneGenerator.sweep_tone(200, 800, 1.0)
    
    # 3. 복합음 생성
    print("\n3. 복합음(Complex Tone) 생성: 440Hz + 880Hz + 1320Hz")
    complex_tone = ToneGenerator.complex_tone(
        [440, 880, 1320],
        [0.5, 0.3, 0.2],
        1.0
    )
    
    # 4. 소음 생성
    print("\n4. 백색 소음(White Noise) 생성")
    white_noise = ToneGenerator.white_noise(1.0)
    print(f"   Pink Noise 생성")
    pink_noise = ToneGenerator.pink_noise(1.0)
    
    # 5. 신호 처리
    print("\n5. 신호 처리:")
    print("   - Envelope 적용 (attack=0.1s, release=0.2s)")
    envelope_tone = SoundProcessor.apply_envelope(tone, envelope_type='linear')
    
    print("   - Low-pass filter 적용 (cutoff=500Hz)")
    filtered_tone = SoundProcessor.apply_filter(tone, 'lowpass', 500)
    
    print("   - Amplitude Modulation 적용 (mod_freq=5Hz)")
    modulated_tone = SoundProcessor.apply_amplitude_modulation(tone, 5)
    
    # 6. 신호 분석
    print("\n6. 신호 분석:")
    dominant_freq = SoundAnalyzer.find_dominant_frequency(tone)
    print(f"   지배적 주파수: {dominant_freq:.1f}Hz")
    
    loudness = SoundAnalyzer.compute_loudness(tone)
    print(f"   음량(dB): {loudness:.1f}dB")
    
    loudness_noise = SoundAnalyzer.compute_loudness(white_noise)
    print(f"   백색소음 음량(dB): {loudness_noise:.1f}dB")
    
    print("\n데모 완료!")


if __name__ == '__main__':
    demo()
